from pymongo import MongoClient
import pdmongo as pdm
import pandas as pd
import numpy as np
import re

from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS

MONGO_HOST = 'mongodb://localhost/twitterdb'


class TweetObject:
    # connection
    def connect_mongo(self):
        try:
            client = MongoClient(MONGO_HOST)

            # db = client.pruebadb
            db = client.climateinfo

            # Store info from "filtered_stream" collection into pandas dataframe
            df = pdm.read_mongo("prepared_tweets", [], db)
            print(df.dtypes)
            return df

        except Exception as e:
            print(e)

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
            exclusion_list = ['[^a-zA-Z]', 'rt', 'http', 'co', 'RT', 'x']
            exclusions = '|'.join(exclusion_list)

            text = re.sub(exclusions, ' ', df['tweet'][i])
            text = text.lower()

            words = text.split()
            words = [word for word in words if not word in stopword_list]

            # Fill up columns with cleaned tweets and data length
            df.loc[:, 'clean_tweets'][i] = ' '.join(words)

        df.loc[:, 'len'] = np.array([len(tweet) for tweet in df['clean_tweets']])

        result = Counter(" ".join(df["clean_tweets"]).split()).most_common(50)
        print(result)

        result_df = pd.DataFrame(result, columns=['Palabra', 'Frequencia']).set_index('Palabra')
        print(result_df)

        # save clean tweets to new collection
        # db.new_collection.insert_one(df)

        # print(df)

        return df


if __name__ == '__main__':
    t = TweetObject()

    data = TweetObject.connect_mongo(t)
    data = t.clean_tweets(data)
