import pygame
import cards
import character
import media
import random

# -- Tipos de cartas --
MOVE = "move"
ATTACK = "attack"
DEFENSE = "defense"
MOONSHOT = "moonshot"
TYPECARD = [MOVE, ATTACK, DEFENSE, MOONSHOT]


class tup():
    def __init__(self):
        pass


class moving_card(cards.card):
    def __init__(self, player, gui):
        super(moving_card, self).__init__(MOVE)
        self.front, self.rect = media.load_png("move_card.png")
        self.player = player
        self.description = '''Move player 1 to 6 steps'''
        self.gui = gui

    def action(self):
        '''Aleatoriamente selecciona el numero de pasos
        el personaje se mueve en torno a esos pasos
        Se muestra los pasos que le faltan, lo que hace la carta'''
        if not self.used:
            self.STEPS = random.randint(1, 6)
            print("pasos", self.STEPS)
            self.road = []
            # self.copy = character.copy(self.player)
            self.used = True
        if len(self.road) <= self.STEPS:
            if self.gui.grid.movingchar(self.player, self.player.move()))
            # self.player.mov()

            # Copia una imagen del personaje
            # Escoge opciones validas, guarda el camino en la variable road
                pass
        for steps in self.road:
            # realizar animacióno
            # Esto es otro sitio????
            pass
