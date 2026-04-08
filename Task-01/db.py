import sqlite3
from datetime import date, timedelta
import os

DB_PATH = "data/products.db"


def init_db():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        name TEXT,
        price REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_products(products):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    today = str(date.today())

    for p in products:
        try:
            price = float(p["price"].replace("₹", "").replace(",", ""))

            cur.execute(
                "INSERT INTO products VALUES (?, ?, ?)",
                (p["name"], price, today)
            )
        except:
            continue

    conn.commit()
    conn.close()


def get_price_changes():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))

    cur.execute("SELECT name, price FROM products WHERE date=?", (today,))
    today_data = dict(cur.fetchall())

    cur.execute("SELECT name, price FROM products WHERE date=?", (yesterday,))
    yesterday_data = dict(cur.fetchall())

    conn.close()

    changes = []

    for name in today_data:
        if name in yesterday_data:
            old = yesterday_data[name]
            new = today_data[name]

            if old != new:
                change = ((new - old) / old) * 100
                changes.append((name, old, new, round(change, 2)))

    return changes