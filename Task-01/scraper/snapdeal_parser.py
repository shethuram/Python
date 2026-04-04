from bs4 import BeautifulSoup


def parse_snapdeal(html):
    soup = BeautifulSoup(html, "lxml")
    products = []

    items = soup.find_all("div", class_="product-tuple-listing")

    for item in items:
        try:
            name = item.find("p", class_="product-title").text.strip()

            price_tag = item.find("span", class_="product-price")
            if not price_tag:
                continue

            price = price_tag.text.strip()
            price = float(price.replace("Rs.", "").replace(",", ""))

            sku = item.get("data-id")

            # 🚨 IMPORTANT FIX
            if not sku:
                continue

            products.append({
                "name": name,
                "price": price,
                "sku": sku
            })

        except Exception:
            continue

    return products