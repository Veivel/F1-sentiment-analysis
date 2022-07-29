# Made with modifications from https://github.com/nirholas/Get-Tweet-Replies-With-Python-Tweepy

from datetime import datetime as dt
import pandas as pd
import csv
import tweepy
import ssl

# ssl._create_default_https_context = ssl._create_unverified_context
def get_credentials():
    creds = dict()
    with open("train/data/access.txt", "r") as acc:
        # consumer key & secret
        creds['api_key'] = acc.readline().strip()
        creds['api_secret'] = acc.readline().strip()
        # access token/key & secret
        creds['access_key'] = acc.readline().strip()
        creds['access_secret'] = acc.readline().strip()
        # bearer token
        creds['bearer_token'] = acc.readline().strip()
        
    return creds

def now():
    return dt.now().strftime("%Y-%m-%d_%H:%M:%S")

class replies_retriever:
    """A retriever of a specific tweet's list of (recent) replies.
    Please ensure the tweet is actually recent. Thanks."""
    
    def __init__(self, tweeter, tweet_id):
        current_date = now()
        self.file_path = f'train/data/raw/{current_date}.csv'
        self.MAX_ITERATIONS = 1000
        self.tweeter = tweeter
        self.tweet_id = tweet_id
        
        self.__auth()
        # self.replies = self.pull_replies()

    def __auth(self):
        """Method to obtain credentials from (gitinogred) access.txt,
        and then authenticate."""
        acc = get_credentials()
        # consumer key & secret
        self.__api_key = acc['api_key']
        self.__api_secret = acc['api_secret']
        # access token/key & secret
        self.__access_key = acc['access_key']
        self.__access_secret = acc['access_secret']
        
        # Authentication with Twitter
        auth = tweepy.OAuthHandler(self.__api_key, self.__api_secret)
        auth.set_access_token(self.__access_key, self.__access_secret)
        self.api = tweepy.API(auth)
        
        return "Authentication successful."
        
    def pull_replies(self):
        '''Obtain the replies from self.tweet_id'''
        replies=[]
        # Iterate through most recent tweets directed at 'name'.
        for tweet in tweepy.Cursor(self.api.search_tweets, q='to:'+self.tweeter, result_type='recent').items(self.MAX_ITERATIONS):
            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if (tweet.in_reply_to_status_id_str==self.tweet_id):
                    replies.append(tweet)
        return replies
    
    def write_to_file_path(self, replies=None):
        if replies == None:
            replies = self.replies
        path = self.file_path
        
        with open(path, 'w') as f:
            csv_writer = csv.DictWriter(f, fieldnames=('id', 'text'))
            csv_writer.writeheader()
            for tweet in replies:
                row = {'id': tweet.id, 'text': tweet.text.replace('\n', ' ')}
                csv_writer.writerow(row)

        with open('train/data/raw/log.csv', 'a') as f:
            f.write(f'{path};{self.tweet_id};context;driver,team\n')
            
        return f"Program finished writing to: {path}\n"
    
class searcher:
    """Retriever of tweets that match a specific search query.\n
    NOT USED & NOT 100% TESTED"""
    
    def __init__(self, keyword):
        current_date = now()
        self.file_path = f'train/data/raw/{current_date}.csv'
        self.MAX_SEARCHES = 100
        self.keyword = keyword
        self.__auth()
        # init Client
    
    def __auth(self):
        acc = get_credentials()
        # consumer key & secret
        self.__api_key = acc['api_key']
        self.__api_secret = acc['api_secret']
        # access token/key & secret
        self.__access_key = acc['access_key']
        self.__access_secret = acc['access_secret']
        # bearer token
        self.__bearer_token = acc['bearer_token']
        
        self.client = tweepy.Client(
        bearer_token        = self.__bearer_token,
        access_token        = self.__access_key,
        access_token_secret = self.__access_secret,
        consumer_key        = self.__api_key,
        consumer_secret     = self.__api_secret
        )
    
    def pull_tweets(self):
        tweets, tweet_ids = [], []
        recent = self.client.search_recent_tweets(
                    query = self.keyword, 
                    max_results = self.MAX_SEARCHES)
        for item in recent[0]:
            tweet = item.text # TODO: need replace comma?
            tweets.append(tweet)
            tweet_ids.append(item.id)
        df = pd.DataFrame({'id': tweet_ids, 'text': tweets})
        
        return df
    
    def write_to_file_path(self, df=None):
        if df == None:
            try:
                self.tweets.to_csv(self.file_path, index=False, header=False)
            except:
                return f"Error writing to {self.file_path}. You used no args, and self.tweets does not exist."
        df.to_csv(self.file_path, index=False, header=False)

if __name__ == "__main__":
    # update these for the tweet you want to process replies to 
    # 'name' = the account username and you can find the tweet id within the tweet URL
    # note: tweet_id is preferably from a recent tweet.
    name = 'F1'
    tweet_id = '1552950055493050372'
    
    rep = replies_retriever(tweeter=name, tweet_id=tweet_id)
    replies = rep.pull_replies()
    msg = rep.write_to_file_path(replies)
    
    print(msg)