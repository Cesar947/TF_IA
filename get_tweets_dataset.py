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


# Palabras o textos buscados

#depressed
#sadness
#sad
#alone
#need help

# En items(600), el 600 es el número de tweets máximos para obtener
# Se realizaron varios intentos para completar el dataset al 100%, 
# puesto que no se llegaba al máximo de tweets con las búsquedas
for tweet in tweepy.Cursor(api.search, q="need help OR I'm depressed", lang='en', tweet_mode='extended').items(600):
    if ('RT @' not in tweet.full_text):
        textFile.write(tweet.full_text + "|%&|\n")





