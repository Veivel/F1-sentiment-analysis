import copy
import pandas as pd
import os
import re
import string
from datetime import datetime as dt

current_date = dt.now().strftime("%Y-%m-%d_%H:%M:%S")
    
raw_file = 'train/data/raw/2022-07-29_15:55:48.csv'
data = pd.read_csv(raw_file, header=0)

DRIVERS = pd.read_csv('train/data/metadata/2022-drivers-v2.csv', delimiter=';')
TEAMS = pd.read_csv('train/data/metadata/2022-teams.csv', delimiter=';')
DRIVER_NICKS = [nickname for row in DRIVERS['nicknames'] for nickname in row.split(",")]
TEAM_NICKS = [nickname for row in TEAMS['nicknames'].values for nickname in row.split(',')]

def get_driver_name(word):
    driver = DRIVERS['nicknames'].loc[DRIVERS['nicknames'].str.contains(f"{word}")]
    return driver.str.split(',').values[0][0]

labels = []
data_copy = copy.deepcopy(data)
for i, row in data_copy.iterrows(): # Iterate through each tweet
    sentence = row['text']
    words = sentence.split(' ')
    category = set()
    
    for word in words: # Iterate through each word in a tweet
        word = re.sub('[^a-zA-Z ]', '', word).lower()
        if word in DRIVER_NICKS:
            category.add(get_driver_name(word))
            continue
        if word in TEAMS['nicknames'].values:
            category.add(word)
            continue
        
    #print(f'{category} --- {sentence:72}\n')
    if len(category) != 0:
        labels.append(sorted(list(category)))
    else:
        labels.append("[None]")
        
out = pd.DataFrame({"topic": labels, "id": data['id'], "text": data['text']})
name = raw_file.split('/')[-1]
out.to_csv(f'train/data/topic-labeled/t_{name}', index=False)
print(f"Successfully written to t_{name}\n")
