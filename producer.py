import praw
from confluent_kafka import Producer
from time import sleep
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import json

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the credentials from environment variables
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
user_agent = os.getenv('USER_AGENT')

# Instantiate the object with your client_id and client_secret
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Create a Kafka producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'default.topic.config': {'acks': 'all'}
}


# Initialize NLTK's sentiment analyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Initialize sentiment count dictionary
sentiment_count = {
    'positive': 0,
    'negative': 0,
    'neutral': 0
}

# Create a Kafka producer instance
producer = Producer(conf)

# Kafka topic
kafka_topic = 'soccer'
subreddit = reddit.subreddit('soccer')
for comment in subreddit.stream.comments():
     # Perform sentiment analysis using NLTK
    sentiment = sia.polarity_scores(comment.body)['compound']
    print(sentiment)

    # Update sentiment count
    if sentiment > 0.2:
        sentiment_count['positive'] += 1
    elif sentiment < -0.2:
        sentiment_count['negative'] += 1
    else:
        sentiment_count['neutral'] += 1
    
    producer.produce(kafka_topic, value=json.dumps(sentiment_count).encode('utf-8'))

    # Flush the producer buffer
    producer.flush()

    # Sleep for 1 second
    sleep(1)
