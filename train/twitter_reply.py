# Made with modifications from https://github.com/nirholas/Get-Tweet-Replies-With-Python-Tweepy

from datetime import datetime as dt
import csv
import tweepy
import ssl

current_date = dt.now().strftime("%Y-%m-%d_%H:%M:%S")
ssl._create_default_https_context = ssl._create_unverified_context

# Access Credentials
with open("data/access.txt", "r") as acc:
    # consumer key & secret
    api_key = acc.readline().strip()
    api_secret = acc.readline().strip()
    # access token/key & secret
    access_key = acc.readline().strip()
    access_secret = acc.readline().strip()

# Authentication with Twitter
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# update these for the tweet you want to process replies to 
# 'name' = the account username and you can find the tweet id within the tweet URL
# note: tweet_id is preferably from a recent tweet.
name = 'F1'
tweet_id = '1546383285122506752'

replies=[]
# Iterate through most recent tweets directed at 'name'.
for tweet in tweepy.Cursor(api.search_tweets, q='to:'+name, result_type='recent').items(20):
    if hasattr(tweet, 'in_reply_to_status_id_str'):
        if (tweet.in_reply_to_status_id_str==tweet_id):
            replies.append(tweet)

file_path = f'data/raw/{current_date}.csv'

# Write to file (raw)
with open(file_path, 'w') as f:
    csv_writer = csv.DictWriter(f, fieldnames=('id', 'text'))
    csv_writer.writeheader()
    for tweet in replies:
        row = {'id': tweet.id, 'text': tweet.text.replace('\n', ' ')}
        csv_writer.writerow(row)
print(f"Program finished writing to: {file_path}\n")

with open('data/raw/raw_metadata.csv', 'a') as f:
    f.write(f'{file_path};{tweet_id};context;driver,team\n')