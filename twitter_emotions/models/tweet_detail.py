from decouple import config
import tweepy
import pygame
import urllib.request
import io
from models.component import Component

consumer_key = config('TWITTER_API_KEY')
consumer_secret = config('TWITTER_API_SECRET_KEY')
access_token = config('TWITTER_ACCESS_TOKEN')
access_token_secret = config('TWITTER_ACCESS_TOKEN_SECRET')


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

pygame.init()

pos = pygame.image.load('./twitter_emotions/assets/positive.png')
neg = pygame.image.load('./twitter_emotions/assets/negative.png')

font_user = pygame.font.Font('./twitter_emotions/assets/font_family/GothamNarrow-Light.otf', 15)
font_name = pygame.font.Font('./twitter_emotions/assets/font_family/GothamNarrow-Medium.otf', 20)
font_text = pygame.font.Font('./twitter_emotions/assets/font_family/GothamNarrow-Book.otf', 20)

class TweetDetail(Component):
    def __init__(self, x, y, width = pos.get_rect().width, height = pos.get_rect().height):
        Component.__init__(self, x, y, width, height)
        self.tweet_text = ''
        self.tweet_user_name = ''
        self.tweet_user = ''
        self.tweet_user_image = ''
        self.file_image = None
        self.photo_profile = None

    def draw_tweet(self, window):           
        #window.blit(self.photo_profile, (self.x, self.y))
        self.image = pygame.Surface([200,200])
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, (0,0,0), (self.x + 20, self.y + 10), 23)
        #User
        user_text = font_name.render(self.tweet_user_name, 1, (0,0,0))
        window.blit(user_text, (self.x + 80, self.y))
        #User name
        name_text = font_user.render("@" + self.tweet_user, 1, (127,143,158))
        window.blit(name_text, (self.x + 80, self.y + 20))
        #Tweet text
        tweet_text = font_text.render(self.tweet_text, 1, (0,0,0))
        window.blit(tweet_text, (self.x, self.y+50))
        
    def get_tweet(self, tweet_id): 
        tweet = api.get_status(tweet_id)
        self.tweet_user_name = tweet.user.name
        self.tweet_user_image = tweet.user.profile_image_url
        self.tweet_user = tweet.user.screen_name
        self.tweet_text = tweet.text
        self.file_image = io.BytesIO(urllib.request.urlopen(self.tweet_user_image).read())
        self.photo_profile = pygame.image.load(self.file_image)






