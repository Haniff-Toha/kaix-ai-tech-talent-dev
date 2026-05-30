"""
RAG chunk generator for scraped courses.

Converts structured course dicts into natural language chunks
that get embedded and stored in the knowledge_rag table.
"""

import logging
import uuid

from sqlalchemy import text as sa_text

from app.db.session import async_session
from app.services.embedding_service import embedding_service

logger = logging.getLogger(__name__)


def generate_course_chunk(course: dict) -> str:
    """
    Generate a natural language RAG chunk from a structured course dict.

    The chunk is optimized for semantic search — it reads like a
    recommendation the Roadmap Agent would make.
    """
    source = course.get("source", "unknown")
    title = course.get("title", "Unknown")
    platform = course.get("platform_display", source.capitalize())
    level = course.get("level", "beginner")
    language = course.get("language", "en")
    lang_label = "Bahasa Indonesia" if language == "id" else "English"

    # Duration
    duration = course.get("duration_hours")
    if duration:
        if duration < 1:
            dur_label = f"{int(duration * 60)} menit"
        else:
            dur_label = f"{duration:.0f} jam"
    else:
        dur_label = "durasi tidak diketahui"

    # Price
    is_free = course.get("is_free", False)
    price_idr = course.get("price_idr_approx")
    if is_free:
        price_label = "Gratis"
    elif price_idr:
        price_label = f"Rp {price_idr:,}".replace(",", ".")
    else:
        price_label = "Berbayar"

    # Rating
    rating = course.get("rating")
    rating_count = course.get("rating_count")
    rating_parts = []
    if rating:
        rating_parts.append(f"Rating {rating:.1f}/5")
    if rating_count:
        if source == "youtube":
            rating_parts.append(f"{rating_count:,} views".replace(",", "."))
        else:
            rating_parts.append(f"{rating_count:,} siswa".replace(",", "."))
    rating_label = ". ".join(rating_parts) + "." if rating_parts else ""

    # Certificate
    cert_label = "Dilengkapi sertifikat." if course.get("has_certificate") else ""

    # Skills
    skills = course.get("skills_covered", [])
    skills_label = ", ".join(skills[:5]) if skills else "pemrograman umum"

    # Career tracks
    tracks = course.get("career_tracks", [])
    tracks_label = ", ".join(t.replace("_", " ") for t in tracks)

    # Instructor
    instructor = course.get("instructor")
    instructor_label = f"Oleh {instructor}. " if instructor else ""

    # Source-specific context
    extra_context = ""

    if source == "dicoding":
        # Learning path sequence info
        for tag in (course.get("topics_covered") or []):
            if isinstance(tag, str):
                if tag.startswith("dicoding_path_name:"):
                    path_name = tag.replace("dicoding_path_name:", "")
                    if path_name and path_name != "catalog":
                        extra_context += f"Bagian dari learning path '{path_name}' di Dicoding. "
                if tag.startswith("dicoding_path_sequence:"):
                    seq = tag.replace("dicoding_path_sequence:", "")
                    if seq and seq != "0":
                        extra_context += f"Kelas ke-{seq} dalam urutan. "

    elif source == "youtube":
        for tag in (course.get("topics_covered") or []):
            if isinstance(tag, str) and tag.startswith("channel:"):
                channel = tag.replace("channel:", "")
                extra_context += f"Channel: {channel}. "

    elif source == "book":
        extra_context += "Format: Buku. "

    # Description
    desc = course.get("description_short")
    desc_label = f"\n{desc}" if desc else ""

    chunk = (
        f"Sumber belajar: '{title}' di {platform}. "
        f"Bahasa: {lang_label}. Level: {level}. "
        f"Durasi: {dur_label}. Harga: {price_label}. "
        f"{instructor_label}"
        f"{rating_label} "
        f"{cert_label} "
        f"Skill yang dipelajari: {skills_label}. "
        f"Relevan untuk: {tracks_label}. "
        f"{extra_context}"
        f"{desc_label}"
    ).strip()

    return chunk


def generate_chunk_metadata(course: dict) -> dict:
    """Generate metadata JSONB for a course RAG chunk."""
    return {
        "content_type": "course_resource",
        "source": course.get("source", "unknown"),
        "platform": course.get("platform_display", ""),
        "career_track": (course.get("career_tracks") or ["unknown"])[0],
        "skill_name": (course.get("skills_covered") or [None])[0],
        "seniority": _level_to_seniority(course.get("level", "beginner")),
        "language": course.get("language", "en"),
        "is_free": course.get("is_free", False),
        "tags": _generate_tags(course),
        "content_hash": course.get("content_hash"),
    }


async def update_course_rag(courses: list[dict], batch_size: int = 20) -> int:
    """
    Generate RAG chunks from courses, embed, and upsert into knowledge_rag.

    Only adds/updates course-type chunks — leaves curated knowledge intact.
    Returns number of chunks updated.
    """
    if not courses:
        return 0

    count = 0

    async with async_session() as db:
        for i in range(0, len(courses), batch_size):
            batch = courses[i : i + batch_size]

            # Generate chunks and check against database
            chunks_to_embed = []
            for course in batch:
                chunk_text = generate_course_chunk(course)
                metadata = generate_chunk_metadata(course)
                career_track = (course.get("career_tracks") or ["unknown"])[0]
                content_hash = course.get("content_hash")

                # Look up existing RAG chunk by content_hash to check if content changed
                existing_content = None
                if content_hash:
                    res = await db.execute(
                        sa_text(
                            "SELECT content FROM knowledge_rag WHERE "
                            "metadata->>'content_type' = 'course_resource' AND "
                            "metadata->>'content_hash' = :content_hash"
                        ),
                        {"content_hash": content_hash}
                    )
                    row = res.fetchone()
                    if row:
                        existing_content = row[0]

                # If the exact same content is already embedded, skip to avoid duplicates and save quota
                if existing_content == chunk_text:
                    logger.info(f"⏭ Skipping embedding for '{course.get('title')}' — chunk text unchanged")
                    continue

                # Delete old chunk if content changed or if we need to replace it
                if content_hash:
                    await db.execute(
                        sa_text(
                            "DELETE FROM knowledge_rag WHERE "
                            "metadata->>'content_type' = 'course_resource' AND "
                            "metadata->>'content_hash' = :content_hash"
                        ),
                        {"content_hash": content_hash}
                    )

                chunks_to_embed.append({
                    "content": chunk_text,
                    "metadata": metadata,
                    "career_track": career_track,
                })

            if not chunks_to_embed:
                continue

            # Embed only the chunks that are new or updated
            texts = [c["content"] for c in chunks_to_embed]
            try:
                embeddings = await embedding_service.embed_documents(texts)
            except Exception as e:
                logger.error(f"Embedding failed for batch {i}: {e}")
                continue

            # Insert
            for chunk, embedding in zip(chunks_to_embed, embeddings):
                await db.execute(
                    sa_text(
                        "INSERT INTO knowledge_rag (id, content, embedding, metadata, career_track) "
                        "VALUES (:id, :content, :embedding, :metadata, :career_track)"
                    ),
                    {
                        "id": str(uuid.uuid4()),
                        "content": chunk["content"],
                        "embedding": str(embedding),
                        "metadata": __import__("json").dumps(chunk["metadata"]),
                        "career_track": chunk["career_track"],
                    },
                )

            count += len(chunks_to_embed)
            logger.info(
                f"  RAG batch {i // batch_size + 1}: "
                f"{len(chunks_to_embed)} chunks embedded and stored"
            )

        await db.commit()

    logger.info(f"✅ RAG update complete: {count} course chunks added/updated")
    return count


def _level_to_seniority(level: str) -> str:
    return {
        "beginner": "beginner",
        "intermediate": "junior",
        "advanced": "mid",
    }.get(level, "all")


def _generate_tags(course: dict) -> list[str]:
    tags = []
    tags.append(course.get("source", "unknown"))
    tags.append(course.get("platform_display", "").lower())
    if course.get("is_free"):
        tags.append("free")
    if course.get("has_certificate"):
        tags.append("certificate")
    if course.get("is_bahasa_indonesia"):
        tags.append("bahasa-indonesia")
    tags.extend(course.get("skills_covered", [])[:3])
    return [t for t in tags if t]
