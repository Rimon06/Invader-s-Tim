import pygame
import scene
import character
import media
import cards
import random
import Manage
import GUI
# import math
# from pygame import math as PyM

# Initialize the pygame
pygame.init()
clock = pygame.time.Clock()

# Create the screen
AWin = (Width, Height) = (600, 450)
RGB = (255, 125, 180)
screen = pygame.display.set_mode(AWin)

# Title and Icon
pygame.display.set_caption("Invader's Tim")
icon, _ = media.load_png("Tim_Brown.jpg")
pygame.display.set_icon(icon)


#  --Title Scene--
class TitleScene(Manage.Scene):
    def __init__(self):
        super(TitleScene, self).__init__()
        self.background, self.RECT = media.load_png("background.png")
        self.box1 = pygame.Rect(50, 50, 100, 50)
        self.box2 = pygame.Rect(50, 200, 100, 50)

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        pygame.draw.rect(screen, (0, 255, 0), self.box1)
        pygame.draw.rect(screen, (255, 0, 0), self.box2)
        media.put_string("Jugar", screen, self.box1.center)
        media.put_string("Salir", screen, self.box2.center)

    def update(self):
        pass

    def handle_events(self, events):
        mouse = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()[0]
        if self.box1.collidepoint(mouse) and press:
            self.manager.go_to(init())
        elif self.box2.collidepoint(mouse) and press:
            self.manager.go_to(ByeScene())


#  --Init Scene--
class init(Manage.Scene):
    def __init__(self):
        super(init, self).__init__()
        self.FONT = pygame.font.Font(None, 46)
        self.text = self.FONT.render("Tim Invaded The Moon", 1, (240, 230, 180))
        self.background, self.RECT = media.load_png("background.png")
        self.alpha = 0
        self.pos = self.text.get_rect()
        self.pos.center = screen.get_rect().center

    def render(self, screen):
        screen.fill((20, 10, 20))
        self.background.set_alpha(255-self.alpha)
        self.text.set_alpha(self.alpha)
        screen.blit(self.background, (0, 0))
        screen.blit(self.text, self.pos)

    def update(self):
        if self.alpha < 256:
            self.alpha += 1

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                self.manager.go_to(GameScene())


#  --GoodBye Scene--
class ByeScene(Manage.Scene):
    def render(self, screen):
        pass

    def update(self):
        quit()

    def handle_events(self, events):
        pass


#  --Level Scene--
class GameScene(Manage.Scene):
    def __init__(self):
        super(GameScene, self).__init__()
        self.score = 0
        self.grid = scene.grid(50, 50, 32, 32, 8)
        self.velita = character.player(self.grid)  # Jugador Principal
        self.ghosts = []
        for x in range(5):
            self.ghosts.append(character.Enemy(self.grid))
        self.players = self.ghosts[:]
        self.players.append(self.velita)
        # self.cartica = cards.deck(21)
        self.font = pygame.font.Font(None, 20)
        self.GUI = GUI.pantalla(self.velita, screen, self.grid)
        random.shuffle(self.players)
        self.turns = Manage.TurnManager(self.players, self.grid)

        self.alpha = 0

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if self.turns.ActionTurn()(e.key, self.grid):
                    self.turns.NextTurn(1)
                    pygame.time.delay(50)
                # if e.key == pygame.K_v:
                #     self.cartica.shuffle()
                # if e.key == pygame.K_c:
                #     self.cartica.take_card()
                # if e.key == pygame.K_x:
                #     self.cartica.put_to_show()
                if e.key == pygame.K_p:
                    pygame.image.save(screen, "screenshot.png")
                if e.key == pygame.K_SPACE:
                    self.manager.go_to(TitleScene())

    def update(self):
        # mouse_pressed = pygame.mouse.get_pressed()
        self.text = self.font.render(
            f'''PosX: {self.velita.Px}, PosY: {self.velita.Py} ~~ {self.grid.CHECK_mouse()}''', 1, (250, 250, 25))
        # -aquí pondre la cuestión de los turnos

    def render(self, screen):
        screen.fill((255, 125, 180))
        screen.blit(self.text, (5, 480))
        media.put_string(f'{self.turns.round}', screen, (0, 0))
        self.GUI.draw_things()

        # self.cartica.show(screen, self.grid.inside_grid.bottomleft)
        pygame.display.update()


running = True
manager = Manage.SceneManager(TitleScene())
while running:
    clock.tick(60)

    if pygame.event.get(pygame.QUIT):
        manager.go_to(ByeScene())
    manager.scene.handle_events(pygame.event.get())
    manager.scene.update()
    manager.scene.render(screen)
    pygame.display.flip()
