import pygame
import random
# from cards import Deck
import media
from cards import choice_type


class GameEntity():
    scenario = None  # Static attribute for all GameEntity classes that represents grid

    def __init__(self, name, nam_image):
        self.name = name
        self.img, self.rect = media.load_png(nam_image)
        self.set_pos((0, 0))

    def set_pos(self, pos):
        self.Px, self.Py = pos

    def get_pos(self):
        return (self.Px, self.Py)

    def into_scenario(self):
        '''include any Game Entity into Scenario's grid'''
        if self.scenario is not None:
            self.scenario.includ(self, self.get_pos())

    def random_setpos(self):
        if self.scenario is None:
            return

        t = 0
        while self.scenario[self.get_pos()].is_filled():
            pos = tuple(random.randint(0, self.scenario.num-1) for _ in range(2))
            self.set_pos(pos)
            t += 1
            if t > len(self.scenario):  # Intentar matar GameEntity
                break
        self.into_scenario()

    def draw(self, screen):
        screen.blit(self.img, self.rect.topleft)


class Character(GameEntity):
    def __init__(self, name, nam_image, life):
        GameEntity.__init__(self,  name, nam_image)
        # # deck_building
        # self.deck = Deck(self, 10, ¿gui?)

        # Vida del player
        self.life = life

    def move(self):
        pass


class Player(Character):
    def __init__(self):
        Character.__init__(self, "Tim", "Tim.png", life=3)
        # self.deck = cards.Deck(10)
        self.into_scenario()

    def move(self, road, actual):
        '''road is list of possible moves, actual is actual possible position
        returns tuple of:
        1 - tuple, pos of mouse
        2 - bool, if it is a valid move
        3 - bool, if mouse rightclicked
        '''
        pos = self.scenario.CHECK_mouse()  # Detects and return by the mouse a casilla
        i_can_move = self.scenario.Can_you_move(actual, pos)
        not_in_road = pos not in road
        click = pygame.mouse.get_pressed()[0]
        return pos, i_can_move and not_in_road, click

    def attack(self, mapa):
        XYcas = self.scenario.CHECK_mouse()  # detects and return a casilla
        if XYcas is None or XYcas == self.get_pos():
            return
        casilla = mapa[XYcas]

        # clicked in a casilla with character
        if pygame.mouse.get_pressed()[0] and casilla.have_character():
            return casilla.player
        return


class Enemy(Character):
    def __init__(self):
        Character.__init__(self, "Ghost", "SpaceGhost.png", life=2)
        self.random_setpos()
        self.Vx = 1
        self.Vy = 1

    def mov(self, key):
        self.Vx, self.Vy = 0, 0
        count = 0
        while True:
            x = random.choice([0, 1])
            if x:  # Se mueve horizontalmente
                self.Vx = random.choice([-1, 1])
                self.Vy = 0
            else:  # Se mueve Verticalmente
                self.Vx = 0
                self.Vy = random.choice([-1, 1])
            if self.scenario.movingchar(self, (self.Vx, self.Vy)) or count == 4:
                return True
            count += 1

    def respawn(self):
        pos = self.Px, self.Py
        self.scenario[pos].blank()
        self.__init__()


class Object_Scene(GameEntity):
    '''Object goes into scenary'''

    def __init__(self, name):
        ''''''
        GameEntity.__init__(self, name, name+'.png')


class Rock(Object_Scene):
    '''literally does nothing. neither move nor interact with users'''

    def __init__(self, pos):
        Object_Scene.__init__(self, 'rock')
        self.set_pos(pos)


class Card(Object_Scene):
    '''card that can be grabbed by Character objects to put in their decks'''

    def __init__(self):
        Object_Scene.__init__(self, 'card')
        self.random_setpos()

    def get(self):
        return choice_type()
        self.scenario.includ(self, (self.Px, self.Py))
