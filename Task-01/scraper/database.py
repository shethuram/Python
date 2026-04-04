import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

# Load env variables
load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def save_product(product):
    conn = get_connection()
    cur = conn.cursor()

    sku = product["sku"]
    name = product["name"]
    price = product["price"]

    # Check if product exists
    cur.execute("SELECT price FROM products WHERE sku = %s", (sku,))
    result = cur.fetchone()

    if result:
        old_price = float(result[0])

        if old_price != price:
            cur.execute(
                "UPDATE products SET price=%s, last_updated=%s WHERE sku=%s",
                (price, datetime.now(), sku)
            )
    else:
        cur.execute(
            "INSERT INTO products (sku, name, price) VALUES (%s, %s, %s)",
            (sku, name, price)
        )

    # Always track history
    cur.execute(
        "INSERT INTO price_history (sku, price) VALUES (%s, %s)",
        (sku, price)
    )

    conn.commit()
    cur.close()
    conn.close()



def fetch_price_changes():
    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT ph1.sku, ph1.price AS old_price, ph2.price AS new_price
    FROM price_history ph1
    JOIN price_history ph2
        ON ph1.sku = ph2.sku
        AND ph1.scraped_at < ph2.scraped_at
    WHERE ph2.scraped_at = (
        SELECT MAX(scraped_at)
        FROM price_history
        WHERE sku = ph1.sku
    )
    AND ph1.scraped_at = (
        SELECT MAX(scraped_at)
        FROM price_history
        WHERE sku = ph1.sku
        AND scraped_at < ph2.scraped_at
    )
    """

    cur.execute(query)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows
