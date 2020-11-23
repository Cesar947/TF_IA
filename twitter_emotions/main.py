import pygame	

import sys
import time 	
import random
import pygame.scrap as scrap
from pygame.locals import SCRAP_CLIPBOARD

from pygame.constants import KEYDOWN, K_LCTRL, K_g, K_v	
from models.app import App 

#initiate pygame
pygame.init()	

#display pygame
window = pygame.display.set_mode((700, 700))		#set width & height of display
pygame.display.set_caption("Twitter Prediction")		#set window name
background_color = (255, 255, 255)
#bg = pygame.image.load('./twitter_emotions/assets/pokemon_pattern.png')

app = App(window)

#game starts
while True:
    window.fill(background_color)
    #window.blit(bg, (0, 0))
    app.draw_app()
    pygame.display.update()	

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            app.search(pos)    
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                app.search_text_paste()
            if event.key == pygame.K_BACKSPACE:
                app.search_text_space(event)
            #else:
            #    app.search_text_write(event)
            #app.search(pos)    
            
        if event.type == pygame.MOUSEMOTION:
            app.click_button(pos)


