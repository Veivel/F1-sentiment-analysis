import praw

with open("train/data/access.txt", "r") as acc:
    # consumer key & secret
    content = [item.strip() for item in acc.readlines()]
    client_id = content[-4]
    client_secret = content[-3]
    user_name = content[-2]
    user_password = content[-1]

client = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=user_name,
    password=user_password,
    user_agent="Curiosity Scraper by u/ComfortableMacaroon6"
)

client.read_only = True
print(client.user.me())