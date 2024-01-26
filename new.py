from create_level import create_level
from useful_funcs import *
from settings import *
from menu import *

from traps.DartTrap import DartTrap
from traps.FallingPlatform import FallingPlatform
from traps.FireMaker import FireMaker
from traps.JumpRefresher import JumpRefresher
from traps.Platform import Platform
from traps.Saw import Saw
from traps.Spike import Spike
from traps.SpikedBall import SpikedBall
from traps.Trampoline import Trampoline

from enemies.Plant import Plant
from enemies.AngryPig import AngryPig

from blocks.Block import Block
from hero.Hero import Hero
from config_change import set_settings

pygame.init()

hero = Hero("Mask Dude", 50, 50)
start_point = pygame.Rect(0, HEIGHT, 1, 1)

Block("Autumn Big", 0, 350)
Block("Autumn Big", 2400, 350)
for i in range(50):
    block = Block("Autumn Big", 0 + i * 48, 400)

for i in range(50):
    block = Block("Autumn Big", 0 + i * 48, 600)

from random import randint, choice

#  for i in range(20):
#     block = SpikedBall(randint(0, 740), randint(0, 300), traectory=(1, 1), velocity=0.5, before_start=0, length=200)
#  for i in range(20):
#      block = DartTrap(randint(0, 740), randint(0, 300), direction="Up")
for i in range(20):
    block = AngryPig(randint(100, 2000), randint(100, 300))
for i in range(20):
    block = Plant(randint(100, 2000), randint(100, 300))

running = True
KEY_BINDINGS = get_keys()
load_ost("ost_1.mp3")


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 6 -
                    min(WIDTH // 6, abs(start_point.left - target.rect.left)))
        start_point.x += self.dx
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 1.2)
        start_point.y += self.dy


while running:
    camera = Camera()
    camera.update(hero)
    for sprite in all_sprites:
        camera.apply(sprite)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color("orange"))
    hero_group.update(pygame.key.get_pressed())
    all_sprites.draw(screen)
    hero_group.draw(screen)
    trap_group.update(hero=hero, blocks=block_group)
    enemy_group.update(hero=hero, blocks=block_group)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
