#email : fachreyzaputra@gmail.com
import tweepy
import csv
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import time
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

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
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

# We create an extractor object:
extractor = twitter_setup()

# We create a trends list as follows:
indonesia = 23424846
trends = extractor.trends_place(id=indonesia)

for item in (trends[0]['trends']):
    print (item['name'])

date_since = "2020-09-07"

search_words = "#onepiece990"

new_search = search_words + " -filter:retweets"

tweets = tweepy.Cursor(extractor.search, q=new_search, lang="id", since=date_since).items(2000)

items = []
# for tweet in tweets:
#     while True:
#         try:
#             tweet = tweets.next()
#             items.append (' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split()))
#         except tweepy.TweepError:
#             time.sleep(60 * 15)
#             continue
#         except StopIteration:
#             break

for tweet in tweets:
    items.append (' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split()))

hasil = pd.DataFrame(data=items, columns=['Tweets Trend One Piece'])

#punc
def remove_punct(text):
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text

hasil['Tweet_punct'] = hasil['Tweets Trend One Piece'].apply(lambda x: remove_punct(x))

#token
def tokenization(text):
    text = re.split(r'\W+', text)
    return text

hasil['Tweet_tokenized'] = hasil['Tweet_punct'].apply(lambda x: tokenization(x.lower()))

#stopword
factory = StopWordRemoverFactory()
stopword = factory.get_stop_words()

def remove_stopwords(text):
    text = [word for word in text if word not in stopword]
    return text
    
hasil['Tweet_nonstop'] = hasil['Tweet_tokenized'].apply(lambda x: remove_stopwords(x))

#stem
factory_stem = StemmerFactory()
stemmer = factory_stem.create_stemmer()

def stemming(text):
    text = [stemmer.stem(word) for word in text]
    return text

hasil['Tweet_stemmed'] = hasil['Tweet_nonstop'].apply(lambda x: stemming(x))

print(hasil.head())

pos_list= open(r"kata_positif.txt")
pos_kata = pos_list.readlines()
neg_list= open(r"kata_negatif.txt")
neg_kata = neg_list.readlines()

a = []
items = hasil['Tweet_stemmed']
for kata in items:
    count_p = 0
    count_n = 0
    for kata_pos in pos_kata:
        if kata_pos.strip() in kata[0]:
            count_p +=1
    for kata_neg in neg_kata:
        if kata_neg.strip() in kata[0]:
            count_n +=1
    a.append(count_p - count_n)

hasil["value"] = a
print ("Nilai rata-rata Kata P-N pada Trend One Piece Chapter 990: "+str(np.mean(hasil["value"])))
print ("Standar deviasi Kata P-N pada Trend One Piece Chapter 990: "+str(np.std(hasil["value"])))
print ("Median Kata P-N pada Trend One Piece Chapter 990: "+str(np.median(hasil["value"])))

labels, counts = np.unique(hasil["value"], return_counts=True)
plt.bar(labels, counts, align='center')
plt.gca().set_xticks(labels)
plt.xlabel("Banyaknya Kata P-N")
plt.ylabel("Jumlah")
plt.title("Grafik Kata P-N pada One Piece Chapter 990")

plt.show()

hasil.to_csv(r"trend-onepiece.csv", index=False)