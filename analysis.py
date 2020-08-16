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
        print('Connect mongo: ')

        try:
            # Connect to mongo, to de db and to the col
            client = MongoClient(MONGO_HOST)
            # db = client.pruebadb
            db = client.climateinfo
            col = db.filtered_tweets

            print(client)
            print(db)
            print(col)

            # Save info from collection to pandas dataframe
            df = pdm.read_mongo("filtered_tweets", [], db)

            print('Tenemos el dataframe')
            print(df)
            return df

        except Error as e:
            pass
            # print(e)

    # Clean raw tweets, remove stopwords, punctuation, lower case all, html and emoticons
    # This will be done using Regex, ? means option so colou?r matches both color and colour.

    # def clean_tweets(self, df):
    #     # Preprocessing
    #
    #     stop = nltk.download('stopwords')
    #
    #     stopword_list = stopwords.words('english')
    #     ps = PorterStemmer()
    #     df["clean_tweets"] = None
    #     df['len'] = None
    #
    #     print(df)
    #
    #     # get rid of anything that isn't a letter
    #     for i in range(0, len(df['tweet'])):
    #
    #         exclusion_list = ['[^a-zA-Z]', 'rt', 'http', 'co', 'RT']
    #         exclusions = '|'.join(exclusion_list)
    #         text = re.sub(exclusions, ' ', df['tweet'][i])
    #         text = text.lower()
    #         words = text.split()
    #         words = [word for word in words if not word in stopword_list]
    #
    #         # only use stem of word
    #         words = [ps.stem(word) for word in words]
    #         df['clean_tweets'][i] = ' '.join(words)
    #
    #     # Create column with data length
    #     df['len'] = np.array([len(tweet) for tweet in df["clean_tweets"]])
    #     return df
    #
    # # This function calculates sentiment on our cleaned tweets. Uses textblob to calculate polarity.
    # # arg1: takes in a tweet (row of dataframe)
    #
    # def sentiment(self, tweet):
    #
    #     # need to improve
    #     analysis = TextBlob(tweet)
    #     if analysis.sentiment.polarity > 0:
    #         return 1
    #     elif analysis.sentiment.polarity == 0:
    #         return 0
    #     else:
    #         return -1
    #
    # # Save cleaned data to a csv for further analysis.
    #
    # def save_to_csv(self, df):
    #
    #     try:
    #         df.to_csv("clean_tweets.csv")
    #         print("\n")
    #         print("csv successfully saved. Yaaaaaaaaay \n")
    #
    #     except Error as e:
    #         print(e)
    #
    #     return
    #
    # # Create wordcloud using mpl
    #
    # def word_cloud(self, df):
    #     print('aentroooo')
    #     figu = plt.subplots(figsize=(12, 10))
    #     wordcloud = WordCloud(
    #         background_color='white',
    #         width=1000,
    #         height=800).generate(" ".join(df['clean_tweets']))
    #     figu.imshow(wordcloud)
    #     figu.axis('off')
    #     figu.show()
    #     return



# tw = TweetObject()
# original_df = TweetObject.connect_mongo(tw)

# print(type(original_df))
# print(original_df)
# print(TweetObject.clean_tweets(tw, original_df))

if __name__ == '__main__':
    t = TweetObject()

    data = TweetObject.connect_mongo(t)

    # data = t.clean_tweets(data)
    # print('------------------------------Yesssss-------------------------------------')
    #
    # data['Sentiment'] = np.array([t.sentiment(x) for x in data['clean_tweets']])
    #
    # print('holi')
    #
    # t.word_cloud(data)
    # t.save_to_csv(data)
    #
    # print('holi2')
    #
    # pos_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] > 0]
    # neg_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] < 0]
    # neu_tweets = [tweet for index, tweet in enumerate(data["clean_tweets"]) if data["Sentiment"][index] == 0]
    #
    # # Print results
    # print("percentage of positive tweets: {}%".format(100 * (len(pos_tweets) / len(data['clean_tweets']))))
    # print("percentage of negative tweets: {}%".format(100 * (len(neg_tweets) / len(data['clean_tweets']))))
    # print("percentage of neutral tweets: {}%".format(100 * (len(neu_tweets) / len(data['clean_tweets']))))