import pygame
from models.component import Component

pygame.init()

pos = pygame.image.load('./twitter_emotions/assets/positive.png')
neg = pygame.image.load('./twitter_emotions/assets/negative.png')
checkers =  pygame.transform.scale(pygame.image.load('./twitter_emotions/models/background.png'), (100,138))

class Option(Component):
    def __init__(self, i, x, y, width = pos.get_rect().width, height = pos.get_rect().height):
        Component.__init__(self, x, y, width, height)
        self.i = i
        if i == 1:
            self.asset = pygame.transform.smoothscale(pos, (90,125))
        elif i == 2:
            self.asset =  self.asset = pygame.transform.smoothscale(neg, (90,125))
        

    def draw_option(self, window):           
        window.blit(self.asset, (self.x, self.y))

    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

    def increment(self, window):
        if self.i == 1: 
            self.asset = pos
        elif self.i == 2:
            self.asset = neg 
        window.blit(checkers, (self.x, self.y))
        window.blit(self.asset, (self.x - 10, self.y - 10))
        
    def change_opacity(self, window):
        x = 0
        while x < 300:
                y = 0
                while y < 300:
                        window.blit(checkers, (self.x, self.y))
                        y += 32
                x += 32
        self.asset = pygame.transform.smoothscale(self.asset, (72,100))   
        self.blit_alpha(window, self.asset, (self.x + 15, self.y + 15),128)