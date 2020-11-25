import pygame
import media


class casilla():
    def __init__(self, esx, esy, width, height, player=None):
        self.rect = pygame.Rect(esx, esy, width, height)
        self.player = player
        self.peso = 10 if self.player is not None else 0

    # Coloca a player en la casilla actual, y a la anterior le pone cero
    def agregar(self, player, casilla=None):
        if player is not None and self.peso < 10:
            self.player = player
            self.peso = 10
            if casilla is not None:
                casilla.player = None
                casilla.peso = 0

    def highlight(self):
        return (0, 255, 0)

    def show_data(self, screen, dim):
        '''Mover a GUI'''
        pygame.draw.rect(screen, (0, 255, 125), dim)
        media.put_string(self.player.name, screen, (dim[0]+5, dim[1]+5))


class grid():  # Agregarle la lista de tiles para las imagenes...
    def __init__(self, esx, esy, width, height, num):

        self.x, self.y = esx, esy  # Esquina superior izquierda del tablero

        self.width, self.height = width, height  # Dimensiones de una sola casilla

        self.num = num  # numero de casillas en una fila/columna del tablero
        self.mapa = dict()
        # Genera el grid de num filas x num columnas y los guarda en un diccionario que lee las casillas i con j
        for y in range(0, self.height*self.num, self.height):
            for x in range(0, self.width*self.num, self.width):
                i = x//self.width
                j = y//self.height
                self.mapa[i, j] = casilla(self.x+x, self.y+y, self.width, self.height)
        # rect() del tablero completo
        self.inside_grid = (self.mapa[0, 0].rect).union(self.mapa[self.num-1, self.num-1].rect)

    # Dibuja el tablero con una grilla de color negro
    def draw(self, screen):
        # dibuja el fondo del tablero
        pygame.draw.rect(screen, (255, 255, 255), self.inside_grid)
        # dibuja la grilla del tablero, separando cada casilla
        for cuadro in self.mapa.values():
            pygame.draw.rect(screen, (0, 0, 0), cuadro.rect, 1)
        # Probablemente mover a GUI.py
        highlighted = self.CHECK_mouse()
        if highlighted is not None:
            box = self.mapa[highlighted]
            pygame.draw.rect(screen, box.highlight(), box.rect, 1)
            if box.peso == 10 and pygame.mouse.get_pressed()[0]:
                dim = (self.inside_grid.right+20, self.inside_grid.top, 100, self.inside_grid.height)
                box.show_data(screen, dim)
        # Dibuja los jugadores en la casilla, si los hay
        for j in range(0, self.num):
            for i in range(0, self.num):
                player = self.mapa[i, j].player
                if player is not None:
                    self.putinmiddle(player, (i, j))
                    self.mapa[i, j].player.pos(screen)

    def moving_rects(self):
        '''Mueve todos los rects de las casillas '''
        dx = self.inside_grid.left - self.mapa[0, 0].rect.left
        dy = self.inside_grid.top - self.mapa[0, 0].rect.top
        for casilla in self.mapa.values():
            casilla.rect.move_ip(dx, dy)

    def CHECK_mouse(self):
        '''Mover esto a las cosas que detectará el GUI'''
        posMouse = pygame.mouse.get_pos()
        for casilla in self.mapa:
            if self.mapa[casilla].rect.collidepoint(posMouse):
                return casilla
        return None

    # Establece la posición del personaje en una de las casillas
    def putinmiddle(self, player, pos):
        player.rect.midbottom = self.mapa[pos].rect.center
        self.mapa[pos].agregar(player)

    def movingchar(self, player, pos):
        moveX, moveY = pos[0], pos[1]
        if moveX != 0:
            moveX //= abs(moveX)
        if moveY != 0:
            moveY //= abs(moveY)
        # Movimiento del jugador. Si se sale del tablero, dibujar
        prevx = player.Px, player.Py
        i = player.Px + moveX
        j = player.Py + moveY
        if i < 0 or i > self.num-1 or j < 0 or j > self.num-1 or (i == player.Px and j == player.Py):
            return False
        # Mueve el jugador de un espacio a otro
        # Probablemente cambiar por algo mas sencillo
        if self.mapa[i, j].peso < 10:
            self.mapa[i, j].agregar(player, self.mapa[player.Px, player.Py])
            player.Px, player.Py = i, j

        self.putinmiddle(player, (player.Px, player.Py))
        if prevx == (player.Px, player.Py):
            return False
        else:
            return True

        # def possiblemoves(self, )
