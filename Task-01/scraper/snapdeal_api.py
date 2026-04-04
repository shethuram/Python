import requests


def fetch_snapdeal_products(query, start=0):
    url = "https://m.snapdeal.com/service/get/search/v3/getSearchResults"

    params = {
        "keyword": query,
        "start": start,
        "number": 12,
        "sortBy": "rlvncy",
        "categoryId": 0
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print("❌ Failed:", response.status_code)
        return []

    try:
        data = response.json()

    except:
        print("❌ Not JSON")
        print(response.text[:200])
        return []

    products = []

    items = data.get("searchResultDTOMobile", {}).get("catalogSearchDTOMobile", [])

    for item in items:
        try:
            name = item.get("title") or item.get("actualProductName")
            price = item.get("sellingPrice")
            sku = str(item.get("id"))

            if not name or not price or not sku:
                continue

            products.append({
                "name": name,
                "price": float(price),
                "sku": sku
            })

        except:
            continue

    return products