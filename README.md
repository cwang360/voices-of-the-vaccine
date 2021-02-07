# Voices of the Vaccine
![Image of Interactive Map](https://drive.google.com/file/d/1Uz4NO2J4TY6xEoI8Qx_C4BpnhjacDXAR/preview)
## Inspiration
Ever felt bombarded by social media posts? In today's fast-paced climate, it feels difficult to gauge others' opinions on important topics such as the COVID vaccine. If only information could be condensed into an all-encompassing, user-friendly visualization tool that can help vaccine providers and marketing professionals determine appropriate geographic areas to focus their efforts on. We designed Voices of the Vaccine to address these concerns and help users develop a better understanding of the vast spectrum of global opinions on the vaccine. 

## Functionality
Voices of the Vaccine employs deep learning techniques to classify the positivity levels of relevant tweets and displays the ratio of positive-to-negative tweets in a particular area using a color gradient. Users can interact with the map by navigating to different areas of the globe.

## How We Built It
We used NLTK and Vader to classify tweets pulled from a public COVID Vaccine Tweets dataset in order to build a dataset to train our neural network on. We then utilized TensorFlow to develop an accurate recurrent neural network to classify tweets scraped from the Internet. Using Plotly, we created a map that uses location tags from the tweets to display color-coded circles that represent the overall opinion of an area.

## In This Repository:
- **twitter-bot** contains the Python script that fetches Tweets and outputs a .txt file with lines of tweets grouped by latitude/longitude (tweets.txt), as well as a cleaned-up version of the tweets, removing unnecessary symbols (cleaned_tweets.txt)
- **sentiment-analysis** contains the Python script that trains a model with data from covidVD.csv* and uses the model to classify the sentiment of tweets from cleaned_tweets.txt. It outputs a csv (plotting_points.csv) containing Longitude, Latitude, average sentiment of tweets from that location, and the number of tweets from that location.
- **sentiment-analysis-model** contains the saved model from sentiment-analysis
- **plotter** uses Plotly and Dash to graph the data from plotting_points.csv on a map and display it on a web app.

*covidVD.csv contains tweets from a [Kaggle database](https://www.kaggle.com/kaushiksuresh147/covidvaccine-tweets/code) and corresponding sentiment values obtained by using [Vader](https://github.com/cjhutto/vaderSentiment)
