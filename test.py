from decouple import config
import tweepy
import csv

consumer_key = config('TWITTER_API_KEY')
consumer_secret = config('TWITTER_API_SECRET_KEY')
access_token = config('TWITTER_ACCESS_TOKEN')
access_token_secret = config('TWITTER_ACCESS_TOKEN_SECRET')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#results = api.search('I want to be alone', lang='en', count=10)
textFile = open('tweets_sad.txt', 'a', encoding='utf-8')
#q: query
#lang: language
#count: count
#results = :

for tweet in tweepy.Cursor(api.search, q='depressed OR sad OR sadness', lang='en', tweet_mode='extended').items(2000):
    if ('RT @' not in tweet.full_text):
        textFile.write(tweet.full_text + "|%&|\n")


#depressed
#sadness
#sad
#alone



