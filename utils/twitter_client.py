import tweepy
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_twitter_client():
    """Get Twitter API v1.1 client for posting tweets"""
    try:
        auth = tweepy.OAuth1UserHandler(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
        api = tweepy.API(auth, wait_on_rate_limit=True)
        
        # Verify credentials
        api.verify_credentials()
        logger.info("Twitter API v1.1 authentication successful")
        return api
    except Exception as e:
        logger.error(f"Twitter API v1.1 authentication failed: {e}")
        return None

def get_bearer_client():
    """Get Twitter API v2 client for advanced features"""
    try:
        client = tweepy.Client(
            bearer_token=os.getenv("BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
            wait_on_rate_limit=True
        )
        
        # Test the connection
        me = client.get_me()
        logger.info(f"Twitter API v2 authentication successful for user: {me.data.username}")
        return client
    except Exception as e:
        logger.error(f"Twitter API v2 authentication failed: {e}")
        return None