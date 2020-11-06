from pymongo import MongoClient
import pdmongo as pdm
import pandas as pd

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

            print(df.head())
            print(df.dtypes)
            print(df['fecha'])
            print(df['id_region'])
            return df

        except Exception as e:
            print(e)

    def prueba_json(self):
        # data = request.args.get('data', type=int)

        data1 = pd.read_csv('csv/dictionaries.csv')
        data2 = pd.read_csv('csv/dictionaries2.csv')
        data3 = pd.read_csv('csv/dictionaries3.csv')

        # print(words)

        dict1 = data1
        dict2 = data2
        dict3 = data3


if __name__ == '__main__':
    t = TweetObject()
    # data = TweetObject.connect_mongo(t)
    t.prueba_json()
