from scraper import scrape_products
from db import init_db, save_products, get_price_changes
from report import save_report
from utils import log


def main():
    log("Scraper started — target: flipkart")

    init_db()

    products = scrape_products(log)

    save_products(products)

    log(f"Total: {len(products)} products saved to DB")

    changes = get_price_changes()

    print("\n=== Price Change Report ===")
    print("| Product | Old Price | New Price | Change |")

    for name, old, new, change in changes:
        print(f"| {name[:30]} | ₹{old} | ₹{new} | {change}% |")

    log(f"{len(changes)} price changes detected")

    file = save_report(changes)

    log(f"Report saved to {file}")


if __name__ == "__main__":
    main()