from pymongo import MongoClient
import pdmongo as pdm

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


if __name__ == '__main__':
    t = TweetObject()
    data = TweetObject.connect_mongo(t)
