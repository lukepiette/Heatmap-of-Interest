#!/usr/bin/env python
# coding: utf-8

# In[52]:


import pygame
import time

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

display_width = 1800
display_height = 1000

gameDisplay=pygame.display.set_mode((display_width,display_height))

imgcircle=pygame.image.load("flash_img.jpg")
# imgcircle=pygame.transform.scale(imgcircle,(int(display_width/2),int(display_height/2)))
clock = pygame.time.Clock()
FPS = 60
ch = 1.0/15.0

def show_eye():
    count=0
    while True:
        count+=1
        t=time.time()

        if count%2:
            gameDisplay.blit(imgcircle,(0,0))
        else:
            gameDisplay.fill(black)
        pygame.display.update()

        j=ch-(time.time()-t)
        if j>0:
            time.sleep(j)
show_eye()

