from decouple import config
import tweepy
import pygame
import pygame.freetype
import urllib.request
import emoji
import io
import os
from models.component import Component
from models.util import crop_image



consumer_key = config('TWITTER_API_KEY')
consumer_secret = config('TWITTER_API_SECRET_KEY')
access_token = config('TWITTER_ACCESS_TOKEN')
access_token_secret = config('TWITTER_ACCESS_TOKEN_SECRET')

pygame.freetype.init()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

fontdir = os.path.dirname(os.path.abspath (__file__))

pygame.init()

pos = pygame.image.load('./twitter_emotions/assets/positive.png')
neg = pygame.image.load('./twitter_emotions/assets/negative.png')

font = pygame.font.Font('./twitter_emotions/models/font_family/seguiemj.ttf', 18)

font_user = pygame.freetype.Font(os.path.join (fontdir, "font_family", "GothamNarrow-Light.otf"), 18, font_index=0, resolution=0, ucs4=False)
font_name = pygame.freetype.Font(os.path.join (fontdir, "font_family", "seguiemj.ttf"), 20, font_index=0, resolution=0, ucs4=False)
font_text = pygame.freetype.Font(os.path.join (fontdir, "font_family", "seguiemj.ttf"), 18, font_index=0, resolution=0, ucs4=False)

class TweetDetail(Component):
    def __init__(self, x, y, pipeline=None, som=None, width = pos.get_rect().width, height = pos.get_rect().height):
        Component.__init__(self, x, y, width, height)
        self.pipeline = pipeline
        self.som = som
        self.tweet_text = ''
        self.tweet_user_name = ''
        self.tweet_user = ''
        self.tweet_user_image = ''
        self.file_image = None
        self.photo_profile = None
        self.photo_profile2 = None

    def draw_tweet(self, window):     
        window.blit(self.photo_profile, (self.x, self.y))
        #User
        user_text, _ = font_name.render(self.tweet_user_name,  fgcolor=None, bgcolor=None, style=pygame.freetype.STYLE_DEFAULT, rotation=0, size=0)
        window.blit(user_text, (self.x + 55, self.y+5))
        #User name
        name_text, _ = font_user.render("@" + self.tweet_user, fgcolor=(127,143,158), bgcolor=None, style=pygame.freetype.STYLE_DEFAULT, rotation=0, size=0)
        window.blit(name_text, (self.x + 55, self.y + 28))
        #Tweet text
        self.blit_text(window, self.tweet_text, (self.x+5, self.y+70))
        
    def get_tweet(self, tweet_id): 
        tweet = api.get_status(tweet_id, tweet_mode='extended')
        self.tweet_user_name = tweet.user.name
        self.tweet_user_image = tweet.user.profile_image_url
        self.tweet_user = tweet.user.screen_name
        self.tweet_text = tweet.full_text
        """ print(self.tweet_text)
        print(self.pipeline.test_tweet_vectorization(self.tweet_text)) """
        result = self.som.singleClusterization(self.pipeline.test_tweet_vectorization(self.tweet_text))
        self.file_image = io.BytesIO(urllib.request.urlopen(self.tweet_user_image).read())
        mode, size, data = crop_image(self.tweet_user_image)
        self.photo_profile = pygame.image.fromstring(data, size, mode)


    def blit_text(self, surface, text, pos):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        x, y = pos
        for line in words:
            for word in line:
                word_surface , _ = font_text.render(word, fgcolor=None, bgcolor=None, style=pygame.freetype.STYLE_DEFAULT, rotation=0, size=0)
                word_width, _ = word_surface.get_size()
                if x + word_width >= 600:
                    x = pos[0]  # Reset the x.
                    y += 24  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += 24 # Start on new row.





