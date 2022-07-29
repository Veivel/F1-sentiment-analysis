import datetime as dt
from os import system
import tweepy
import pandas as pd

# OBSOLETE

MAX_NUM = 100
file_name = 'raw_george_russell'
keyword = 'George Russell'
#current_date = dt.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

# # Obtaining Credentials to access Twitter
# with open("data/access.txt", "r") as acc:
#     # consumer key & secret
#     api_key = acc.readline().strip()
#     api_secret = acc.readline().strip()
#     # access token/key & secret
#     access_key = acc.readline().strip()
#     access_secret = acc.readline().strip()
#     # bearer token
#     bearer = acc.readline().strip()

# # Initialize a Client object with the proper credentials
# client = tweepy.Client(
#     bearer_token        = bearer,
#     access_token        = access_key,
#     access_token_secret = access_secret,
#     consumer_key        = api_key,
#     consumer_secret     = api_secret
# )

# file_path = f'data/raw/{file_name}.csv'

try:
    existing_tweets = pd.read_csv(file_path, header=True)
    existing_tweets = list(existing_tweets['text'])
except:
    existing_tweets = list()
    with open(file_path, 'w') as file:
        file.write("id,text\n")

tweets, tweet_ids = list(), list()
# recent = client.search_recent_tweets(query=keyword, max_results=MAX_NUM)
    
# for item in recent[0]:
#     tweet = item.text.replace(",","")
#     if tweet not in existing_tweets and \
#         tweet not in tweets:
#         tweets.append(tweet)
#         tweet_ids.append(item.id)
# tweets = pd.DataFrame({'id': tweet_ids, 'text': tweets})

# Exporting Tweets
tweets.to_csv(file_path, index=False, header=False, mode='a')
