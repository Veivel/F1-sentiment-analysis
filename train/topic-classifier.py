import copy
import pandas as pd
import os
import re
import string
from datetime import datetime as dt

DRIVERS = pd.read_csv('train/data/reference/drivers-2022-v2.csv', delimiter=';')
TEAMS = pd.read_csv('train/data/reference/teams-2022.csv', delimiter=';')
DRIVER_NICKS = [nickname for row in DRIVERS['nicknames'] for nickname in row.split(",")]
TEAM_NICKS = [nickname for row in TEAMS['nicknames'].values for nickname in row.split(',')]

class auto_labeler:
    """This is NOT a machine learning model. This is just an algorithm."""
    
    def __init__(self, df):
        self.df = df
        pass
    
    @staticmethod
    def __get_name(word, dataframe):
        arr = dataframe['nicknames'].loc[dataframe['nicknames'].str.contains(f"{word}")]
        code = arr.str.split(',').values[0][0]
        
        return code
    
    @staticmethod
    def get_driver_name(word):
        """STATIC method to obtain driver name"""
        return auto_labeler.__get_name(word, DRIVERS)
    
    @staticmethod
    def get_team_name(word):
        """STATIC method to obtain team name"""
        return auto_labeler.__get_name(word, TEAMS)
    
    def classify_topics(self):
        self.labels = []
        df_copy = copy.deepcopy(self.df)
        for i, row in df_copy.iterrows(): # Iterate through each tweet
            sentence = row['text']
            words = sentence.split(' ')
            category = set()
            
            for word in words: # Iterate through each word in a tweet
                word = re.sub('[^a-zA-Z ]', '', word).lower()
                if word in DRIVER_NICKS:
                    category.add(auto_labeler.get_driver_name(word))
                    continue
                if word in TEAM_NICKS:
                    category.add(auto_labeler.get_team_name(word))
                    continue
            #print(f'{category} --- {sentence:72}\n')
            if len(category) != 0:
                self.labels.append(sorted(list(category)))
            else:
                self.labels.append("[None]")
                
    def write_to_file_path(self, raw):
        out = pd.DataFrame({"topic" : self.labels, 
                            "id"    : self.df['id'], 
                            "text"  : self.df['text']})
        file_path = raw.split('/')[-1]
        out.to_csv(f'train/data/topic-labeled/t_{file_path}', index=False)
        return f"Successfully written to t_{file_path}\n"
    
class label_iterator:
    # topic labeler manual
    def __init__(self):
        pass
    
class label_adder:
    # topic labeler py
    def __init__(self):
        pass
                
if __name__ == "__main__":
    raw = input("Insert raw file (relative path): ")
    try:
        f = open(raw)
    except FileNotFoundError:
        print(f"Cannot open file. File {raw} doesn't exist.")
    else:
        df = pd.read_csv(raw, header=0)
        auto = auto_labeler(df=df)
        auto.classify_topics()
        auto.write_to_file_path(raw)