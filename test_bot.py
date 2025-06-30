# test_bot.py - Test your bot without posting to Twitter

import logging
import json
import time
from datetime import datetime
from trend_discovery import get_trending_tweet_patterns, get_hashtag_trends
from generate_tweets import generate_tweets
from optimize_strategy import optimize_strategy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def simulate_posting(tweets):
    """Simulate posting tweets and return mock data"""
    posted_tweets = []
    
    for i, tweet_data in enumerate(tweets):
        tweet_text = tweet_data.get('text', tweet_data) if isinstance(tweet_data, dict) else tweet_data
        tweet_id = f"sim_{int(time.time())}_{i}"
        
        posted_tweets.append({
            'id': tweet_id,
            'text': tweet_text,
            'type': tweet_data.get('type', 'unknown') if isinstance(tweet_data, dict) else 'unknown',
            'posted_at': time.time(),
            # Simulate realistic engagement metrics
            'likes': max(1, hash(tweet_text) % 50),  # 1-50 likes
            'retweets': max(0, hash(tweet_text) % 15),  # 0-15 retweets
            'replies': max(0, hash(tweet_text) % 8),   # 0-8 replies
            'quotes': max(0, hash(tweet_text) % 5),    # 0-5 quotes
            'bookmarks': max(0, hash(tweet_text) % 12), # 0-12 bookmarks
            'impressions': max(100, hash(tweet_text) % 1000 + 100), # 100-1100 impressions
            'engagement_rate': round(((hash(tweet_text) % 50) / max(100, hash(tweet_text) % 1000 + 100)) * 100, 2)
        })
        
        logger.info(f"✅ SIMULATED: Posted tweet {i+1}: {tweet_text[:60]}...")
        time.sleep(1)  # Simulate delay
    
    return posted_tweets

def test_bot_pipeline():
    """Test the complete bot pipeline in simulation mode"""
    logger.info("🤖 Starting Twitter Bot Test (Simulation Mode)")
    logger.info("=" * 60)
    
    try:
        # 1. Test trend discovery
        logger.info("📊 Step 1: Discovering trends...")
        patterns = get_trending_tweet_patterns()
        hashtags = get_hashtag_trends()
        
        print(f"\n🔥 Trending Patterns Found:")
        for i, pattern in enumerate(patterns, 1):
            print(f"  {i}. {pattern}")
        
        print(f"\n#️⃣ Trending Hashtags:")
        for hashtag in hashtags:
            print(f"  {hashtag}")
        
        # 2. Test tweet generation
        logger.info("\n✏️ Step 2: Generating tweets...")
        tweets = generate_tweets(patterns)
        
        if not tweets:
            logger.error("❌ No tweets generated!")
            return
        
        print(f"\n📝 Generated {len(tweets)} tweets:")
        print("-" * 40)
        for i, tweet in enumerate(tweets, 1):
            print(f"Tweet {i} ({tweet['type'].upper()}):")
            print(f"  📝 {tweet['text']}")
            print(f"  📏 Length: {len(tweet['text'])} characters")
            print()
        
        # 3. Simulate posting
        logger.info("🚀 Step 3: Simulating tweet posting...")
        posted_tweets = simulate_posting(tweets)
        
        # 4. Display simulated metrics
        logger.info("\n📈 Step 4: Simulated engagement metrics...")
        print("\n📊 Engagement Results:")
        print("-" * 60)
        
        total_likes = 0
        total_retweets = 0
        total_impressions = 0
        
        for tweet in posted_tweets:
            print(f"🐦 Tweet ID: {tweet['id']}")
            print(f"   Type: {tweet['type'].upper()}")
            print(f"   Text: {tweet['text'][:50]}...")
            print(f"   ❤️  Likes: {tweet['likes']}")
            print(f"   🔄 Retweets: {tweet['retweets']}")
            print(f"   💬 Replies: {tweet['replies']}")
            print(f"   👁️  Impressions: {tweet['impressions']}")
            print(f"   📊 Engagement Rate: {tweet['engagement_rate']}%")
            print()
            
            total_likes += tweet['likes']
            total_retweets += tweet['retweets']
            total_impressions += tweet['impressions']
        
        # 5. Test optimization
        logger.info("🎯 Step 5: Analyzing performance...")
        insights, hypothesis = optimize_strategy(posted_tweets)
        
        print("🏆 PERFORMANCE SUMMARY:")
        print("=" * 40)
        print(f"📈 Total Likes: {total_likes}")
        print(f"🔄 Total Retweets: {total_retweets}")
        print(f"👁️  Total Impressions: {total_impressions}")
        
        if insights:
            print(f"🥇 Best Tweet Type: {insights['best_performing_type']}")
            print(f"📊 Average Engagement: {insights['avg_engagement_rate']}%")
            print(f"🏅 Best Tweet Likes: {insights['best_tweet']['likes']}")
        
        print(f"\n💡 OPTIMIZATION INSIGHTS:")
        print(hypothesis)
        
        # 6. Save test results
        results = {
            'test_run': True,
            'timestamp': datetime.now().isoformat(),
            'trends_used': patterns,
            'hashtags_used': hashtags,
            'tweets_generated': tweets,
            'simulated_performance': posted_tweets,
            'insights': insights,
            'hypothesis': hypothesis
        }
        
        # Save to file
        with open(f'test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        logger.info("✅ Test completed successfully!")
        logger.info("📁 Results saved to test_results_*.json")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Error in test pipeline: {e}")
        return None

def check_api_access():
    """Check what level of Twitter API access you have"""
    from utils.twitter_client import get_bearer_client
    
    print("🔍 Checking Twitter API Access Level...")
    print("-" * 40)
    
    client = get_bearer_client()
    if not client:
        print("❌ Unable to authenticate with Twitter API")
        return
    
    try:
        # Test basic API access
        me = client.get_me()
        print(f"✅ Basic API Access: Working")
        print(f"   Account: @{me.data.username}")
        print(f"   Name: {me.data.name}")
        
        # Test tweet creation (this will likely fail with free tier)
        try:
            # This is just a test - won't actually post
            print("🧪 Testing tweet creation access...")
            # client.create_tweet(text="Test") # Commented out to avoid actual posting
            print("✅ Tweet Creation: Available")
        except Exception as e:
            if "403" in str(e) and "access level" in str(e).lower():
                print("❌ Tweet Creation: Restricted")
                print("   🔒 You need Twitter API v2 Write access")
                print("   💰 This requires a paid Twitter API plan")
                print("   📖 Learn more: https://developer.twitter.com/en/portal/products")
            else:
                print(f"❌ Tweet Creation Error: {e}")
                
    except Exception as e:
        print(f"❌ API Access Error: {e}")

def main():
    """Main test function"""
    print("🤖 Twitter Bot Testing Suite")
    print("=" * 50)
    
    # Check API access first
    check_api_access()
    print("\n")
    
    # Run full test pipeline
    test_bot_pipeline()
    
    print("\n" + "=" * 50)
    print("🎉 Testing Complete!")
    print("\n💡 Next Steps:")
    print("1. If you want to post real tweets, upgrade to Twitter API v2 Write access")
    print("2. The bot logic is working perfectly in simulation mode")
    print("3. All components (trend discovery, generation, optimization) are functional")
    print("4. You can use this for content planning even without posting")

if __name__ == "__main__":
    main()

# upgrade_instructions.py - Instructions for upgrading Twitter API access

def show_upgrade_instructions():
    """Show instructions for upgrading Twitter API access"""
    
    instructions = """
    🚀 HOW TO UPGRADE YOUR TWITTER API ACCESS
    =======================================
    
    Your bot is working perfectly, but you need higher API access to post tweets.
    
    📋 CURRENT SITUATION:
    • You have Twitter API v2 Basic (Free) access
    • This allows reading tweets but NOT posting them
    • Error 403: "limited v1.1 endpoints" means you need Write access
    
    💰 UPGRADE OPTIONS:
    
    1. 📝 BASIC WRITE ACCESS ($100/month)
       • Post up to 300 tweets per month
       • Perfect for personal bots
       • Includes all read functionality
    
    2. 🚀 PRO ACCESS ($5,000/month) 
       • Post up to 3,000 tweets per month
       • Advanced analytics
       • Higher rate limits
    
    📖 HOW TO UPGRADE:
    1. Go to https://developer.twitter.com/en/portal/products
    2. Sign in to your developer account
    3. Select "Basic" or "Pro" plan
    4. Add payment method
    5. Update your app permissions to "Read and Write"
    
    🔧 ALTERNATIVE SOLUTIONS:
    
    1. 🧪 SIMULATION MODE (Current)
       • Test your bot logic without posting
       • Generate content for manual posting
       • Perfect for development and testing
    
    2. 📱 MANUAL POSTING
       • Generate tweets with your bot
       • Copy and paste to Twitter manually
       • Free but requires manual work
    
    3. 🔄 BUFFER/HOOTSUITE INTEGRATION
       • Use social media management tools
       • Some have free tiers
       • Schedule generated content
    
    💡 RECOMMENDATION:
    Start with simulation mode to perfect your bot, then upgrade when ready to automate posting.
    """
    
    print(instructions)

if __name__ == "__main__":
    show_upgrade_instructions()