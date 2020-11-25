
import pygame
import clipboard
from models.text_box import TextBox, username_settings
from models.component import Component


pygame.init()

s_back = pygame.image.load('./twitter_emotions/assets/search_back.png')
s_back_sel = pygame.image.load('./twitter_emotions/assets/search_back_selected.png')
s_btn = pygame.image.load('./twitter_emotions/assets/search_button.png')
s_btn_sel = pygame.image.load('./twitter_emotions/assets/search_button_selected.png')

font = pygame.font.Font('./twitter_emotions/models/font_family/GothamNarrow-Light.otf', 18)


class SearchBar(Component):
    def __init__(self, x, y, width = s_back.get_rect().width, height = s_back.get_rect().height):
        Component.__init__(self, x, y, width, height)
        self.asset = s_back
        self.button = s_btn
        self.text_box = TextBox(rect=(self.x + 40,self.y + 3,510,33), **username_settings)
        self.search_text = ''
        self.clicked = False
        self.image = pygame.Surface((510 ,39))
        
    def draw_search_bar(self, window):        
        window.blit(self.asset, (self.x, self.y))
        window.blit(self.button, (self.x + 10, self.y + 8))
        self.text_box.update()
        self.text_box.draw(window)

    def is_clicked(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] <self.y + self.height:
                if self.clicked == False:
                    self.asset = s_back_sel
                    self.button = s_btn_sel
                    self.clicked = True
                else:
                    self.asset = s_back
                    self.button = s_btn
                    self.clicked = False

        
    def write_search_text(self, event):
        self.text_box.get_event(event)

    def paste_search_text(self):
        self.search_text = clipboard.paste()
        self.text_box.set_buffer(self.search_text)

    def space_search_text(self):
        self.search_text = self.search_text[:-1]

    def get_tweet_id(self):
        url = self.search_text.replace('?s=20','')
        return url.split('/')[-1]
