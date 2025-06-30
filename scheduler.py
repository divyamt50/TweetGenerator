import schedule
import time
from main import run_scheduled
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_scheduler():
    """Setup automated posting schedule"""
    # Post 3 times a day: morning, afternoon, evening
    schedule.every().day.at("09:00").do(run_scheduled)
    schedule.every().day.at("14:00").do(run_scheduled)
    schedule.every().day.at("19:00").do(run_scheduled)
    
    logger.info("Scheduler setup complete. Bot will post 3 times daily.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    setup_scheduler()