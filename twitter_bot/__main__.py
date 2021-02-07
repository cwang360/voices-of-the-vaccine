import tweepy
import re


consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET

# sentiment change over time?
# focus on people who want vaccine but can't get it? frustration towards getting vaccine or frustration towards vaccine itself
# or people who approve/disapprove of the vaccine

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth.secure = True
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

q = "vaccine"
tweetsPerQry = 40
fName = "tweets.txt"
sinceId = None

max_id = -1
maxTweets = 2000

tweetCount = 0

minLong = -125
maxLong = -70
minLat = 25
maxLat = 50
radius = "34.5mi"



print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    # while tweetCount < maxTweets:
    for i in range(minLat, maxLat):
        lat = i
        for j in range(minLong, maxLong):
            long = j
            geo = str(lat) + ","+str(long) + "," +radius
            print(geo)
            tweets = []
            # if tweetCount < maxTweets:
            try:
                new_tweets = api.search(q=q, lang="en", count=tweetsPerQry, tweet_mode='extended', geocode=geo)
                # if not new_tweets:
                #     print("No more tweets found")
                #     break
                if new_tweets:
                    print("new")
                    f.write(str(lat)+","+str(long)+":\n")
                    for tweet in new_tweets:
                        text = str(tweet.full_text.replace('\n', '').replace("\xe2\x80\x99", "\'").encode("utf-8"))+"\n"
                        f.write(text)

                    tweetCount += len(new_tweets)
                    print("Downloaded {0} tweets".format(tweetCount))
                    max_id = new_tweets[-1].id


            except tweepy.TweepError as e:
                print("some error : " + str(e))
                break

print("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))

def clean(tweet):

    tweet = re.sub(r'^RT[\s]+', '', tweet)
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r'&amp;', 'and', tweet)
    tweet = re.sub(r'@[A-Za-z0–9]+', '', tweet)

    tweet = str(tweet).replace(r'\xe2\x80\x99', '\'')
    tweet = tweet.replace(r'\xe2\x80\x9c', '\"')
    tweet = tweet.replace(r'\xe2\x80\x9d', '\"')
    tweet = re.sub(r'\\...', '', tweet)

    return tweet


def read_tweets(file_name):
    with open(file_name, 'r') as f:
        tweets = [clean(line.strip()) for line in f]
    f.close()
    return tweets

tweets = read_tweets(fName)
with open("cleaned_tweets.txt", 'w') as f:
    for t in tweets:
        f.write(t+"\n")
    f.close()
print("finished cleaning")
