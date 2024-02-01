from create_level import create_level
from useful_funcs import *
from settings import *
from menu import *

from traps.Trap import Trap
from traps.DartTrap import DartTrap
from traps.FallingPlatform import FallingPlatform
from traps.FireMaker import FireMaker
from traps.JumpRefresher import JumpRefresher
from traps.Platform import Platform
from traps.Saw import Saw
from traps.Spike import Spike
from traps.SpikedBall import SpikedBall
from traps.Trampoline import Trampoline

from enemies.Enemy import Enemy
from enemies.Plant import Plant
from enemies.AngryPig import AngryPig
from enemies.BlueBird import BlueBird
from enemies.Chicken import Chicken
from enemies.Bunny import Bunny
from enemies.Ghost import Ghost
from enemies.Skull import Skull

from blocks.Block import Block, block_names
from hero.Hero import Hero
from background import Background

from config_change import set_settings

pygame.init()

hero = Hero("Ninja Frog", 0, 0)
start_point = pygame.Rect(0, HEIGHT, 1, 1)


KEY_BINDINGS = get_keys()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 6 -
                    min(WIDTH // 4, abs(start_point.left - target.rect.left)))
        start_point.x += self.dx
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT +
                    min(HEIGHT // 4, start_point.top - target.rect.top))
        start_point.y += self.dy

    def bg_apply(self, target, bg):
        bg.rect.x = (target.rect.x - WIDTH // 2) - WIDTH * ((target.rect.x - start_point.x) / (WIDTH * 10))
        bg.rect.y = min((target.rect.y - HEIGHT) - HEIGHT * ((target.rect.y - start_point.y) / (HEIGHT * 10)),
                        -(HEIGHT // 4))


def upload_level(level_name):
    with open(f"levels\{level_name}.txt", "r") as lv:
        lv = lv.read().split("\n")

        for block in lv:

            block = block.split(';')
            if block[0] in block_names:
                block_group.add(Block(block[0], int(block[1]), int(block[2])))
            elif block[0] == "Dart Trap\\Idle.png":
                param = eval(block[3])
                trap_group.add(DartTrap(int(block[1]), int(block[2]), param["direction"],
                                         param["arrow_velocity"], param["before_start"], param["shot_delay"]))
            elif block[0] == "Falling Platform\\Idle.png":
                param = eval(block[3])
                trap_group.add(FallingPlatform(int(block[1]), int(block[2]), param["traectory"], param["velocity"],
                                                param["before_start"], param["length"], param["before_fall"],
                                                param["refresh_time"],
                                                param["falling_time"]))
            elif block[0] == "Fire Maker\\Idle.png":
                param = eval(block[3])
                trap_group.add(FireMaker(int(block[1]), int(block[2]), param["before_start"], param["shot_delay"],
                                          param["warning_time"], param["damaging_time"]))
            elif block[0] == "Jump Refresher\\Idle.png":
                param = eval(block[3])
                trap_group.add(JumpRefresher(int(block[1]), int(block[2]), param["refresh_time"]))
            elif block[0] == "Platform\\Idle.png":
                param = eval(block[3])
                trap_group.add(Platform(int(block[1]), int(block[2]), param["traectory"],
                                         param["velocity"], param["before_start"], param["length"],
                                         param["variation"]))
            elif block[0] == "Saw\\Idle.png":
                param = eval(block[3])
                trap_group.add(Saw(int(block[1]), int(block[2]), param["traectory"], param["velocity"],
                                    param["before_start"], param["length"]))
            elif block[0] == "Spike\\Idle.png":
                param = eval(block[3])
                trap_group.add(Spike(int(block[1]), int(block[2])))
            elif block[0] == "Spiked Ball\\Idle.png":
                param = eval(block[3])
                trap_group.add(SpikedBall(int(block[1]), int(block[2]), param["traectory"], param["velocity"],
                                           param["before_start"], param["length"]))
            elif block[0] == "Trampoline\\Idle.png":
                param = eval(block[3])
                trap_group.add(Trampoline(int(block[1]), int(block[2]), param["direction"], param["bounce_speed"]))
            elif block[0] == "Angry Pig\\Idle.png":
                enemy_group.add(AngryPig(int(block[1]), int(block[2])))
            elif block[0] == "Blue Bird\\Idle.png":
                enemy_group.add(BlueBird(int(block[1]), int(block[2])))
            elif block[0] == "Bunny\\Idle.png":
                enemy_group.add(Bunny(int(block[1]), int(block[2])))
            elif block[0] == "Chicken\\Idle.png":
                enemy_group.add(Chicken(int(block[1]), int(block[2])))
            elif block[0] == "Ghost\\Idle.png":
                enemy_group.add(Ghost(int(block[1]), int(block[2])))
            elif block[0] == "Plant\\Idle.png":
                enemy_group.add(Plant(int(block[1]), int(block[2])))
            elif block[0] == "Skull\\Idle.png":
                enemy_group.add(Skull(int(block[1]), int(block[2])))


def main_game():
    cur_level = 1
    upload_level("lvl1")
    camera = Camera()
    death_bg = Background("bg_3", 0, -HEIGHT)
    running = True
    while running:

        camera.update(hero)
        nearest_traps.empty()
        nearest_blocks.empty()
        nearest_enemies.empty()
        for sprite in all_sprites:
            camera.apply(sprite)
            if check_activity(sprite, hero):
                if isinstance(sprite, Block):
                    nearest_blocks.add(sprite)
                elif isinstance(sprite, Trap):
                    nearest_traps.add(sprite)
                elif isinstance(sprite, Enemy):
                    nearest_enemies.add(sprite)
                sprite.is_active = True
            else:
                sprite.is_active = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for enemy in enemy_group:
            enemy.under_map_check(start_point)
        screen.fill(pygame.Color("orange"))

        hero_group.update(pygame.key.get_pressed())
        camera.bg_apply(hero, death_bg)
        background_group.draw(screen)
        block_group.draw(screen)
        trap_group.draw(screen)
        enemy_group.draw(screen)
        hero_group.draw(screen)
        trap_group.update(hero=hero, blocks=block_group)
        enemy_group.update(hero=hero, blocks=block_group, start=start_point)
        pygame.display.flip()
        clock.tick(FPS)


main_game()
pygame.quit()
