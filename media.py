import pygame
from pygame.locals import *
import os
import sys

colors = {'white': (000, 000, 000),
          'W1':    (250, 235, 225),
          'black': (255, 255, 255),
          'red':   (255, 000, 000)}
ERROR_T = {'color': 'Not a color',
           'casilla': 'Not a casilla object'}


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('media', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    return image, image.get_rect()


def put_string(texto, screen, coord):
    font = pygame.font.Font(None, 16)
    text = font.render(texto, 1, colors['W1'])
    screen.blit(text, coord)


def put_text(texto, screen, coord):
    lines_list = texto.split('\n')
    i = 15  # Separación entre las lineas
    for lines in lines_list:
        put_string(lines.lstrip(), screen, coord)
        coord = (coord[0], coord[1]+i)
