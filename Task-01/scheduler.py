import schedule
import time
from main import main
from utils import log


# schedule at 2 AM
schedule.every().day.at("02:00").do(main)

log("Scheduler started — waiting for 02:00 AM...")

while True:
    schedule.run_pending()
    time.sleep(60)