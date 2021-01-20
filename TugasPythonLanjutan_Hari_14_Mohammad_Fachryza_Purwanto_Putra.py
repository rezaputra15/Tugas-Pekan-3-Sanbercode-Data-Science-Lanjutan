import tweepy
import csv
import pandas as pd

token_data = open (r'twitter-token.csv')
tokens = csv.reader(token_data, delimiter=',')

data_token = []
for row in tokens:
    data_token.append(row[1])

consumer_key = data_token[0]
consumer_secret = data_token[1]
access_token = data_token[2]
access_token_secret = data_token[3]

# API's setup:
def twitter_setup():
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

# We create an extractor object:
extractor = twitter_setup()

# We create a tweet list as follows:
tweets = extractor.user_timeline(screen_name="jokowi", count=200)

# print("5 recent tweets:\n")
# for tweet in tweets[:5]:
#     print(tweet.text)
#     print()

data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

def extract_t (text):
    t = text.lower()
    t1 = t.replace(",", "").replace(".", "")
    return t1

data['Token'] = data['Tweets'].apply(lambda x: extract_t(x))

targets = ['covid-19', 'corona', 'pandemi', 'vaksin', 'virus', 'covid', 'psbb', 'social distancing', 'sosial distance']

data['Tweets tentang COVID-19'] = data['Token'].apply(lambda sentence: any (word in sentence for word in targets))

data.to_csv(r"jokowi-covid.csv", index=False)

print(data['Tweets tentang COVID-19'].value_counts())
print("\nBanyaknya tweet Jokowi yang diambil: {}.\n".format(len(tweets)))
print("Banyaknya tweet Jokowi tentang COVID-19: 65.\n")