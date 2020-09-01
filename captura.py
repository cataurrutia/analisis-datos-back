# from __future__ import print_function
from pymongo import MongoClient
from flask import Flask
import tweepy
import json

MONGO_HOST = 'mongodb://localhost/twitterdb'

CONSUMER_KEY = "1l6Uaxb65mR6rqtvODXs1efB9"
CONSUMER_SECRET = "CZVDMzoweq35K7BdXiynEcqw9kE9iFQPMDQyOJ6T8eUqL4aj0h"
ACCESS_TOKEN = "702892689080115200-JANKXmIOyxk234nHqOwio9sSD213efz"
ACCESS_TOKEN_SECRET = "RyR8nnFdz1SQiS3D9QMd039pnpajsq41A5H21lAo3sWQt"

# WORDS = ['#bigdata', '#AI', '#datascience', '#machinelearning', '#ml', '#iot', 'DuocUC']
# WORDS = ['Biden', 'covid', 'Trump', 'democrats', 'Bernie', 'AOC']
# WORDS = ['climate change', 'global warming', 'climate tracking', 'climate action', 'pollution', 'co2 emissions ', 'greenhouse gas']
WORDS = ['Medioambiente', 'Chile', 'glaciares', 'cambioclimatico', 'Deshielo', 'calentamientoglobal']


# Class provided by tweepy to access the Twitter Streaming API.
class StreamListener(tweepy.StreamListener):

    def on_connect(self):
        # Connect to the Streaming API
        api = tweepy.API(auth)

        print("You are now connected to the streaming API.")

        # Testing connection by listing the home timeline
        # public_tweets = api.home_timeline()
        # for tweet in public_tweets:
        #   print(tweet.text)
        #   print("-------------------------tweet del timeline------------------------------")

    def on_error(self, status_code):
        # On error: display the error and status code
        print('An Error has occurred: ' + repr(status_code))
        return False

    def on_data(self, data):
        try:
            # Connects to mongoDB
            client = MongoClient(MONGO_HOST)

            # Use twitter_db database. If it doesn't exist, it will create it.
            # db = client.pruebadb
            db = client.climateinfo

            # Decode JSON from Twitter
            raw_data = json.loads(data)

            # Select features
            id_str = raw_data['id_str']
            username = raw_data['user']['screen_name']
            created_at = raw_data['created_at']
            tweet = raw_data['text']
            retweet_count = raw_data['retweet_count']
            if raw_data['place'] is not None:
                place = raw_data['place']['country']
                print(place)
            else:
                place = None
            location = raw_data['user']['location']

            # Save filtered tweets in dictionary
            tweet_info = {
                "id_str": id_str,
                "username": username,
                "created_at": created_at,
                "tweet": tweet,
                "retweet_count": retweet_count,
                "place": place,
                "location": location
            }

            # Print out a message to the screen that we have collected a tweet
            print("Tweet creado el: " + str(created_at))

            # Insert data into mongoDB in a collection called filtered_tweets
            # If filtered_tweets doesn't exist, it will create it.
            db.filtered_tweets.insert_one(tweet_info)

            # Save full raw data from tweets
            # db.raw_tweets.insert_one(raw_data)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    # Tweepy authentication
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Set up the StreamerListener. The 'wait_on_rate_limit=True' for the Twitter API rate limit, so we don't get banned.
    listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))

    # Set up the Stream from tweepy
    stream = tweepy.Stream(auth=auth, listener=listener)

    print("Utilizando las palabras: " + str(WORDS))

    stream.filter(track=WORDS)
