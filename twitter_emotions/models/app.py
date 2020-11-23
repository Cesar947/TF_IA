import pygame

from models.option import Option
from models.search_bar import SearchBar
from models.toolbar import ToolBar
from models.button import Button
from models.tweet_detail import TweetDetail

class App():
    def __init__(self, window):
        self.window = window
        self.sbar = SearchBar(70,140)
        self.tbar = ToolBar(0,20)
        self.btn = Button(480,200)
        self.good_option = Option(1,200,400)
        self.bad_option = Option(2,400,400)
        self.searched = False
        self.tweet_detail = TweetDetail(210,260)

    def draw_app(self):
        self.sbar.draw_search_bar(self.window)
        self.tbar.draw_tool_bar(self.window)
        self.btn.draw_button(self.window)
        self.good_option.draw_option(self.window)
        self.bad_option.draw_option(self.window)
        if self.searched == True:
            self.tweet_detail.draw_tweet(self.window)

    def search(self, pos):
        self.sbar.is_clicked(pos)
        #self.sbar.not_clicked(pos)

    def search_text_write(self, event):
        self.sbar.write_search_text(event)

    def search_text_space(self, event):
        self.sbar.space_search_text(event)

    def search_text_paste(self):
        self.sbar.paste_search_text()

    def over_button(self, pos):
        self.btn.is_over(pos)

    def click_button(self, pos):
        self.btn.is_over(pos)
        self.tweet_detail.get_tweet("1330883685470572544")
        self.searched = True