import json
import time
import pandas as pd
import re
import tweepy
from pymongo import MongoClient

# Global variables
MONGO_HOST = 'mongodb://localhost/twitterdb'

CONSUMER_KEY = "Nc6WlmocGdQJzwqS1n3rqdFya"
CONSUMER_SECRET = "9go1rno2aum8zce5WMATxeXSO0wgA0u8YZv8qAnGRxWVZ94LFY"
ACCESS_TOKEN = "1301970143044677633-yYVYr5A02UcGfhSmdDsQwQjQ5wHvO1"
ACCESS_TOKEN_SECRET = "JmDEruY9gCIyZAwaeba7tbOAkLdGhIfAXnMjrGbYlapGs"

search_words = []


# Pausa para no sobrecargar de peticiones los servidores de twitter
def limit_handler(cursor):
    try:
        while True:
            yield cursor.next()
    except RateLimitError:
        time.sleep(1000)


# Load search words from csv
def search_terms():
    global search_words

    words = pd.read_csv('../csv/search_terms.csv')
    words = words['Tema']

    search_words = words.to_list()

    return search_words


# Class provided by tweepy to access the Twitter Streaming API.
class StreamListener(tweepy.StreamListener):

    # Connect to the Streaming API
    def on_connect(self):
        api = tweepy.API(auth)
        print("You are now connected to the streaming API.")

        # Testing connection by listing the home timeline
        # public_tweets = api.home_timeline()
        # for tweet in public_tweets:
        #   print(tweet.text)
        #   print("-------------------------tweet del timeline------------------------------")

    # On error display the error and status code
    def on_error(self, status_code):
        print('An Error has occurred: ' + repr(status_code))
        return False

    # When it finds a tweet
    def on_data(self, data):
        try:
            # Connects to mongoDB climateinfo, if it doesn't exist, it will create it.
            client = MongoClient(MONGO_HOST)
            db = client.climateinfo

            # Decode JSON from Twitter for each tweet
            raw_data = json.loads(data)

            # Select features
            t_id = raw_data['id']
            created_at = raw_data['created_at']
            tweet = raw_data['text']
            location = str(raw_data['user']['location'])

            print(type(tweet))

            # Save ONLY tweets from Chile to db
            if re.search('[Cc]hile', location) or re.search('[Rr]egi[óo]n', location) or re.search('[Cc][Hh][Ll]',
                                                                                                   location):
                # tweet = tweet.encode('utf-8')
                tweet = str(tweet)
                # Save filtered tweets in dictionary
                tweet_info = {
                    "id": t_id,
                    "created_at": created_at,
                    "tweet": tweet,
                    "location": location
                }

                # Insert data into mongoDB in a collection called filtered_stream
                # If filtered_stream doesn't exist, it will create it.
                db.filtered_stream.insert_one(tweet_info)

                # Print out a message to the screen that we have collected a tweet
                print("Tweet creado el: " + str(created_at))
                print(type(tweet))

        except Exception as e:
            print(e)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            pass


if __name__ == '__main__':
    # Set filter words
    search_terms()

    # Tweepy authentication
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Set up the StreamerListener. The 'wait_on_rate_limit=True' for the Twitter API rate limit, so we don't get banned.
    listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True))

    # Set up the Stream from tweepy
    stream = tweepy.Stream(auth=auth, listener=listener)

    print("Utilizando las palabras: " + str(search_words))

    stream.filter(track=search_words)

# BEARER_TOKEN = AAAAAAAAAAAAAAAAAAAAANxVHgEAAAAAUMC37BeQ%2F57ve%2BSXb%2FpXu5ldGsM%3Dj7BZeaoayMZOPU3gC49iM7RNQpllkRvdBA7dWtqqlX2Dl9lnMp
