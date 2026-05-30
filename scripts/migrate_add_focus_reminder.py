"""Migration: Add is_today_focus to courses, label + linked_course_id to reminders."""
import asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["OPENBLAS_NUM_THREADS"] = "1"
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import text
from app.db.session import async_session

STATEMENTS = [
    "ALTER TABLE courses ADD COLUMN IF NOT EXISTS is_today_focus BOOLEAN DEFAULT FALSE",
    "ALTER TABLE reminders ADD COLUMN IF NOT EXISTS label TEXT",
    "ALTER TABLE reminders ADD COLUMN IF NOT EXISTS linked_course_id UUID REFERENCES courses(id) ON DELETE SET NULL",
]

async def main():
    async with async_session() as db:
        for stmt in STATEMENTS:
            print(f"  > {stmt[:60]}...")
            await db.execute(text(stmt))
        await db.commit()
    print("\n✅ Migration complete!")

asyncio.run(main())
