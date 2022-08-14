# F1 SENTIMENT ANALYSIS
-----
Understanding the Internet's Opinions on Formula 1
<p> by Givarrel Veivel

![alt text](https://pbs.twimg.com/profile_banners/69008563/1659283314/1500x500)
-----
### WORK IN PROGRESS

**PROBLEM STATEMENT**: On the internet, it's much easier to pay attention to either toxicity & hate, or notions that only reflect our own (confirmation bias). This project looks at the data more objectively to REALLY unveil Reddit & Twitter's sentiment on different Formula 1 drivers, while also trying to make sense of the different factors of opinions in F1.

This is a TEXT CLASSIFICATION and OPINION MINING project, where data is retrieved from replies under official @F1 tweets (and possibly Reddit comments in the future). Each tweet will be classified based on topic (the subject driver or team), and then we will label the tweet's sentiment (positive vs negative opinion).

-----
### PIPELINE

(1) Pull replies from specified tweet -> (2) Label opinion/sentiment -> (3) Clean text content of tweets (for bag of words model)-> (4) Evaluate & train model -> (5) Test model on unlabeled data

-----
### TO-DO LIST
- Gather more training data (!!!)
- Implement BERT model
- Gather data from Reddit