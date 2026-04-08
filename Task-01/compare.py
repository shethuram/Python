import sqlite3

DB_PATH = "data/products.db"


def compare_prices():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT name, price, date FROM products
    ORDER BY name, date DESC
    """)

    rows = cur.fetchall()
    conn.close()

    changes = []
    latest = {}

    for name, price, dt in rows:
        if name not in latest:
            latest[name] = price
        else:
            old_price = latest[name]
            new_price = price

            if old_price != new_price:
                change = ((new_price - old_price) / old_price) * 100
                changes.append((name, old_price, new_price, round(change, 2)))

    return changes