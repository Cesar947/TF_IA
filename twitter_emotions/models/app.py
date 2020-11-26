import pygame
import os
from models.option import Option
from models.search_bar import SearchBar
from models.toolbar import ToolBar
from models.button import Button
from models.tweet_detail import TweetDetail
from nlp.NLP_Pipeline import NlpPipeline
from som.SOM import Som

class App():
    def __init__(self, window):
        self.window = window
        self.sbar = SearchBar(70,140)
        self.tbar = ToolBar(0,20)
        self.btn = Button(480,200)
        self.good_option = Option(1,200,550)
        self.bad_option = Option(2,400,550)
        self.searched = False
        cwd = os.getcwd() 
        files = os.listdir(cwd) 
        print("Files in %r: %s" % (cwd, files))
        self.pipeline = NlpPipeline(open("twitter_emotions/nlp/tweets_dataset.txt", "r", encoding="utf8"))
        self.pipeline.run_pipeline()

        #CREACION DE INSTANCIA SOM
        som = Som(self.pipeline.bag_of_words, None, 12, 6, 0.7, 1000)
        som.train()
        
        # Pasando el pipeline como parámetro al TweetDetail
        # TweetDetail: Clase en donde se realiza la extracción y muestra del tweet
        self.tweet_detail = TweetDetail(120,260, self.pipeline, som)
        self.tweet_id = ''
        self.clicked_bar = False

    def draw_app(self):
        self.sbar.draw_search_bar(self.window)
        self.tbar.draw_tool_bar(self.window)
        self.btn.draw_button(self.window)
        if self.searched == False:
            self.good_option.draw_option(self.window)
            self.bad_option.draw_option(self.window)
        if self.searched == True:
            self.tweet_detail.draw_tweet(self.window)
            self.good_option.change_opacity(self.window)
            self.bad_option.increment(self.window)

    def search(self, pos):
        self.sbar.is_clicked(pos)
        if self.clicked_bar == False:
            self.clicked_bar = True
        elif self.clicked_bar == True:
            self.clicked_bar = False

    def erase_text(self, pos):
        if self.clicked_bar == True:
            self.sbar.erase_text(pos)

    def search_text_write(self, event):
        if self.clicked_bar == True:
            self.sbar.write_search_text(event)

    def search_text_space(self, event):
        self.sbar.space_search_text(event)

    def search_text_paste(self):
        self.sbar.paste_search_text()

    def over_button(self, pos):
        self.btn.is_over(pos)

    def click_button(self, pos):
        if self.sbar.get_text() != '':
            self.btn.is_over(pos)
            self.tweet_id = self.sbar.get_tweet_id()
            self.tweet_detail.get_tweet(self.tweet_id)
            self.searched = True
