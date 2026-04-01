from bs4 import BeautifulSoup
import re


def parse_books(html):
    soup = BeautifulSoup(html, "lxml")
    products = []

    items = soup.find_all("article", class_="product_pod")

    for item in items:
        # Name
        name = item.h3.a["title"]

        # Price (extract number using regex)
        price_text = item.find("p", class_="price_color").text
        price = float(re.sub(r"[^\d.]", "", price_text))

        # SKU (derive from URL)
        link = item.h3.a["href"]
        sku = link.split("/")[-2]

        products.append({
            "name": name,
            "price": price,
            "sku": sku
        })

    return products



def get_next_page_url(base_url, page_num):
    if page_num == 1:
        return base_url
    return f"http://books.toscrape.com/catalogue/page-{page_num}.html"