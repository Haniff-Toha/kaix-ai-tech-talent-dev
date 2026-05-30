"""
Fix scraped courses where the title contains a price (e.g., 'Rp950,000')
instead of the actual course name.

For Dicoding courses, we extract the real name from the URL slug.
Example: https://www.dicoding.com/academies/555-belajar-fundamental-analisis-data
  -> "Belajar Fundamental Analisis Data"
"""

import asyncio
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import text
from app.db.session import async_session


def extract_title_from_url(url: str) -> str | None:
    """
    Extract a readable course title from a Dicoding URL slug.
    
    Example:
        'https://www.dicoding.com/academies/555-belajar-fundamental-analisis-data'
        -> 'Belajar Fundamental Analisis Data'
    """
    if not url:
        return None

    # Match the slug part after the last /
    match = re.search(r'/(\d+-[^/]+)$', url)
    if not match:
        return None

    slug = match.group(1)
    # Remove the numeric prefix (e.g., '555-')
    slug = re.sub(r'^\d+-', '', slug)
    # Convert hyphens to spaces and title case
    title = slug.replace('-', ' ').title()

    return title


async def main():
    async with async_session() as db:
        # Find all courses with price-like titles
        result = await db.execute(text(
            "SELECT id, title, url, source FROM scraped_courses "
            "WHERE title LIKE 'Rp%' OR title LIKE '$%'"
        ))
        bad_courses = result.fetchall()

        print(f"Found {len(bad_courses)} courses with bad titles")

        fixed = 0
        skipped = 0

        for row in bad_courses:
            course_id = row.id
            old_title = row.title
            url = row.url
            source = row.source

            new_title = extract_title_from_url(url)

            if new_title:
                # Store the old price as price_idr_approx
                price_str = old_title.replace('Rp', '').replace(',', '').strip()
                try:
                    price_idr = int(price_str)
                except ValueError:
                    price_idr = None

                await db.execute(
                    text(
                        "UPDATE scraped_courses SET title = :title, "
                        "price_idr_approx = COALESCE(price_idr_approx, :price) "
                        "WHERE id = :id"
                    ),
                    {"title": new_title, "price": price_idr, "id": course_id},
                )
                print(f"  FIXED: '{old_title}' -> '{new_title}' (price={price_idr})")
                fixed += 1
            else:
                print(f"  SKIP: '{old_title}' - could not extract title from URL: {url}")
                skipped += 1

        await db.commit()
        print(f"\nDone! Fixed: {fixed}, Skipped: {skipped}")

        # Verify
        result = await db.execute(text(
            "SELECT COUNT(*) FROM scraped_courses WHERE title LIKE 'Rp%'"
        ))
        remaining = result.scalar()
        print(f"Remaining bad titles: {remaining}")


if __name__ == "__main__":
    asyncio.run(main())
