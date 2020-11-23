import pygame
from models.component import Component

pygame.init()

btn = pygame.image.load('./twitter_emotions/assets/clasificar_icon.png')
btn_sel = pygame.image.load('./twitter_emotions/assets/clasificar_icon_selected.png')

class Button(Component):
    def __init__(self, x, y, width = btn.get_rect().width, height = btn.get_rect().height):
        Component.__init__(self, x, y, width, height)
        self.asset = btn
        

    def draw_button(self, window):           
        window.blit(self.asset, (self.x, self.y))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] <self.y + self.height:
                self.asset = btn_sel
                return True
        self.asset = btn
        return False
        