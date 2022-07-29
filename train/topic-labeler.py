import copy
import sys
import pandas as pd
import os

raw_file = 'data/raw/2022-07-11_14:47:50.csv'
data = pd.read_csv(raw_file, header=0)

DRIVERS = pd.read_csv('data/metadata/2022-drivers.csv')
TEAMS = pd.read_csv('data/metadata/2022-teams.csv')

labels = []
data_copy = copy.deepcopy(data)
for i, row in data_copy.iterrows():
    sentence = row['text']
    if sentence == "": # TODO: this should be handled elsewhere....
        data.remove(sentence)
        continue
    inputValid = False
    
    print("===== "*8)
    print(f"Label the subject topic of the following tweets.")
    print("Enter 'STOP' to exit.")
    print("Example: 'Charles is spectular!' -> 'LEC' // 'Ferrari engines again...' -> 'Ferrari'")
    print("\nTweet:")
    print(sentence)
    print("===== "*8)
    
    while (not inputValid):
        inp = input("Input: ")
        if inp in DRIVERS['code'] or TEAMS['team_name']:
            inputValid = True
            labels.append(inp)
        elif inp.lower() == "x":
            inputValid = True
            data.drop(labels=[i], inplace=True)
        elif inp == "STOP":
            inputValid = True
            print("Stopping program.")
            sys.exit()
        else:
            continue
    # os.system('cls||clear')

out = data.__deepcopy__()
out['topic'] = labels

name = raw_file.split('/')[-1]
out.to_csv(f'train/data/topic-labeled/t_{name}', index=False)

