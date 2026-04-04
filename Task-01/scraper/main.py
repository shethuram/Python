from scraper.fetcher import fetch_page, rate_limit
from scraper.parser import parse_books, get_next_page_url

BASE_URL = "http://books.toscrape.com/"


def main():
    all_products = []

    for page in range(1, 4):  # scrape first 3 pages
        url = get_next_page_url(BASE_URL, page)

        html = fetch_page(url)
        products = parse_books(html)

        print(f"Page {page}: Found {len(products)} products")

        all_products.extend(products)

        rate_limit()

    print(f"\nTotal products scraped: {len(all_products)}")

    # print sample
    for p in all_products[:5]:
        print(p)


if __name__ == "__main__":
    main()