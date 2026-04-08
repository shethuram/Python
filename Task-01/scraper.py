from playwright.sync_api import sync_playwright
import time
import random


#  ROTATING USER AGENTS
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/118.0"
]


#  RETRY LOGIC
def safe_goto(page, url):
    for _ in range(3):
        try:
            res = page.goto(url, timeout=60000)
            if res and res.status == 200:
                return True
        except:
            time.sleep(2)
    return False


def scrape_products(log):
    products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        #  apply rotating user-agent
        context = browser.new_context(
            user_agent=random.choice(USER_AGENTS)
        )
        page = context.new_page()

        MAX_PAGES = 3

        page_num = 1

        while page_num <= MAX_PAGES:
            url = f"https://www.flipkart.com/search?q=headphones&page={page_num}"

            if not safe_goto(page, url):
                break

            page.wait_for_timeout(2000)

            cards = page.locator("div[data-id]")
            count = cards.count()

            if count == 0:
                break

            log(f"Page {page_num}/{MAX_PAGES} — {count} products extracted")

            for i in range(count):
                try:
                    card = cards.nth(i)

                    name = card.locator("a[title]").first.get_attribute("title")
                    price = card.locator("text=₹").first.text_content()

                    if name and price:
                        products.append({
                            "name": name.strip(),
                            "price": price.strip()
                        })
                except:
                    continue

            page_num += 1
            time.sleep(random.uniform(1, 2))

        browser.close()

    return products