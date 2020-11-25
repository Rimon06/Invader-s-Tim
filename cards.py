import pygame
import media
import random

MOVE = "move"
ATTACK = "attack"
DEFENSE = "defense"
MOONSHOT = "moonshot"
TYPECARD = [MOVE, ATTACK, DEFENSE, MOONSHOT]


class card():
    def __init__(self, type=None):
        self.image, self.rect = media.load_png("card.png")
        self.type = type
        self.rect.topleft = (0, 0)
        self.grab = False
        self.used = False
        self.x2 = pygame.transform.scale(self.image, (self.rect.width*5//2, self.rect.height*5//2))
        self.rect = self.x2.get_rect()

    def show(self, screen, coord=(0, 0)):
        self.rect.topleft = (coord[0], coord[1])
        # Agarra la carta, si la suelta vuelve a su posición normal
        self.grabbed()
        # Imprime la carta del doble del tamaño, y queda una carta encima de la otra

        screen.blit(self.x2, self.rect.topleft)

    def click(self):
        x, y = pygame.mouse.get_pos()

    def grabbed(self):
        x, y = pygame.mouse.get_pos()

        if not self.grab:
            if self.rect.collidepoint(x, y) and pygame.mouse.get_pressed()[0]:
                self.dx, self.dy = x-self.rect.left, y-self.rect.top

                self.grab = True
        elif pygame.mouse.get_pressed()[0]:
            self.rect.topleft = x-self.dx, y-self.dy
        else:
            self.grab = False

    def action(self):
        pass


class deck():
    def __init__(self, number):
        self.cards = []
        for n in range(number):  # Agrega cartas al mazo
            self.cards.append(card(n))
        self.cards.reverse()
        self.number = number
        self.showing = []
        self.limit_show = 3
        self.put_to_show()

    def show(self, screen, offset):
        # Colocarlo en una posicion especifica del grid
        i = 0
        for cards in self.showing:
            cards.show(screen, (offset[0]+i*cards.rect.width+20, offset[1]+20))
            media.put_string(f'{cards.type}', screen, cards.rect.midbottom)
            i += 1
        i = 0
        for cards in self.cards:
            cards.show(screen, (offset[0]-40, 20+offset[1]-i))
            i += 1
            media.put_string(f'{cards.type}', screen, cards.rect.midbottom)

    def shuffle(self):
        random.shuffle(self.cards)

    def put_to_show(self, num=20):
        '''pone todas las cartas que pueda del mazo a la mano
        num:limita la cantidad de cartas.
        Si no hay valor de num pone todas las que pueda en la mano'''
        x = 0
        while len(self.cards) > 0 and len(self.showing) < self.limit_show and x < num:
            carta = self.cards.pop()  # Saca la primera carta que se muestra
            self.showing.append(carta)
            x += 0

    def take_card(self):  # Usar ratón para quitar cartas
        if len(self.showing) != 0:
            self.showing.pop()
