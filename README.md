# F1 SENTIMENT ANALYSIS
-----
Understanding the Internet's Opinions on Formula 1
<p> by Givarrel Veivel

-----
### WORK IN PROGRESS

Problem statement: On the internet, it's much easier to pay attention to either toxicity & hate, or notions that only reflect our own (confirmation bias). This project looks at the data more objectively to REALLY unveil Reddit & Twitter's sentiment on different Formula 1 drivers, while also trying to make sense of the different factors of opinions in F1.

This is a TEXT CLASSIFICATION and OPINION MINING project, where data is retrieved from replies under official @F1 tweets (and possibly Reddit comments in the future). Each tweet will be classified based on topic (the subject driver or team), and then we will label the tweet's sentiment (positive vs negative opinion).

-----
### PIPELINE

(1) Pull replies from tweet -> (2) Label/classify topic -> (3) Label opinion/sentiment -> (4) Clean text content of tweets -> (5) Evaluate & train model -> (6) Test model on unlabeled data

- need to combine 2 & 3 and streamline the process
- continue 4 & 5, try huggingface bert