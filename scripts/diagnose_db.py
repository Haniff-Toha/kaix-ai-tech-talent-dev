"""
Quick diagnostic script — checks DB tables individually.
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import text
from app.db.session import async_session


async def run_query(label, sql_str):
    """Run a single query in its own session."""
    try:
        async with async_session() as db:
            result = await db.execute(text(sql_str))
            rows = result.fetchall()
            print(f"\n[{label}]")
            for row in rows:
                print(f"  {dict(row._mapping)}")
            return rows
    except Exception as e:
        print(f"\n[{label}] ERROR: {e}")
        return []


async def main():
    print("=" * 60)
    print("KAIX DATABASE DIAGNOSTIC")
    print("=" * 60)

    # 1. knowledge_rag
    await run_query("knowledge_rag count", "SELECT COUNT(*) as total FROM knowledge_rag")
    await run_query("knowledge_rag career tracks",
                    "SELECT career_track, COUNT(*) as cnt FROM knowledge_rag GROUP BY career_track ORDER BY cnt DESC")
    await run_query("knowledge_rag embeddings",
                    "SELECT COUNT(*) as with_embedding FROM knowledge_rag WHERE embedding IS NOT NULL")
    await run_query("knowledge_rag embedding dims",
                    "SELECT vector_dims(embedding) as dims FROM knowledge_rag WHERE embedding IS NOT NULL LIMIT 1")
    await run_query("knowledge_rag sample content",
                    "SELECT LEFT(content, 150) as preview, career_track, metadata FROM knowledge_rag LIMIT 3")

    # 2. scraped_courses
    await run_query("scraped_courses count", "SELECT COUNT(*) as total FROM scraped_courses")
    await run_query("scraped_courses sample",
                    "SELECT title, platform_display, level, career_tracks FROM scraped_courses LIMIT 3")

    # 3. profiles
    await run_query("profiles",
                    "SELECT user_id, target_role, experience_level, onboarding_completed FROM profiles LIMIT 3")

    # 4. jobs
    await run_query("recent jobs",
                    "SELECT id, type, status, LEFT(COALESCE(error,''), 200) as error FROM jobs ORDER BY created_at DESC LIMIT 5")

    # 5. roadmaps
    await run_query("roadmaps", "SELECT COUNT(*) as total FROM roadmaps")

    # 6. users
    await run_query("users", "SELECT id, name, email FROM users LIMIT 3")

    # 7. embedding dimension from settings
    from app.config import settings
    print(f"\n[Settings] embedding_dimension = {settings.embedding_dimension}")


if __name__ == "__main__":
    asyncio.run(main())
