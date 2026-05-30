"""Inspect scraped_courses data quality."""
import asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import text
from app.db.session import async_session

async def main():
    async with async_session() as db:
        # Check all columns for a sample
        r = await db.execute(text(
            "SELECT title, url, platform_display, description_short, career_tracks, "
            "source, level, skills_covered, is_free, rating "
            "FROM scraped_courses ORDER BY created_at LIMIT 15"
        ))
        print("=" * 80)
        print("SCRAPED COURSES SAMPLE")
        print("=" * 80)
        for row in r.fetchall():
            d = dict(row._mapping)
            desc = (d['description_short'] or '')
            print(f"\nTITLE: {d['title']}")
            print(f"  URL: {d['url']}")
            print(f"  Platform: {d['platform_display']} | Source: {d['source']}")
            print(f"  Level: {d['level']} | Free: {d['is_free']} | Rating: {d['rating']}")
            print(f"  Tracks: {d['career_tracks']}")
            print(f"  Skills: {d['skills_covered']}")
            print(f"  Desc: {desc[:120]}")

        # Count titles that look like prices
        r2 = await db.execute(text(
            "SELECT COUNT(*) as bad FROM scraped_courses WHERE title LIKE 'Rp%' OR title LIKE '$%'"
        ))
        bad = r2.scalar()
        r3 = await db.execute(text("SELECT COUNT(*) FROM scraped_courses"))
        total = r3.scalar()
        print(f"\n{'=' * 80}")
        print(f"DATA QUALITY: {bad}/{total} titles look like prices")

        # Check for actual course names in description
        if bad > 0:
            r4 = await db.execute(text(
                "SELECT title, description_short, url FROM scraped_courses "
                "WHERE title LIKE 'Rp%' LIMIT 5"
            ))
            print("\nBad title samples:")
            for row in r4.fetchall():
                d = dict(row._mapping)
                desc = (d['description_short'] or 'NO DESC')
                print(f"  title='{d['title']}' desc='{desc[:80]}' url={d['url']}")

asyncio.run(main())
