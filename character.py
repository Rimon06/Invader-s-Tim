import pygame
import random
import cards
import media


class GameEntity():
    def __init__(self, name, nam_image):
        self.name = name
        self.img, self.rect = media.load_png(nam_image)
        self.Px = 0
        self.Py = 0

    def mov(self):
        pass

    def pos(self, screen):
        pass


# Player
class player():
    def __init__(self, grid):
        self.img, self.rect = media.load_png("Candleman.png")
        self.name = "Tim"
        self.Px = 0  # Indice de su ubicación en el mapa
        self.Py = 0
        self.deck = cards.deck(10)
        grid.putinmiddle(self, (self.Px, self.Py))

    # def move (self,):
    #     pass
    def mov(self, key, grid):
        Vx, Vy = 0, 0
        if key == pygame.K_LEFT:
            Vx = -1
            Vy = 0
        elif key == pygame.K_RIGHT:
            Vx = 1
            Vy = 0
        elif key == pygame.K_UP:
            Vx = 0
            Vy = -1
        elif key == pygame.K_DOWN:
            Vx = 0
            Vy = 1
        return grid.movingchar(self, (Vx, Vy))

    def pos(self, screen):
        screen.blit(self.img, self.rect.topleft)

# def validmoves()


class Enemy():
    def __init__(self, grid):
        self.img, self.rect = media.load_png("SpaceGhost.png")
        self.Px, self.Py = 0, 0
        while grid.mapa[self.Px, self.Py].peso >= 10:
            self.Px = random.randint(0, grid.num-1)
            self.Py = random.randint(0, grid.num-1)
        grid.putinmiddle(self, (self.Px, self.Py))
        self.Vx = 1
        self.Vy = 1
        self.name = 'Ghost'

    def mov(self, key, grid):
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
            if grid.movingchar(self, (self.Vx, self.Vy)) or count == 4:
                return True
            count += 1

    def pos(self, screen):
        # self.mov(grid)
        screen.blit(self.img, self.rect.topleft)

    def respawn(self):
        self.__init__()
