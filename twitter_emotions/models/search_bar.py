
import pygame
import clipboard
from models.text_box import TextBox, username_settings
from models.button import EButton
from models.component import Component


pygame.init()

s_back = pygame.image.load('./twitter_emotions/assets/search_back.png')
s_back_sel = pygame.image.load('./twitter_emotions/assets/search_back_selected.png')
s_btn = pygame.image.load('./twitter_emotions/assets/search_button.png')
s_btn_sel = pygame.image.load('./twitter_emotions/assets/search_button_selected.png')

font = pygame.font.Font('./twitter_emotions/models/font_family/GothamNarrow-Light.otf', 18)
close_btn = pygame.image.load('./twitter_emotions/assets/close_btn.png')

class SearchBar(Component):
    def __init__(self, x, y, width = s_back.get_rect().width, height = s_back.get_rect().height):
        Component.__init__(self, x, y, width, height)
        self.asset = s_back
        self.button = s_btn
        self.c_btn = EButton(self.x + 535, self.y + 7, close_btn)
        self.text_box = TextBox(rect=(self.x + 40,self.y + 3,510,33), **username_settings)
        self.search_text = ''
        self.clicked = False
        self.image = pygame.Surface((510 ,39))
        
    def draw_search_bar(self, window):        
        window.blit(self.asset, (self.x, self.y))
        window.blit(self.button, (self.x + 10, self.y + 8))
        self.text_box.update()
        self.text_box.draw(window)
        if self.clicked == True:
            self.c_btn.draw_button(window)

    def is_clicked(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width - 80:
            if pos[1] > self.y and pos[1] <self.y + self.height:
                if self.clicked == False:
                    self.asset = s_back_sel
                    self.button = s_btn_sel
                    self.text_box.set_color((255,255,255))
                    self.clicked = True
                else:
                    self.asset = s_back
                    self.button = s_btn
                    self.text_box.set_color((235, 238, 240))
                    self.clicked = False
        
    def erase_text(self, pos):
        if self.c_btn.is_click(pos):
            self.text_box.set_buffer([])
            self.search_text = ''

    def write_search_text(self, event):
        self.text_box.get_event(event)

    def paste_search_text(self):
        self.search_text = clipboard.paste()
        self.text_box.set_buffer(self.search_text)

    def get_text(self):
        return self.search_text

    def space_search_text(self):
        self.search_text = self.search_text[:-1]

    def get_tweet_id(self):
        url = self.search_text.replace('?s=20', '')
        return url.split('/')[-1]
