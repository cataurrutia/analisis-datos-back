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
            return df

        except Exception as e:
            print(e)

    def prueba_json(self):
        # data = request.args.get('data', type=int)

        data1 = pd.read_csv('csv/dictionaries.csv')
        data2 = pd.read_csv('csv/dictionaries2.csv')
        data3 = pd.read_csv('csv/dictionaries3.csv')

        dict1 = data1.to_json(orient='index')
        dict2 = data2.to_json(orient='index')
        dict3 = data3.to_json(orient='index')

        print(dict1)
        print(dict2)
        print(dict3)


if __name__ == '__main__':
    t = TweetObject()
    # data = TweetObject.connect_mongo(t)
    t.prueba_json()
