import pygame
import media
from character import Character
from data_structure import dict_grid


# Probablemente abstraer una clase padre, como la clase Table del modulo GUI
class casilla():
    '''
Class casilla saves the character in the position Px, Py in the Grid
He may save the tile inside him
Attributes:
rect -> pygame.Rect object
MapX, MapY  -> coord reference/pos character
player -> character here
peso -> peso to referencing other object
    '''

    def __init__(self, esx, esy, width, height, x=0, y=0, player=None):
        self.rect = pygame.Rect(esx, esy, width, height)
        self.MapX = x
        self.MapY = y
        self.agregar(player)

# === Metodos para establecer al player en casilla === #
    def agregar(self, player):
        '''Place a character in this casilla'''
        if player is not None:
            self.player = player
            self.set_peso()
            player.set_pos(self.coords())
            self.middle()
        else:
            self.blank()

    def blank(self):
        '''Set casilla with no character'''
        self.player = None
        self.set_peso()

    def middle(self):
        '''Center character's rect in middle of casilla'''
        self.player.rect.midbottom = self.rect.center

    def set_peso(self):
        if self.have_character():
            self.peso = 10
        else:
            self.peso = 0

# ===    Metodos para mover    === #
    def move_from(self, previous):
        '''moves a character in this casilla from previous casilla'''
        assert type(previous) == casilla, media.ERROR_T['casilla']
        if not self:
            self.agregar(self.player)
            previous.blank()

    def move_to(self, next):
        next.move_from(self)

    def swap(self, other):
        assert type(other) == casilla, media.ERROR_T['casilla']
        p1 = self.player
        p2 = other.player
        self.agregar(p2)
        other.agregar(p1)

# === Metodos logicos === #
    def is_filled(self):
        return self.player is not None

    def __bool__(self):
        return self.is_filled()

    def have_character(self):
        return isinstance(self.player, Character)

# ===   Metodos de Embellecimiento   == #
    def highlight(self):
        return (0, 255, 0)

    def setbackground(self, color):
        assert type(color) == tuple and len(color) in (3, 4), media.ERROR_T['color']
        self.color = color

# ===  Metodos de Retorno   === #
    def show_data(self):
        '''Mover a GUI'''
        self.info = f'Posicion: ({self.MapX},{self.MapY})'
        if self:  # Have an GameEntity
            self.info += f'\nName: {self.player.name}'
            if self.have_character():  # Have a Character
                self.info += f'''\nLife: {self.player.life}'''
        return self.info

    def __repr__(self):
        return self.show_data()+f' {self.rect}'

    def sum_rect(self, other):
        '''return a Rect Object that is create by union of Rect of two casillas'''
        RECT = self.rect.union(other.rect)
        return RECT

    def coords(self):
        return (self.MapX, self.MapY)


class grid(dict_grid):  # Agregarle la lista de tiles para las imagenes...
    def __init__(self, esx, esy, width, height, num):
        # Atributos heredados: W, H, index, info attributes
        super(grid, self).__init__(num)
        self.x, self.y = esx, esy  # Esquina superior izquierda del tablero

        self.width, self.height = width, height  # Dimensiones de una sola casilla

        self.num = num  # numero de casillas en una fila/columna del tablero
        # Genera el grid de num filas x num columnas y los guarda en un diccionario que lee las casillas i con j
        for i, j in self:
            self[i, j] = casilla(self.x+i*self.width,
                                 self.y+j*self.height,
                                 self.width, self.height,
                                 i, j)
        self.rect_table = self[0, 0].sum_rect(self[self.H-1, self.W-1])

    # Dibuja el tablero con una grilla de color negro
    def draw(self, screen):
        # dibuja el fondo del tablero
        pygame.draw.rect(screen, (255, 255, 255), self.rect_table)
        # dibuja la grilla del tablero, separando cada casilla
        for cuadro in self.values():
            pygame.draw.rect(screen, (0, 0, 0), cuadro.rect, 1)

        # Probablemente mover a GUI.py
        highlighted = self.CHECK_mouse()
        if highlighted is not None:
            box = self[highlighted]
            pygame.draw.rect(screen, box.highlight(), box.rect, 1)

        # Dibuja los jugadores en la casilla, si los hay
        for j in range(self.W):
            for i in range(self.H):
                player = self[i, j].player
                if self[i, j]:  # Have an player (player is not None)
                    # self.putinmiddle(player, (i, j))
                    self[i, j].middle()
                    player.draw(screen)

    def moving_rects(self):
        '''Mueve todos los rects de las casillas '''
        dx = self.rect_table.left - self[0, 0].rect.left
        dy = self.rect_table.top - self[0, 0].rect.top
        for casilla in self.values():
            casilla.rect.move_ip(dx, dy)  # Metodo para mover el rect Y centrar el personaje

    def CHECK_mouse(self):
        '''Mover esto a las cosas que detectará el GUI'''
        posMouse = pygame.mouse.get_pos()
        for casilla in self:
            if self[casilla].rect.collidepoint(posMouse):
                return casilla
        return None

    # Mejorar las funciones de colocar y mover un personaje en una casilla.
    # Hacer más sencilla la función agregar de la clase casilla, para utilizar un método en esta clase
    # que implemente de mejor manera el intercambio

    def includ(self, player, pos):
        self[pos].agregar(player)

    def swap(self, pos1, pos2):
        cas1 = self[pos1]
        cas2 = self[pos2]
        cas1.swap(cas2)

    def Can_you_move(self, playerpos, next):
        vecino = self.neighbours(playerpos)
        valid_casilla = next in vecino and next is not None
        return valid_casilla and not self[next].is_filled()

    def neighbours(self, pos):
        i, j = pos
        moves = [(i+1, j), (i-1, j), (i, j-1), (i, j+1)]  # derecha, izquierda, arriba, abajo
        vecino = []
        for x, y in moves:
            if x < 0 or x > self.H-1 or y < 0 or y > self.W-1:
                vecino.append(None)
            else:
                vecino.append((x, y))
        return vecino
