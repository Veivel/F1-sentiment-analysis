import copy
import pandas as pd
import os
import re
import string
from datetime import datetime as dt

current_date = dt.now().strftime("%Y-%m-%d_%H:%M:%S")
    
raw_file = 'train/data/topic-labeled/t_2022-07-29_15:55:48.csv'
data = pd.read_csv(raw_file, header=0)

l = len(data['text'])
labels = ['alonso'] * l

# out = pd.DataFrame({"topic": labels, "id": data['id'], "text": data['text']})
if 'topic' in data:
    print("Appending labels to existing topic column")
    existing = [item[2:-2] if item[0:5] == '[None]' else "" for item in data['topic'].values]
    print(labels, existing)
    data['topic'] = [','.join(topic) if topic[0] != "" else topic[1] for topic in zip(existing, labels)]
else:
    data['topic'] = labels
name = raw_file.split('/')[-1]
data = data[['topic','id','text']]
data.to_csv(f'train/data/topic-labeled/t_{name}', index=False)
print(f"Successfully written to t_{name}\n")