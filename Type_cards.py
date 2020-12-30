import pygame as pg
import random

pg.init()
screen = pg.display.set_mode([500, 500])
square = pg.Surface((20, 20))
square.fill((255, 255, 255))
rect = square.get_rect()
clock = pg.time.Clock()
position_vec = pg.Vector2(rect.topleft)
direction_vec = None
target_vec = None
speed = 1
while True:
    clock.tick(30)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            rect.x = random.randrange(0, 479)
            rect.y = random.randrange(0, 479)
        if event.type == pg.MOUSEMOTION:
            target_vec = pg.Vector2(event.pos)
            direction_vec = target_vec - position_vec
            direction_vec.normalize_ip()
    pressed = pg.key.get_pressed()
    if pressed[pg.K_w]:
        rect.y -= 1
    if pressed[pg.K_s]:
        rect.y += 1
    if pressed[pg.K_a]:
        rect.x -= 1
    if pressed[pg.K_d]:
        rect.x += 1
    if target_vec is not None:
        position_vec += direction_vec * speed
        rect.x = int(position_vec.x)
        rect.y = int(position_vec.y)
        if position_vec.distance_squared_to(target_vec) < speed*speed:
            rect.x = int(target_vec.x)
            rect.y = int(target_vec.y)
            target_vec = None
            print(rect.x, rect.y)
    screen.fill((0, 0, 0))
    screen.blit(square, rect)
    pg.display.flip()
