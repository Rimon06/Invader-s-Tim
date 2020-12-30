import pygame
import media
import random

MOVE = "move"
ATTACK = "attack"
DEFENSE = "defense"
MOONSHOT = "moonshot"
TYPECARD = [MOVE, ATTACK, MOONSHOT]  # , DEFENSE, MOONSHOT]


class card():
    def __init__(self, type=None):
        self.image, self.rect = media.load_png("card.png")
        self.type = type
        self.grab = False
        self.used = False
        self.x2 = pygame.transform.scale(self.image, (self.rect.width*2, self.rect.height*2))
        self.rect = self.x2.get_rect()
        self.dx, self.dy = 0, 0
        self.description = ''

    def draw(self, screen, coord=(0, 0)):
        self.rect.topleft = (coord[0], coord[1])
        self.grabbed()  # Agarra una carta, y cambia la posicion del rect

        screen.blit(self.x2, self.rect.topleft)  # CUIDADO, MOSTRARÁ SOLO EL REVERSO

    # En estas dos funciones hay un posible error con el click. Pendiente.
    def click(self):
        '''select a card clicking it'''
        x, y = pygame.mouse.get_pos()
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:

        if self.click_card():
            # self.grab = not self.grab
            if not self.grab:  # dx and dy are both 0 if the card is not selected
                self.dx, self.dy = 0, 0
                self.use = False
        return x, y

    def mouse_in_card(self):
        x, y = pygame.mouse.get_pos()
        return self.rect.collidepoint(x, y)

    def click_card(self):
        return self.mouse_in_card() and pygame.mouse.get_pressed()[0]

    def show_data(self):
        text = f'''Type: {self.type}
grab: {self.grab}
used: {self.used}
dx,dy: ({self.dx},{self.dy})
''' + self.description
        return text

    def grabbed(self):
        x, y = self.click()

        if not self.grab:
            # Falta el event.type == KEYDOWN, por eso la carta se reinicia varias veces . . .
            # collide and get_pressed
            if self.click_card():
                self.dx, self.dy = x-self.rect.left, y-self.rect.top
                self.grab = True
        elif self.click_card():  # pygame.mouse.get_pressed()[0]:
            self.grab = False
        elif pygame.mouse.get_pressed()[0]:
            self.rect.topleft = x-self.dx, y-self.dy

# Methods for subclasses

    def action(self):
        '''Things the character needs to do before applying the effects of the card'''
        pass

    def apply(self):
        '''Effect of the card'''
        pass


# Cambiar como muestra los cuadros en los que puede moverse
class moving_card(card):
    def __init__(self, player, gui):
        super(moving_card, self).__init__(MOVE)
        # self.front, self.rect = media.load_png("move_card.png")
        self.player = player
        self.description = '''Move player 1 to 6 steps'''
        self.gui = gui
        self.num = 0

    def action(self):
        '''Aleatoriamente selecciona el numero de pasos
        el personaje se mueve en torno a esos pasos
        Se muestra los pasos que le faltan, lo que hace la carta'''
        if not self.used:
            self.STEPS = random.randint(1, 6)
            print("pasos", self.STEPS)
            self.road = []
            self.used = True
            self.decided = self.player.get_pos()  # Px, Py
        if len(self.road) < self.STEPS:
            # choose path
            # self.player.move()
            # pos, logic, click = self.player.move(self.road, self.decided)
            # if logic:
            #     SET color of background as green
            #     box = self.gui.grid[pos]
            #     box.setbackground((0,255,0))
            #     pygame.draw.rect(self.gui.screen, (0, 255, 0), box.rect)
            #     pygame.display.update(box.rect)
            pos = self.gui.grid.CHECK_mouse()
            b = pos not in self.road
            c = self.gui.grid.Can_you_move(self.decided, pos)
            if b and c:
                # draw remarked casilla
                box = self.gui.grid[pos]
                pygame.draw.rect(self.gui.screen, (0, 255, 0), box.rect)
                pygame.display.update(box.rect)
                if pygame.mouse.get_pressed()[0]:
                    # el codigo de abajo debe prevalecer para cualquier personaje
                    # el de arriba es valido solo para el jugador principal.
                    # ¡El CPU no puede usar el mouse!
                    # Sin embargo, debe mantenerse ciertas condiciones de movimiento como
                    # el metodo Can_you_move(),
                    self.road.append(pos)
                    self.decided = pos
        if not self.grab:
            self.used = False
        # ¿Que pasa si no hay más caminos posible?
        # Escoge opciones validas, guarda el camino en la variable road

    def apply(self):
        # Posiblemente hacer: Realizar un método intercambio entre casillas
        if len(self.road) == self.STEPS and self.num != self.STEPS:
            posAct = self.player.get_pos()
        #    actual = self.gui.grid[posAct]  # Celda actual del personaje
            self.gui.grid.swap(self.road[self.num], posAct)
            pygame.time.delay(500)
            self.num += 1
        return self.num == self.STEPS
        # realizar animacióno
        # Esto es otro sitio????


class attack_card(card):
    def __init__(self, player, gui):
        super(attack_card, self).__init__(ATTACK)
        self.player = player
        self.description = '''Select an character to attack him'''
        self.gui = gui
        self.target = None

    def action(self):
        if not self.used:
            self.target = self.player.attack(self.gui.grid)
            if self.target is None:
                return False
            else:
                self.used = True
                return True

            # XYcas = self.gui.grid.CHECK_mouse()
            # if XYcas is None or XYcas == (self.player.Px, self.player.Py):
            #     return False
            # casilla = self.gui.grid[XYcas]
            # if pygame.mouse.get_pressed()[0] and casilla.peso == 10:  # Condición antes vista
            #     self.target = casilla.player
            #     self.used = True
            # Hacer que la imagen del target resalte más al ser escogido

        pass

    def apply(self):
        if self.used:
            self.target.life -= random.randint(1, 3)
            return True
        return False


class moonshot_card(card):
    def __init__(self, player, gui):
        super(moonshot_card, self).__init__(MOONSHOT)
        self.player = player
        self.description = '''M O O N S H O T'''
        self.gui = gui

    def action(self):
        pass

    def apply(self):
        self.player.moon_points += 1
        return True


CARD_DICT = {MOVE: moving_card, ATTACK: attack_card, MOONSHOT: moonshot_card}


def choice_type():
    t_card = random.choices(TYPECARD, weights=[25, 25, 60])
    return CARD_DICT[t_card[0]]


class Deck():
    def __init__(self, player, number, gui):
        self.cards = []
        for n in range(number):  # Agrega cartas al mazo
            card = choice_type()
            self.cards.append(card(player, gui))
        self.cards.reverse()
        self.number = number
        self.showing = []
        self.limit_show = 5
        self.put_in_hand()
        self.use = None

    def draw(self, screen, center):
        # Colocarlo en una posicion especifica del grid
        RECT = pygame.Rect(0, 0, 64*len(self.showing), 40)
        RECT.center = center
        i = 0
        for cards in self.showing:
            cards.draw(screen, (RECT.left+i*40, RECT.top-10))
            media.put_string(f'{cards.type}', screen, cards.rect.midbottom)
            i += 1
        i = 0
        for cards in self.cards:
            cards.draw(screen, (50, RECT.top-10-i))
            i += 1
            media.put_string(f'{cards.type}', screen, cards.rect.midbottom)

    def shuffle(self):
        random.shuffle(self.cards)

    def put_in_hand(self, num=20):
        '''pone todas las cartas que pueda del mazo a la mano
        num:limita la cantidad de cartas.
        Si no hay valor de num pone todas las que pueda en la mano'''
        x = 0
        while len(self.cards) > 0 and len(self.showing) < self.limit_show and x < num:
            carta = self.cards.pop()  # Saca la primera carta que se muestra
            self.showing.append(carta)
            x += 0

    def take_card(self, card=None):  # Usar ratón para quitar cartas
        if len(self.showing) != 0:
            if card is None:
                self.showing.pop()
            else:
                self.showing.pop(self.showing.index(card))

    def using_card(self):
        for card in self.showing:
            if card.grab:  # Tomar una carta
                self.use = card
                break
        else:
            self.use = None
            for card in self.showing:
                card.used = False
        # Uso de la carta
        if self.use is not None:
            self.use.action()
            if self.use.apply():
                self.take_card(self.use)  # Enviar carta usada para eliminarla
                self.use = None
                return True
        return False


# Hacer función reinicio de carta. . .111
# Pasos:
# Secuencia lógica antes
# Secuencia animada antes
# Secuencia animada durante #
# Secuencia Lógica despues
# Secuencia animada despues
