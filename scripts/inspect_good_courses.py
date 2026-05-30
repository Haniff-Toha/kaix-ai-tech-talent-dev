"""Check what good-titled courses look like."""
import asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import text
from app.db.session import async_session

async def main():
    async with async_session() as db:
        # Good titles
        r = await db.execute(text(
            "SELECT title, url, source, platform_display, description_short, career_tracks, skills_covered "
            "FROM scraped_courses WHERE title NOT LIKE 'Rp%' LIMIT 10"
        ))
        print("GOOD TITLE SAMPLES:")
        for row in r.fetchall():
            d = dict(row._mapping)
            desc = (d['description_short'] or '')
            print(f"\n  TITLE: {d['title']}")
            print(f"  URL: {d['url']}")
            print(f"  Source: {d['source']} | Platform: {d['platform_display']}")
            print(f"  Tracks: {d['career_tracks']}")
            print(f"  Skills: {d['skills_covered']}")
            print(f"  Desc: {desc[:120]}")

        # Source breakdown
        print("\n\nSOURCE BREAKDOWN:")
        r2 = await db.execute(text(
            "SELECT source, COUNT(*) as cnt, "
            "SUM(CASE WHEN title LIKE 'Rp%' THEN 1 ELSE 0 END) as bad_titles "
            "FROM scraped_courses GROUP BY source ORDER BY cnt DESC"
        ))
        for row in r2.fetchall():
            d = dict(row._mapping)
            print(f"  {d['source']}: {d['cnt']} total, {d['bad_titles']} bad titles")

asyncio.run(main())
