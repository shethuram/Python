import schedule
import time
from main import run_scraper
from utils import log


# schedule at 2 AM
schedule.every().day.at("02:00").do(run_scraper)

log("Scheduler started — waiting for 02:00 AM...")

while True:
    schedule.run_pending()
    time.sleep(60)