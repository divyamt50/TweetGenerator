from trend_discovery import get_trending_tweet_patterns, get_hashtag_trends
from generate_tweets import generate_tweets
from post_tweet import post_multiple_tweets
from track_metrics import track_multiple_tweets
from optimize_strategy import optimize_strategy
import logging
import json
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main bot execution function"""
    logger.info("Starting Twitter Bot execution...")
    
    try:
        # 1. Discover current trends
        logger.info("Step 1: Discovering trends...")
        patterns = get_trending_tweet_patterns()
        hashtags = get_hashtag_trends()
        
        # 2. Generate tweets based on trends
        logger.info("Step 2: Generating tweets...")
        tweets = generate_tweets(patterns)
        
        if not tweets:
            logger.error("No tweets generated. Exiting.")
            return
        
        # Add trending hashtags to tweets
        for tweet in tweets:
            if len(tweet['text']) < 250:  # Only add hashtags if there's room
                tweet['text'] += f" {hashtags[0]}"
        
        logger.info(f"Generated {len(tweets)} tweets")
        for i, tweet in enumerate(tweets, 1):
            logger.info(f"Tweet {i} ({tweet['type']}): {tweet['text'][:100]}...")
        
        # 3. Post tweets with delays
        logger.info("Step 3: Posting tweets...")
        posted_tweets = post_multiple_tweets(tweets, delay_minutes=30)
        
        if not posted_tweets:
            logger.error("No tweets were posted successfully. Exiting.")
            return
        
        logger.info(f"Successfully posted {len(posted_tweets)} tweets")
        
        # 4. Wait and track metrics
        logger.info("Step 4: Waiting for engagement and tracking metrics...")
        time.sleep(300)  # Wait 5 minutes for initial engagement
        
        tweet_ids = [tweet['id'] for tweet in posted_tweets]
        metrics = track_multiple_tweets(tweet_ids)
        
        # Combine posted tweet data with metrics
        for i, tweet in enumerate(posted_tweets):
            if i < len(metrics):
                tweet.update(metrics[i])
        
        # 5. Optimize strategy for next run
        logger.info("Step 5: Optimizing strategy...")
        insights, hypothesis = optimize_strategy(posted_tweets)
        
        # 6. Save results for future analysis
        results = {
            'timestamp': datetime.now().isoformat(),
            'trends_used': patterns,
            'hashtags_used': hashtags,
            'tweets_posted': posted_tweets,
            'insights': insights,
            'hypothesis': hypothesis
        }
        
        # Log summary
        logger.info("=" * 50)
        logger.info("EXECUTION SUMMARY")
        logger.info("=" * 50)
        logger.info(f"Tweets posted: {len(posted_tweets)}")
        if insights:
            logger.info(f"Best tweet got {insights['best_tweet'].get('likes', 0)} likes")
            logger.info(f"Average engagement rate: {insights['avg_engagement_rate']}%")
            logger.info(f"Best performing type: {insights['best_performing_type']}")
        logger.info("=" * 50)
        
        return results
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        return None

def run_scheduled():
    """Function for scheduled runs"""
    logger.info("Running scheduled Twitter bot...")
    results = main()
    if results:
        logger.info("Scheduled run completed successfully")
    else:
        logger.error("Scheduled run failed")

if __name__ == "__main__":
    main()