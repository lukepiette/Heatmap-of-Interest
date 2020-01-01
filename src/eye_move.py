#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pygame,sys
import time,random
from pygame.sprite import Sprite
import struct
import socket
import codecs
import time
import sys

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

display_width = 1800
display_height = 1000

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Brain Controlled Snake")

imgcircle=pygame.image.load("imgcircle.png")
clock = pygame.time.Clock()
FPS = 60


def data_parse(data):
    data = data.strip("\n").split(", ")
    return(data)

def show_eye(data):
    '''
    Shows your eye as it tracks its location.
    '''

    gameDisplay.fill(black)
    x_cor = float(data[0])*display_width
    y_cor = float(data[1])*display_height-100
    gameDisplay.blit(imgcircle,(x_cor,y_cor))
    pygame.display.update()

    open('data/xy_coordinates','a').write(str((time.time(),int(x_cor),int(y_cor))))

while True:
    currTime = time.time()
    data = data_parse(sys.stdin.readline())
    show_eye(data)

pygame.quit()

