"""
Knowledge RAG ingestion script.

Parses the Knowledge RAG markdown files and embeds all chunks into PostgreSQL.

Usage:
    python -m scripts.ingest_knowledge_rag

Expects two markdown files in the project root:
    - ../knowledge_rag_template.md     (Backend Engineer track)
    - ../knowledge_rag_all_tracks.md   (All other 7 tracks)
"""

import asyncio
import logging
import re
import json
from pathlib import Path

from app.config import settings
from app.db.session import async_session
from app.services.embedding_service import embedding_service
from app.db.models import KnowledgeRAGChunk
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths to RAG source files
RAG_FILES = [
    Path(__file__).parent.parent.parent / "knowledge_rag_template.md",
    Path(__file__).parent.parent.parent / "knowledge_rag_all_tracks.md",
]


def parse_chunks(markdown_text: str) -> list[dict]:
    """
    Parse the Knowledge RAG markdown format into structured chunks.

    Each chunk is delimited by '---chunk---' and contains:
        - Metadata (JSON in a code block)
        - Content (plain text after ### Content)
    """
    chunks = []
    raw_chunks = re.split(r"---chunk---", markdown_text)

    for raw in raw_chunks:
        raw = raw.strip()
        if not raw or len(raw) < 50:
            continue

        # Extract metadata JSON
        metadata = {}
        json_match = re.search(r"```json\s*\n(.*?)\n\s*```", raw, re.DOTALL)
        if json_match:
            try:
                metadata = json.loads(json_match.group(1))
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse metadata JSON: {json_match.group(1)[:100]}")

        # Extract content (everything after ### Content)
        content_match = re.search(r"###\s*Content\s*\n(.*)", raw, re.DOTALL)
        if content_match:
            content = content_match.group(1).strip()
        else:
            # Fallback: use everything after the metadata block
            content = re.sub(r"###\s*Metadata.*?```", "", raw, flags=re.DOTALL).strip()

        if content and len(content) > 20:
            # Skip chunks without proper metadata (template headers, etc.)
            if not metadata:
                logger.debug(f"  Skipping chunk without metadata: {content[:60]}...")
                continue

            chunks.append({
                "content": content,
                "metadata": metadata,
                "career_track": metadata.get("career_track", "unknown"),
            })

    return chunks


async def ingest():
    """Main ingestion function."""
    all_chunks = []

    for filepath in RAG_FILES:
        if not filepath.exists():
            logger.warning(f"RAG file not found: {filepath}")
            continue

        logger.info(f"Parsing: {filepath.name}")
        file_content = filepath.read_text(encoding="utf-8")
        chunks = parse_chunks(file_content)
        logger.info(f"  Found {len(chunks)} chunks")
        all_chunks.extend(chunks)

    logger.info(f"\nTotal chunks to embed: {len(all_chunks)}")

    if not all_chunks:
        logger.error("No chunks found! Check file paths and format.")
        return

    # Embed in batches
    batch_size = 20
    async with async_session() as db:
        # Clear existing knowledge RAG data
        await db.execute(text("DELETE FROM knowledge_rag"))
        logger.info("Cleared existing knowledge_rag table")

        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i : i + batch_size]
            contents = [c["content"] for c in batch]

            logger.info(f"Embedding batch {i // batch_size + 1}/{(len(all_chunks) + batch_size - 1) // batch_size} ({len(contents)} chunks)...")

            try:
                embeddings = await embedding_service.embed_documents(contents)
            except Exception as e:
                logger.error(f"Embedding failed for batch {i}: {e}")
                continue

            for chunk, embedding in zip(batch, embeddings):
                record = KnowledgeRAGChunk(
                    content=chunk["content"],
                    embedding=embedding,
                    metadata_=chunk["metadata"],
                    career_track=chunk["career_track"],
                )
                db.add(record)

            await db.flush()
            logger.info(f"  Stored {len(batch)} chunks")

        await db.commit()

    logger.info(f"\n✅ Ingestion complete! {len(all_chunks)} chunks embedded and stored.")


if __name__ == "__main__":
    asyncio.run(ingest())
