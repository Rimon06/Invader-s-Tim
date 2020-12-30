# import pygame
# from character import Player


class SceneManager(object):
    def __init__(self, scene):
        self.go_to(scene)

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self


class Scene(object):
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError


class TurnManager(object):
    def __init__(self, group, grid):
        '''
        Recibe un grupo de personajes
        '''
        self.turnlist = group
        self.Ident = 0
        self.round = 0
        self.NextTurn(0)

    def NextTurn(self, next):
        '''
        Pasa el turno
        '''
        if self.Ident == len(self.turnlist)-1:
            self.round += 1
        self.Ident = (self.Ident+next) % len(self.turnlist)  # self.ident
        self.Actual = self.turnlist[self.Ident]

    def ActionTurn(self):
        if True:  # self.Actual.life > 0:
            return self.Actual.mov
            # if self.Actual is player:
            #     self.Actual.Waiting  # Turno del jugador
            # else:
            #     pass   # Turno de cada computadora. IA en juego
            # self.NextTurn(1)
        else:
            self.turnlist.pop(self.Ident)
            self.NextTurn(0)
