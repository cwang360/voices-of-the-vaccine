import re, string
import pandas as pd
from nltk.corpus import twitter_samples
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

stop_words = stopwords.words('english')

covidData = pd.read_csv("cTP2.csv")

def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence


def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


cDTweets = covidData[["user_location", "text"]]

vaderDatar = pd.DataFrame(columns=["location","text", "sentiment"])

analyzer = SentimentIntensityAnalyzer()
for i in cDTweets.iterrows():
    try:
        vs = analyzer.polarity_scores(i[1][1])
        vDInsert = {"location": i[1][0], "text": i[1][1], "sentiment": vs["compound"]}
        vaderDatar.loc[i[0]] = vDInsert
    except TypeError:
        print("Float is not iterable but we do not care")
    print(i[0])

vaderDatar.to_csv("covidVD.csv")
print("to csv reached")
