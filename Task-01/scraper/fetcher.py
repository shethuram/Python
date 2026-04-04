import time
import random
import requests
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential

# Initialize user-agent generator
ua = UserAgent()


def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_page(url):
    try:
        headers = get_headers()

        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=10)

        # Handle status codes
        if response.status_code == 200:
            return response.text

        elif response.status_code == 429:
            print("Rate limited! Sleeping...")
            time.sleep(5)
            raise Exception("Retry due to rate limit")

        else:
            print(f"Error: {response.status_code}")
            response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise


def rate_limit():
    sleep_time = random.uniform(1, 3)
    print(f"Sleeping for {sleep_time:.2f} seconds")
    time.sleep(sleep_time)