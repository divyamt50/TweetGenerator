import google.generativeai as genai
import os
import logging
import json
from dotenv import load_dotenv
from config import GEMINI_KEY

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_tweets(trend_patterns, previous_performance=None):
    """Generate tweets based on trending patterns and previous performance"""
    
    performance_context = ""
    if previous_performance:
        performance_context = f"""
        Previous performance insights:
        - Best performing tweet style: {previous_performance.get('best_style', 'Unknown')}
        - Average engagement: {previous_performance.get('avg_engagement', 0)} likes
        - Top keywords: {', '.join(previous_performance.get('top_keywords', []))}
        """
    
    prompt = f"""
    You are a viral tweet creator. Based on these trending patterns: {', '.join(trend_patterns)}
    {performance_context}
    
    Create exactly 3 tweets, each under 280 characters. Return ONLY the tweets without any formatting, code blocks, or extra text.
    
    Tweet 1: A hook-style tweet that grabs attention immediately
    Tweet 2: A list-style tweet with numbered tips or points
    Tweet 3: A question-style tweet that encourages engagement
    
    Requirements:
    - Modern, conversational tone
    - Include 1 relevant hashtag per tweet
    - Each tweet should be complete and ready to post
    - No markdown, no code blocks, no JSON
    - Each tweet on a separate line
    
    Just return the 3 tweets, one per line.
    """
    
    try:
        response = model.generate_content(prompt)
        logger.info("Successfully generated tweets with Gemini")
        
        # Clean the response text
        text = response.text.strip()
        
        # Remove code blocks if present
        if "```" in text:
            # Extract content between code blocks
            parts = text.split("```")
            for part in parts:
                if not part.strip().startswith(('json', 'python', 'javascript', '{')):
                    text = part.strip()
                    break
        
        # Split into lines and clean
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Remove any JSON-like content or formatting
        clean_lines = []
        for line in lines:
            if not line.startswith(('{', '}', '"', '[', ']', 'TWEET', 'Tweet')):
                if len(line) > 10 and not line.startswith('```'):  # Skip very short lines
                    clean_lines.append(line)
        
        # Create tweet objects
        tweets = []
        tweet_types = ["hook", "list", "question"]
        
        for i in range(min(3, len(clean_lines))):
            tweets.append({
                "type": tweet_types[i],
                "text": clean_lines[i][:280]  # Ensure character limit
            })
        
        # Ensure we have exactly 3 tweets
        while len(tweets) < 3:
            fallback_tweets = [
                {"type": "hook", "text": "The most underrated skill in 2025? Learning to say no to good opportunities so you can say yes to great ones. #Success"},
                {"type": "list", "text": "3 things that changed my mindset:\n1. Progress > Perfection\n2. Consistency > Intensity\n3. Systems > Goals #Growth"},
                {"type": "question", "text": "What's one belief you held 5 years ago that you've completely changed your mind about? #PersonalGrowth"}
            ]
            tweets.append(fallback_tweets[len(tweets)])
        
        # Validate tweet lengths and content
        valid_tweets = []
        for tweet in tweets[:3]:
            if 20 <= len(tweet['text']) <= 280:  # Reasonable length
                valid_tweets.append(tweet)
        
        if len(valid_tweets) < 3:
            logger.warning("Generated tweets were invalid, using high-quality fallbacks")
            return [
                {"type": "hook", "text": "Everyone talks about work-life balance, but what you really need is work-life harmony. Here's the difference... #WorkLife"},
                {"type": "list", "text": "5 micro-habits that compound:\n1. Read 10 pages daily\n2. Walk after meals\n3. Write 3 gratitudes\n4. Drink water first\n5. No phone for 1st hour #Habits"},
                {"type": "question", "text": "If you could master one skill instantly, what would it be and why? Drop your answer below! 👇 #Skills"}
            ]
        
        return valid_tweets
            
    except Exception as e:
        logger.error(f"Error generating tweets: {e}")
        return [
            {"type": "hook", "text": "The biggest lie we tell ourselves: 'I'll start tomorrow.' Tomorrow never comes. Start today, even if it's imperfect. #Motivation"},
            {"type": "list", "text": "4 rules for better decisions:\n1. Sleep on big choices\n2. Ask 'What would I regret not trying?'\n3. Consider the 10-10-10 rule\n4. Trust your gut #DecisionMaking"},
            {"type": "question", "text": "What's one small change you made that had a surprisingly big impact on your life? #LifeHacks"}
        ]