from scraper.fetcher import fetch_page, rate_limit
from scraper.parser import parse_books, get_next_page_url
from scraper.snapdeal_parser import parse_snapdeal
from scraper.database import save_product
from scraper.report import generate_report
from scraper.js_scraper import fetch_js_page
from scraper.snapdeal_api import fetch_snapdeal_products
from datetime import datetime

# -------------------------------
# BASE URLS
# -------------------------------

# BooksToScrape (HTML parsing)
# BASE_URL = "http://books.toscrape.com/"

# Snapdeal (API based)
BASE_QUERY = "tshirt"


# -------------------------------
# BOOKS SCRAPER (HTML) - NOT USED
# -------------------------------

'''
def main():
    start_time = datetime.now()
    print(f"[{start_time}] Scraper started — target: BooksToScrape")

    total_products = 0

    for page in range(1, 4):
        url = get_next_page_url(BASE_URL, page)

        html = fetch_page(url)
        products = parse_books(html)

        print(f"[{datetime.now()}] Page {page} — {len(products)} products extracted")

        for p in products:
            save_product(p)

        total_products += len(products)

        rate_limit()

    end_time = datetime.now()

    print(f"\n[{end_time}] Total: {total_products} products saved to DB")

    generate_report()
'''


# -------------------------------
# SNAPDEAL (JS + HTML) - NOT USED
# -------------------------------

'''
def main():
    print(f"[{datetime.now()}] Scraper started — target: Snapdeal (JS)")

    total_products = 0

    for page in range(1, 4):
        url = f"https://www.snapdeal.com/search?keyword=tshirt&page={page}"

        html = fetch_js_page(url)
        products = parse_snapdeal(html)

        print(f"[{datetime.now()}] Page {page} — {len(products)} products extracted")

        for p in products:
            save_product(p)

        total_products += len(products)

        rate_limit()

    print(f"\nTotal: {total_products} products saved to DB")

    generate_report()
'''


# -------------------------------
# SNAPDEAL (API) - ACTIVE VERSION ✅
# -------------------------------

def main():
    print(f"[{datetime.now()}] Scraper started — target: Snapdeal API")

    total_products = 0

    for page in range(3):
        start = page * 12

        products = fetch_snapdeal_products(BASE_QUERY, start)

        print(f"[{datetime.now()}] Page {page+1} — {len(products)} products extracted")

        for p in products:
            save_product(p)

        total_products += len(products)

        rate_limit()

    print(f"\nTotal: {total_products} products saved to DB")

    generate_report()


if __name__ == "__main__":
    main()