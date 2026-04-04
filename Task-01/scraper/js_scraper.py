from playwright.sync_api import sync_playwright


def fetch_js_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        # open page
        page.goto(url)

        # wait for products to load
        page.wait_for_selector("div.product-tuple-listing")

        html = page.content()

        browser.close()

        return html