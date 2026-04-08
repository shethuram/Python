import csv
from datetime import date
import os


def save_report(changes):
    os.makedirs("reports", exist_ok=True)

    filename = f"reports/{date.today()}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow(["Product", "Old Price", "New Price", "Change %"])

        for row in changes:
            writer.writerow(row)

    return filename