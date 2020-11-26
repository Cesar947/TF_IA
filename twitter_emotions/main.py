from os import pipe
import pygame	

import sys
import time 	
import random
import pygame.scrap as scrap
from pygame.locals import SCRAP_CLIPBOARD

from pygame.constants import KEYDOWN, K_LCTRL, K_g, K_v	
from models.app import App 
from models.button import EButton
from som.SOM import Som
from nlp.NLP_Pipeline import NlpPipeline
#initiate pygame
pygame.init()	

#display pygame
window = pygame.display.set_mode((700, 750))		#set width & height of display
pygame.display.set_caption("Twitter Sentpy")		#set window name
background_color = (255, 255, 255)

#PIPELINE
pipeline = NlpPipeline(open("twitter_emotions/nlp/tweets_dataset.txt", "r", encoding="utf8"))
pipeline.run_pipeline()
#SOM
som = Som(pipeline.bag_of_words, None, 15, 15, 0.4, 1000)
som.train()

programIcon = pygame.image.load('./twitter_emotions/assets/bot_icon.png')
newbtn = pygame.image.load('./twitter_emotions/assets/plusle_icon.png')
pygame.display.set_icon(programIcon)

app = App(window, pipeline, som)
new_btn = EButton(20,30, newbtn)
#game starts
while True:
    window.fill(background_color)
    #window.blit(bg, (0, 0))
    app.draw_app()
    new_btn.draw_button(window)
    pygame.display.update()	

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            sys.exit()
        app.search_text_write(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            app.search(pos)     
            app.click_button(pos)
            app.erase_text(pos)
            if new_btn.is_click(pos):
                app = App(window, pipeline, som)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                app.search_text_paste() 
     
        if event.type == pygame.MOUSEMOTION:
            app.over_button(pos)


