import copy
import sys
import pandas as pd
import os

raw_file = 'train/data/topic-labeled/t_t_2022-07-29_15:55:48.csv'
data = pd.read_csv(raw_file, header=0)

labels = []
data_copy = copy.deepcopy(data)
for i, row in data_copy.iterrows():
    sentence = row['text']
    if sentence == "": # TODO: this should be handled elsewhere....
        data.remove(sentence)
        continue
    inputValid = False
    
    print("===== "*8)
    print(f"Label the sentiment of the following tweets.")
    print("Enter 'STOP' to exit.")
    print("0 : neutral / no sentiment\n1 : negative sentiment\n2 : positive sentiment\nX : erase this tweet")
    print(f"\nTweet about {data_copy['topic'][i]}:")
    print(sentence)
    print("===== "*8)
    
    while (not inputValid):
        inp = input("Input: ")
        if inp in ["0", "1", "2"]:
            inputValid = True
            labels.append(int(inp))
        elif inp.lower() == "x":
            inputValid = True
            data.drop(labels=[i], inplace=True)
        elif inp.lower() == "stop":
            inputValid = True
            print("Stopping program.")
            sys.exit()
        else:
            continue
    # os.system('cls||clear')

out = data.__deepcopy__()
out['sentiment'] = labels

name = raw_file.split('/')[-1]
out.to_csv(f'train/data/sentiment-labeled/s{name}.csv', index=False)
