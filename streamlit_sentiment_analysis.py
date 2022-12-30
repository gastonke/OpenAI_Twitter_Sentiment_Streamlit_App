import openai
import tweepy
import datetime
import streamlit as st

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Replace YOUR_TWITTER_API_KEY, YOUR_TWITTER_API_SECRET, YOUR_TWITTER_ACCESS_TOKEN, and YOUR_TWITTER_ACCESS_TOKEN_SECRET with your Twitter API credentials
auth = tweepy.OAuth1UserHandler(
    "YOUR_TWITTER_API_KEY",
    "YOUR_TWITTER_API_SECRET",
    "YOUR_TWITTER_ACCESS_TOKEN",
    "YOUR_TWITTER_ACCESS_TOKEN_SECRET"
)

api = tweepy.API(auth)

st.title("Stock Sentiment Analysis")

# Get the stock symbol from the user
symbol = st.text_input("Enter the stock symbol:")

# Search Twitter for recent tweets that include the stock symbol
tweets = api.search_tweets(q="#" + symbol, lang="en", count=100)

# Use the OpenAI API to perform sentiment analysis on each tweet
sentiment_data = []
for tweet in tweets:
    # Only include tweets from the past 30 days
    if tweet.created_at > datetime.datetime.now() - datetime.timedelta(days=30):
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"Analyze sentiment of tweet: {tweet.text}",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the sentiment from the model's response
        sentiment = response["choices"][0]["text"].strip()
        sentiment_data.append({"tweet": tweet.text, "sentiment": sentiment})

# Display the sentiment data in a table
st.table(sentiment_data)
