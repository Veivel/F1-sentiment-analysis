from datetime import datetime as dt
import pandas as pd
import csv
import tweepy
import sched
import time
# import topic_classifier

DELAY_IN_MINUTES = 20

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
    """A synchronous object, used to pull a specific tweet's list of (recent) replies.
    Please ensure the original tweet is actually recent. Thanks.
    
    Made with modifications with: https://github.com/nirholas/Get-Tweet-Replies-With-Python-Tweepy"""
    
    def __init__(self, tweeter, tweet_id, max_iterations):
        self.file_path = f'train/data/raw/raw_{tweet_id}.csv'
        self.MAX_ITERATIONS = max_iterations
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
        ''' Write tweets to file_path and return file_path itself in string.'''
        if replies == None:
            replies = self.replies
        path  = self.file_path
        
        try: 
            existing_tweets = pd.read_csv(self.file_path, header=None)
            existing_ids = list(existing_tweets[0])
            mode = 'a'
        except:
            print("Raw file does note xist yet. Creating new one.")
            existing_ids = []
            mode = 'w'
        
        with open(path, mode) as f:
            csv_writer = csv.DictWriter(f, fieldnames=('id', 'text'))
            if not mode == 'a':
                csv_writer.writeheader()
            i = 0
            for tweet in replies:
                if not str(tweet.id) in existing_ids:
                    row = {'id': tweet.id, 'text': tweet.text.replace('\n', ' ')}
                    csv_writer.writerow(row)
                    i += 1
            
        print(f"Pulled {i} new tweets.")
        return path
    
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
    
    def write_to_file_path(self, df="none", file_path=None):
        if file_path == None:
            file_path = self.file_path
        if isinstance(df, str):
            try:
                self.tweets.to_csv(file_path, index=False, header=False)
            except:
                return f"Error writing to {file_path}. No args supplied, and self.tweets does not exist."
        else:
            df.to_csv(file_path, index=False, header=False)
        return f"written to {file_path}"

def main(sc=None, max_iterations=100):
    # update these for the tweet you want to process replies to 
    # 'name' = the account username and you can find the tweet id within the tweet URL
    # note: tweet_id is preferably from a recent tweet.
    name = 'F1' 
    tweet_id = '1557352816624246792'
    
    rep = replies_retriever(tweeter=name, tweet_id=tweet_id, max_iterations=max_iterations)
    replies = rep.pull_replies()
    path = rep.write_to_file_path(replies)
    # topic_classifier.main(path)
    
    if sc != None:
        sc.enter(DELAY_IN_MINUTES * 60, 1, main, (loop,)) # re enter loop

def search():
    s = searcher("ricciardo")
    twts = s.pull_tweets()
    msg = s.write_to_file_path(df=twts, file_path='test/data/ricciardo.csv')
    print(msg)

if __name__ == "__main__":
    print("\ntwitterer.py now running...")
    # loop = sched.scheduler(time.time, time.sleep)
    # loop.enter(DELAY_IN_MINUTES * 60, 1, main, (loop,))
    # loop.run()
    search()