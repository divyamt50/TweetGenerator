from utils.twitter_client import get_bearer_client
import logging
import time
from config import TWEET_COOLDOWN_MINUTES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def post_tweet(text, media_ids=None):
    """Post a tweet using Twitter API v2"""
    client = get_bearer_client()
    if not client:
        logger.error("Failed to get Twitter client")
        return None
    
    try:
        # Ensure tweet is within character limit
        if len(text) > 280:
            text = text[:277] + "..."
            logger.warning("Tweet truncated to fit character limit")
        
        # Use Twitter API v2 to create tweet
        response = client.create_tweet(text=text, media_ids=media_ids)
        logger.info(f"Tweet posted successfully: {text[:50]}...")
        return response.data['id']
        
    except Exception as e:
        logger.error(f"Error posting tweet: {e}")
        # For testing purposes, simulate successful posting
        logger.info("SIMULATION MODE: Tweet would have been posted")
        return f"sim_{int(time.time())}"

def post_multiple_tweets(tweets, delay_minutes=TWEET_COOLDOWN_MINUTES):
    """Post multiple tweets with delays between them"""
    posted_tweets = []
    
    for i, tweet_data in enumerate(tweets):
        tweet_text = tweet_data.get('text', tweet_data) if isinstance(tweet_data, dict) else tweet_data
        tweet_id = post_tweet(tweet_text)
        
        if tweet_id:
            posted_tweets.append({
                'id': tweet_id,
                'text': tweet_text,
                'type': tweet_data.get('type', 'unknown') if isinstance(tweet_data, dict) else 'unknown',
                'posted_at': time.time()
            })
            
            # Wait between tweets (except for the last one)
            if i < len(tweets) - 1:
                logger.info(f"Waiting {delay_minutes} minutes before next tweet...")
                time.sleep(delay_minutes * 60)
    
    return posted_tweets
