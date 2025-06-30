import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_KEY = os.getenv("GEMINI_KEY")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Bot Configuration
MAX_TWEETS_PER_DAY = 10
TWEET_COOLDOWN_MINUTES = 30
ENGAGEMENT_THRESHOLD = 5  # Minimum likes before considering a tweet successful

# Validation
required_vars = [
    GEMINI_KEY, TWITTER_API_KEY, TWITTER_API_SECRET, 
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET, BEARER_TOKEN
]

if not all(required_vars):
    raise ValueError("Missing required environment variables. Check your .env file.")
