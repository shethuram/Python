from scraper.database import fetch_price_changes
import csv
import os
from datetime import datetime


def generate_report():
    changes = fetch_price_changes()

    print("\n=== Price Change Report ===")

    if not changes:
        print("No price changes detected.")
        return

    # Create reports folder if not exists
    os.makedirs("reports", exist_ok=True)

    filename = f"reports/{datetime.now().date()}.csv"

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Product", "Old Price", "New Price", "Change"])

        print(f"{'Product':30} | {'Old Price':10} | {'New Price':10} | {'Change'}")
        print("-" * 70)

        count = 0

        for sku, old_price, new_price in changes:
            if old_price == new_price:
                continue

            change_percent = ((new_price - old_price) / old_price) * 100

            writer.writerow([
                sku,
                f"{old_price:.2f}",
                f"{new_price:.2f}",
                f"{change_percent:+.2f}%"
            ])

            print(f"{sku[:30]:30} | {old_price:<10.2f} | {new_price:<10.2f} | {change_percent:+.2f}%")
            count += 1

    print(f"\n{count} price changes detected.")
    print(f"Report saved to {filename}")