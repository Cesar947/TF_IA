import pygame
from models.component import Component


pygame.init()

twitter_icon = pygame.image.load('./twitter_emotions/assets/twitter_icon.png')
set_icon = pygame.image.load('./twitter_emotions/assets/emoticons_icon.png')


font = pygame.font.Font(None, 25)


class ToolBar(Component):
    def __init__(self, x, y, width = 700, height = 200):
        Component.__init__(self, x, y, width, height)
        self.twitter_icon = twitter_icon
        self.set_icon = set_icon
        
    def draw_tool_bar(self, window):           
        window.blit(self.twitter_icon, (self.x+340, self.y+20))
        window.blit(self.set_icon, (self.x + 640, self.y+20))
