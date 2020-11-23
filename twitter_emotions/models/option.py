import pygame
from models.component import Component

pygame.init()

pos = pygame.image.load('./twitter_emotions/assets/positive.png')
neg = pygame.image.load('./twitter_emotions/assets/negative.png')


class Option(Component):
    def __init__(self, i, x, y, width = pos.get_rect().width, height = pos.get_rect().height):
        Component.__init__(self, x, y, width, height)
        self.i = i
        if i == 1:
            self.asset = pos
        elif i == 2:
            self.asset = neg
        

    def draw_option(self, window):           
        window.blit(self.asset, (self.x, self.y))