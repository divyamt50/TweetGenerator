import logging
from collections import Counter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def optimize_strategy(tweet_feedback):
    """Analyze tweet performance and generate optimization insights"""
    if not tweet_feedback:
        return None, "No data available for optimization"
    
    # Find best performing tweet
    best_tweet = max(tweet_feedback, key=lambda x: x.get('likes', 0) + x.get('retweets', 0) * 2)
    
    # Analyze patterns
    avg_likes = sum(t.get('likes', 0) for t in tweet_feedback) / len(tweet_feedback)
    avg_engagement_rate = sum(t.get('engagement_rate', 0) for t in tweet_feedback) / len(tweet_feedback)
    
    # Identify successful tweet types
    type_performance = {}
    for tweet in tweet_feedback:
        tweet_type = tweet.get('type', 'unknown')
        if tweet_type not in type_performance:
            type_performance[tweet_type] = []
        type_performance[tweet_type].append(tweet.get('likes', 0))
    
    best_type = max(type_performance.keys(), 
                   key=lambda t: sum(type_performance[t]) / len(type_performance[t]))
    
    # Generate insights
    insights = {
        'best_tweet': best_tweet,
        'avg_likes': round(avg_likes, 2),
        'avg_engagement_rate': round(avg_engagement_rate, 2),
        'best_performing_type': best_type,
        'total_tweets_analyzed': len(tweet_feedback)
    }
    
    # Create hypothesis for next batch
    hypothesis = f"""
    Optimization Insights:
    - Best performing tweet type: {best_type}
    - Average engagement rate: {avg_engagement_rate:.2f}%
    - Focus on: {get_content_recommendations(best_tweet, best_type)}
    """
    
    logger.info(f"Strategy optimized. Best tweet got {best_tweet.get('likes', 0)} likes")
    return insights, hypothesis

def get_content_recommendations(best_tweet, best_type):
    """Generate content recommendations based on performance"""
    recommendations = {
        'hook': 'Strong opening statements with immediate value',
        'list': 'Numbered lists and actionable tips',
        'question': 'Engaging questions that encourage replies',
        'unknown': 'Authentic, conversational content'
    }
    return recommendations.get(best_type, 'Engaging, authentic content')