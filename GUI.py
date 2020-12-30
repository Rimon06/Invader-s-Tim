import pygame
# import scene
# import character
import media


class Table(object):
    def __init__(self, player, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.surface = pygame.Surface((w, h))
        self.surface.set_colorkey((0, 0, 0))

    def show_info(self, screen):
        self.surface.fill((240, 120, 0))
        media.put_text(self.words, self.surface, (10, 10))
        screen.blit(self.surface, self.rect)


class pantalla(object):

    def __init__(self, player, screen, grid):
        self.player = player
        self.screen = screen
        self.grid = grid
        # Establecer Tablero en el centro
        self.grid.rect_table.center = (self.screen.get_rect().center)
        self.grid.moving_rects()
        # Creación de la mesa de cartas
        W = self.screen.get_width()
        H = self.screen.get_height()-self.grid.rect_table.bottom
        x = 0
        y = self.grid.rect_table.bottom
        self.table_cards = Table(self.player, x, y, W, H)  # Hands
        print(x, y, W, H)
        # Creación de la hoja de información
        W = (self.screen.get_width()-self.grid.rect_table.width)//2 - 20
        H = self.grid.rect_table.height
        x = self.grid.rect_table.right+10
        y = self.grid.rect_table.top
        self.info = Table(self.player, x, y, W, H)
        print(x, y, W, H)
        self.info.words = ''
        self.type_showed = None  # type of object selected
        self.show = False

        # Tomar en cuenta el botón para avanzar de turno
        # Realizar marco
        pass

    def draw_things(self):
        '''# TODO:
                - Dibujar barra moonshot
        '''
        self.grid.draw(self.screen)
        self.draw_cards_hand()  # Revisar para usar el draw de las cartas
        self.showing_info()

    def draw_cards_hand(self):
        self.Cards_Hand = self.player.deck.showing  # cartas en mano
        self.player.deck.draw(self.screen, self.table_cards.rect.center)
        for card in self.Cards_Hand:
            if card.grab:
                pygame.draw.rect(self.screen, (255, 0, 0), card.rect, 2)

    def Mouse_sets(self):
        mouse = self.grid.CHECK_mouse()  # gets the casilla coord
        if mouse is not None:
            self.type_showed = self.grid[mouse]
        else:
            for card in self.Cards_Hand:  # Checks in cards in Hand
                if card.mouse_in_card():
                    self.type_showed = card
                    break
            else:
                self.type_showed = None
            self.type_showed
        # M_Px, M_Py = pygame.Mouse.get_pos()
        pass

    def Get_Info_from(self):
        # Mouse intersect an casilla with character or a card...
        self.Mouse_sets()
        if self.type_showed is not None:
            self.info.words = self.type_showed.show_data()
        else:
            self.info.words = '~'

    def showing_info(self):
        if not self.show:
            return
        self.Get_Info_from()
        self.info.show_info(self.screen)

        # Dibujar cuadro
        # Comparar si Showed es una carta o un personaje
        # Mostrar informacion del Showed
        pass
