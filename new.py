from create_level import create_level
from useful_funcs import *
from settings import *
from menu import *
import importlib

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

from blocks.Block import Block
from hero.Hero import Hero
from config_change import set_settings

pygame.init()

hero = Hero("Ninja Frog", 50, 50)
start_point = pygame.Rect(0, HEIGHT, 1, 1)




from random import randint

#  for i in range(20):
#     block = SpikedBall(randint(0, 740), randint(0, 300), traectory=(1, 1), velocity=0.5, before_start=0, length=200)

running = True
KEY_BINDINGS = get_keys()

# load_ost("ost_1.mp3")
curr_level = 7





block_group = pygame.sprite.Group()
block_names = ([f"{name} Big" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]] +
               [f"{name} Small" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]])
block_images = {key: load_image(rf"Terrain\Square Blocks\{key}.png") for key in block_names}


folder_path = 'data\Traps'  # путь к папке Traps
subfolders = os.listdir(folder_path)
subfolders_traps = [path for path in subfolders if path != "Fire" and path != "Arrow"]
folders = [f"{path}\Idle.png" for path in subfolders_traps]
trap_images = {path: load_image(rf"Traps\{path}") for path in folders}
folder_path_enemies = 'data\Enemies'  # путь к папке Traps
subfolders_enemies = os.listdir(folder_path_enemies)
subfolders_enemies = [path for path in subfolders_enemies if path != "Orange Particle"
                      and path != "Red Particle"]
folders_enemies = [f"{path}\\Idle.png" for path in subfolders_enemies]

enemies_images = {path: load_image(rf"Enemies\\{path}") for path in folders_enemies}
block_images = block_images


def upload_level():
    with open(f"levels\lvl{curr_level}.txt", "r") as lv:
        lv = lv.read().split("\n")

        for block in lv:

            block = block.split(';')
            print(block[0])
            if block[0] in block_names:
                block_group.add(Block(block[0], int(block[1]), int(block[2])))
            if block[0] == "Dart Trap\\Idle.png":
                param = eval(block[3])
                print(param)
                block_group.add(DartTrap(int(block[1]), int(block[2]), param["direction"],
                                param["arrow_velocity"], param["before_start"], param["shot_delay"]))
            if block[0] == "Falling Platform\\Idle.png":
                param = eval(block[3])
                block_group.add(FallingPlatform(int(block[1]), int(block[2]), param["traectory"], param["velocity"],
                                param["before_start"], param["length"], param["before_fall"], param["refresh_time"],
                                param["falling_time"]))
            if block[0] == "Fire Maker\\Idle.png":
                param = eval(block[3])
                block_group.add(FireMaker(int(block[1]), int(block[2]), param["before_start"], param["shot_delay"],
                                          param["warning_time"], param["damaging_time"]))
            if block[0] == "Jump Refresher\\Idle.png":
                param = eval(block[3])
                block_group.add(JumpRefresher(int(block[1]), int(block[2]), param["refresh_time"]))
            if block[0] == "Platform\\Idle.png":
                param = eval(block[3])
                block_group.add(Platform(int(block[1]), int(block[2]), param["traectory"],
                                         param["velocity"], param["before_start"], param["length"],
                                         param["variation"]))
            if block[0] == "Saw\\Idle.png":
                param = eval(block[3])
                block_group.add(Saw(int(block[1]), int(block[2]), param["traectory"], param["velocity"],
                                    param["before_start"], param["length"]))
            if block[0] == "Spike\\Idle.png":
                param = eval(block[3])
                block_group.add(Spike(int(block[1]), int(block[2])))
            if block[0] == "Spiked Ball\\Idle.png":
                param = eval(block[3])
                block_group.add(SpikedBall(int(block[1]), int(block[2]), param["traectory"], param["velocity"],
                                      param["before_start"], param["length"]))
            if block[0] == "Trampoline\\Idle.png":
                param = eval(block[3])
                block_group.add(Trampoline(int(block[1]), int(block[2]), param["direction"], param["bounce_speed"]))
            if block[0] == "Angry Pig\\Idle.png":
                block_group.add(AngryPig(int(block[1]), int(block[2])))
            if block[0] == "Blue Bird\\Idle.png":
                block_group.add(BlueBird(int(block[1]), int(block[2])))
            if block[0] == "Bunny\\Idle.png":
                block_group.add(Bunny(int(block[1]), int(block[2])))
            if block[0] == "Chicken\\Idle.png":
                block_group.add(Chicken(int(block[1]), int(block[2])))
            if block[0] == "Ghost\\Idle.png":
                block_group.add(Ghost(int(block[1]), int(block[2])))
            if block[0] == "Plant\\Idle.png":
                block_group.add(Plant(int(block[1]), int(block[2])))
            if block[0] == "Skull\\Idle.png":
                block_group.add(Skull(int(block[1]), int(block[2])))



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
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 1.2)
        start_point.y += self.dy

upload_level()

while running:
    camera = Camera()
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
    all_sprites.draw(screen)
    hero_group.draw(screen)
    trap_group.update(hero=hero, blocks=block_group)
    enemy_group.update(hero=hero, blocks=block_group, start=start_point)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
