import pygame
import scene
import character
import media


class Table(object):
    def __init__(self, player, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.surface = pygame.Surface((w, h))


class pantalla(object):
    def __init__(self, player, screen, grid):
        self.player = player
        self.screen = screen
        self.grid = grid
        # Establecer Tablero en el centro
        self.grid.inside_grid.center = self.screen.get_rect().center
        self.grid.moving_rects()
        # Creación de la mesa de cartas
        W = self.screen.get_width()
        H = self.screen.get_height()-self.grid.inside_grid.bottom
        x = 0
        y = self.grid.inside_grid.bottom
        self.table_cards = Table(self.player, x, y, W, H)

        # Creación de la hoja de información
        W = (self.screen.get_width()-self.grid.inside_grid.width)//2 - 20
        H = self.grid.inside_grid.height
        x = self.grid.inside_grid.right+10
        y = self.grid.inside_grid.top
        self.info = Table(self.player, x, y, W, H)
        self.info.words = 'aaa'
        self.Showed = None

    def draw_things(self):
        '''# TODO:
                - Dibujar barra moonshot
        '''
        self.grid.draw(self.screen)
        self.draw_cards_hand()  # Revisar para usar el draw de las cartas
        self.showing_info()

    def draw_cards_hand(self):
        '''ARREGLAR: cards in hand'''
        # cartas en mano
        self.Cards_Hand = self.player.deck.showing
        # objeto Rect para colocar las cartas en mano del jugador
        self.rect_cards = self.Cards_Hand[0].rect.union(
            self.Cards_Hand[len(self.Cards_Hand)-1].rect)

        self.rect_cards.center = self.table_cards.rect.center

        self.player.deck.show(self.screen, self.rect_cards.topleft)

    def showing_info(self):
        self.info.surface.fill((240, 120, 0))
        media.put_string(self.info.words, self.info.surface, (10, 10))
        self.screen.blit(self.info.surface, self.info.rect)

        # Dibujar cuadro
        # Comparar si Showed es una carta o un personaje
        # Mostrar informacion del Showed

        if self.Showed is None:
            return
