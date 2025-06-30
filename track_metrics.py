from utils.twitter_client import get_bearer_client
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def track_metrics(tweet_id, wait_minutes=5):
    """Track metrics for a specific tweet"""
    client = get_bearer_client()
    if not client:
        logger.error("Failed to get Twitter client")
        return {}
    
    # Wait for initial engagement
    if wait_minutes > 0:
        logger.info(f"Waiting {wait_minutes} minutes for initial engagement...")
        time.sleep(wait_minutes * 60)
    
    try:
        response = client.get_tweet(
            tweet_id, 
            tweet_fields=["public_metrics", "created_at", "context_annotations"]
        )
        
        if response.data:
            metrics = response.data.public_metrics
            return {
                "tweet_id": tweet_id,
                "likes": metrics.get("like_count", 0),
                "retweets": metrics.get("retweet_count", 0),
                "replies": metrics.get("reply_count", 0),
                "quotes": metrics.get("quote_count", 0),
                "bookmarks": metrics.get("bookmark_count", 0),
                "impressions": metrics.get("impression_count", 0),
                "created_at": str(response.data.created_at),
                "engagement_rate": calculate_engagement_rate(metrics)
            }
    except Exception as e:
        logger.error(f"Error tracking metrics for tweet {tweet_id}: {e}")
        return {}

def calculate_engagement_rate(metrics):
    """Calculate engagement rate from public metrics"""
    total_engagements = (
        metrics.get("like_count", 0) + 
        metrics.get("retweet_count", 0) + 
        metrics.get("reply_count", 0) + 
        metrics.get("quote_count", 0)
    )
    impressions = metrics.get("impression_count", 0)
    
    if impressions > 0:
        return round((total_engagements / impressions) * 100, 2)
    return 0

def track_multiple_tweets(tweet_ids, wait_minutes=60):
    """Track metrics for multiple tweets"""
    all_metrics = []
    
    for tweet_id in tweet_ids:
        metrics = track_metrics(tweet_id, wait_minutes=0)  # No wait for batch processing
        if metrics:
            all_metrics.append(metrics)
    
    return all_metrics
