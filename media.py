import pygame
from pygame.locals import *
import os
import sys


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
    text = font.render(texto, 1, (250, 235, 225))
    screen.blit(text, coord)
