import pygame
import scene
import character
import media
import random
import Manage
import cards
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
            self.manager.go_to(InitScene("Tim Invaded The Moon"))
        elif self.box2.collidepoint(mouse) and press:
            self.manager.go_to(ByeScene())


#  --Init Scene--
class InitScene(Manage.Scene):
    def __init__(self, message):
        super(InitScene, self).__init__()
        self.FONT = pygame.font.Font(None, 46)
        self.text = self.FONT.render(message, 1, (240, 230, 180))
        self.background, _ = media.load_png("background.png")
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
        if self.alpha < 255:
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
        # Scenario
        self.scenario = scene.grid(50, 50, 32, 32, 8)
        character.GameEntity.scenario = self.scenario
        # playable character
        self.velita = character.Player()  # Jugador Principal
        # non-playable character
        self.ghosts = []
        for x in range(5):
            self.ghosts.append(character.Enemy())
        # Turns-playable character
        self.players = []  # self.ghosts[:]
        self.players.append(self.velita)
        # interface
        self.font = pygame.font.Font(None, 20)
        self.GUI = GUI.pantalla(self.velita, screen, self.scenario)
        # building deck
        self.velita.deck = cards.Deck(self.velita, 10, self.GUI)
        random.shuffle(self.players)
        # Turn manager
        self.turns = Manage.TurnManager(self.players, self.scenario)
        self.alpha = 0
        self.cards = []
        self.velita.moon_points = 0

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_v:
                    self.cards.append(character.Card())
                if e.key == pygame.K_c:
                    self.velita.deck.take_card()
                if e.key == pygame.K_x:
                    self.velita.deck.put_in_hand()
                if e.key == pygame.K_p:
                    pygame.image.save(screen, "screenshot.png")
                if e.key == pygame.K_SPACE:
                    self.manager.go_to(TitleScene())
                if e.key == pygame.K_g:  # Cambiar
                    self.GUI.show = not self.GUI.show
                if e.key == pygame.K_h:
                    self.manager.go_to(EndingScene())

    def update(self):
        # mouse_pressed = pygame.mouse.get_pressed()
        self.text = self.font.render(
            f'''PosX: {self.velita.Px}, PosY: {self.velita.Py} ~~ {self.scenario.CHECK_mouse()}''',
            1, (250, 250, 25))
        if self.velita.deck.using_card():
            self.turns.round += 1
            self.cards.append(character.Card())
        for enemy in self.ghosts:
            if enemy.life <= 0:
                enemy.respawn()
        if self.velita.moon_points == 5:
            self.manager.go_to(EndingScene())

        # -aquí pondre la cuestión de los turnos

    def render(self, screen):
        screen.fill((255, 125, 180))
        screen.blit(self.text, (5, 480))
        media.put_string(f'{self.turns.round}', screen, (0, 0))
        self.GUI.draw_things()
        pygame.display.update()


#  --Winning Scene--
class EndingScene(InitScene):
    def __init__(self):
        super(EndingScene, self).__init__("YOU WON")
        self.counter = 0

    def render(self, screen):
        self.background.set_alpha(self.alpha)
        self.text.set_alpha(self.alpha)
        screen.blit(self.background, (0, 0))
        screen.blit(self.text, self.pos)

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and self.alpha >= 255:
                self.manager.go_to(ByeScene())


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
