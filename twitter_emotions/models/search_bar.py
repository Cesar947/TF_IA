
import pygame
import clipboard
from models.component import Component


pygame.init()

s_back = pygame.image.load('./twitter_emotions/assets/search_back.png')
s_back_sel = pygame.image.load('./twitter_emotions/assets/search_back_selected.png')
s_btn = pygame.image.load('./twitter_emotions/assets/search_button.png')
s_btn_sel = pygame.image.load('./twitter_emotions/assets/search_button_selected.png')

font = pygame.font.Font(None, 25)


class SearchBar(Component):
    def __init__(self, x, y, width = s_back.get_rect().width, height = s_back.get_rect().height):
        Component.__init__(self, x, y, width, height)
        self.asset = s_back
        self.button = s_btn
        self.search_text = ''
        self.clicked = False
        
    def draw_search_bar(self, window):           
        window.blit(self.asset, (self.x, self.y))
        window.blit(self.button, (self.x + 10, self.y + 8))
        s_text = font.render(self.search_text, 1, (0,0,0))
        window.blit(s_text, (self.x + 50, self.y + 10))

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
        self.search_text += event.unicode

    def paste_search_text(self):
        self.search_text = clipboard.paste()

    def space_search_text(self):
        self.search_text = self.search_text[:-1]
