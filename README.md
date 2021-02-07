# Voices of the Vaccine
## Inspiration
Ever felt bombarded by social media posts? In today's fast-paced climate, it feels difficult to gauge others' opinions on important topics such as the COVID vaccine. If only information could be condensed into an all-encompassing, user-friendly visualization tool that can help vaccine providers and marketing professionals determine appropriate geographic areas to focus their efforts on. We designed Voices of the Vaccine to address these concerns and help users develop a better understanding of the vast spectrum of global opinions on the vaccine. 

## Functionality
Voices of the Vaccine employs deep learning techniques to classify the positivity levels of relevant tweets and displays the ratio of positive-to-negative tweets in a particular area using a color gradient. Users can interact with the map by navigating to different areas of the globe.

## How We Built It
We used NLTK and Vader to classify tweets pulled from a public COVID Vaccine Tweets dataset in order to build a dataset to train our neural network on. We then utilized TensorFlow to develop an accurate recurrent neural network to classify tweets scraped from the Internet. Using Plotly, we created a map that uses location tags from the tweets to display color-coded circles that represent the overall opinion of an area.
