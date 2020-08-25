import pdmongo as pdm
import re
import pandas as pd
import nltk
import numpy as np
import matplotlib.pyplot as plt
import os
import ssl

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
from pymongo import MongoClient

MONGO_HOST = 'mongodb://localhost/twitterdb'

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


class TweetObject():

    def connect_mongo(self):

        try:
            client = MongoClient(MONGO_HOST)

            # db = client.pruebadb
            db = client.climateinfo

            # Store info from "twitter_search" collection into pandas dataframe
            df = pdm.read_mongo("filtered_tweets", [], db)

            # print(df.head())
            return df

        except Error as e:
            print(e)

    # Clean raw tweets, remove stopwords, punctuation, lower case all, html and emoticons
    # This will be done using Regex, ? means option so colou?r matches both color and colour.

    def clean_tweets(self, df):
        # Preprocessing

        # stop = nltk.download('stopwords')
        stopword_list = stopwords.words('spanish')

        ps = PorterStemmer()

        # Create additional columns
        df['clean_tweets'] = None
        df['len'] = None

        # get rid of anything that isn't a letter
        for i in range(0, len(df['tweet'])):
            exclusion_list = ['[^a-zA-Z]', 'rt', 'http', 'co', 'RT']
            exclusions = '|'.join(exclusion_list)

            text = re.sub(exclusions, ' ', df['tweet'][i])
            text = text.lower()

            words = text.split()
            words = [word for word in words if not word in stopword_list]

            # only use stem of word
            # words = [ps.stem(word) for word in words]

            # Fill up columns with cleaned tweets and data length
            df.loc[:, 'clean_tweets'][i] = ' '.join(words)

        df.loc[:, 'len'] = np.array([len(tweet) for tweet in df['clean_tweets']])

        # save clean tweets to new collection
        # db.new_collection.insert_one(df)

        # print(df)

        return df

    # This function calculates sentiment on our cleaned tweets. Uses textblob to calculate polarity.
    # arg1: takes in a tweet (row of dataframe)

    def sentiment(self, tweet):

        # need to improve
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    # Save cleaned data to a csv for further analysis.

    def save_to_csv(self, df):

        try:
            df.to_csv("clean_tweets.csv")
            print("\n")
            print('CSV is NOT being saved yet hehehe')
            # print("csv successfully saved. Yaaaaaaaaay \n")

        except Error as e:
            print(e)

        return

    # Create wordcloud using mpl

    def word_cloud(self, df):
        # figu = plt()
        print('jejeje')

        text = " ".join(df['clean_tweets'])

        wordcloud = WordCloud(background_color='white').generate(text)
        # wordcloud = WordCloud(background_color='white', width=1000, height=800).generate(text)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('wordcloud.png')

        # plt.show()
        return


# tw = TweetObject()
# original_df = TweetObject.connect_mongo(tw)

# print(type(original_df))
# print(original_df)
# print(TweetObject.clean_tweets(tw, original_df))

if __name__ == '__main__':
    t = TweetObject()

    data = TweetObject.connect_mongo(t)

    data = t.clean_tweets(data)

    data['Sentiment'] = np.array([t.sentiment(x) for x in data['clean_tweets']])

    t.word_cloud(data)
    # t.save_to_csv(data)

    pos_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] > 0]
    neg_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] < 0]
    neu_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] == 0]
    tweet_count = data.shape[0]

    # Print results
    print("Positive tweets: {}%".format(100 * (len(pos_tweets) / len(data['clean_tweets']))))
    print("Negative tweets: {}%".format(100 * (len(neg_tweets) / len(data['clean_tweets']))))
    print("Neutral tweets: {}%".format(100 * (len(neu_tweets) / len(data['clean_tweets']))))
    print(f"De un total de: {tweet_count} tweets")
