# F1-sentiment-analysis
Understanding the Internet's Opinions on Formula 1\n
by Givarrel Veivel
-----
### WORK IN PROGRESS

Problem statement: On the internet, it's much easier to pay attention to either toxicity & hate, or notions that only reflect our own (confirmation bias). This project looks at the data more objectively to understand Reddit & Twitter's sentiment on different Formula 1 drivers as time goes by. This project also strives to make sense of what counts as negative or positive sentiment, as well as see how that sentiment changes over the course of an F1 season.

This is a TEXT CLASSIFICATION and OPINION MINING project, where data is retrieved from replies under official @F1 tweets (and possibly Reddit comments in the future). Each tweet will be classified based on topic (the driver or team they are talking about), and then we will label the tweet's sentiment (positive vs negative opinion).

-----
### PIPELINE
(1) Pull replies from tweet -> (2) Label topic -> (3) Label opinion/sentiment -> (4) Clean text content of tweets -> (5) Train model -> ..

- need to combine 2 & 3 and streamline the process
- continue 4 & 5, try huggingface bert