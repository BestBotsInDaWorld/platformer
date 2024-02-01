import os
from tkinter import Tk
import pygame

pygame.init()
state = "menu"

def get_keys():
    with open("key_bindings.txt", "r") as f:
        f = f.read()
        keys = f.split()
        # Преобразование каждого значения в объект типа pygame

        up = getattr(pygame, keys[0])
        up = pygame.key.key_code(keys[0][2:])
        down = getattr(pygame, keys[1])
        down = pygame.key.key_code(keys[1][2:])
        right = getattr(pygame, keys[2])
        right = pygame.key.key_code(keys[2][2:])
        left = getattr(pygame, keys[3])
        left = pygame.key.key_code(keys[3][2:])

        # Создание словаря с преобразованными значениями
        binds = {
            "KEY_UP": up,
            "KEY_DOWN": down,
            "KEY_RIGHT": right,
            "KEY_LEFT": left,
        }
        return binds


TRAPS_PARAMETES = {
    "Dart Trap\idle.png": {"direction": "Right", "arrow_velocity": 5, "before_start": 0, "shot_delay": 120},
    "Falling Platform\idle.png": {"traectory": (1, 0), "velocity": 1, "before_start": 0,
                 "length": 300, "before_fall": 90, "refresh_time": 300, "falling_time": 300},
    "Fire Maker\idle.png": {"before_start": 0, "shot_delay": 60, "warning_time": 32, "damaging_time": 60},
    "Jump Refresher\idle.png": {"refresh_time": 300},
    "Platform\idle.png": {"traectory": (1, 0), "velocity": 2, "before_start": 0, "length": 300, "variation" :'Brown'},
    "Saw\idle.png": {"traectory": (1, 0), "velocity": 2, "before_start": 0, "length": 300},
    "Spike\idle.png": {},
    "Spiked Ball\idle.png": {"traectory": (1, 0), "velocity": 2, "before_start": 0, "length": 300},
    "Trampoline\idle.png": {"direction": "Up", "bounce_speed": 10},
}


KEY_BINDINGS = {
    "KEY_UP": pygame.K_UP,
    "KEY_DOWN": pygame.K_DOWN,
    "KEY_RIGHT": pygame.K_RIGHT,
    "KEY_LEFT": pygame.K_LEFT,
}

TRAPS_PARAMETES = {
    "Dart Trap\Idle.png": {"direction": "Right", "arrow_velocity": 5, "before_start": 0, "shot_delay": 120},
    "Falling Platform\Idle.png": {"traectory": (1, 0), "velocity": 1, "before_start": 0,
                 "length": 300, "before_fall": 90, "refresh_time": 300, "falling_time": 300},
    "Fire Maker\Idle.png": {"before_start": 0, "shot_delay": 60, "warning_time": 32, "damaging_time": 60},
    "Jump Refresher\Idle.png": {"refresh_time": 300},
    "Platform\Idle.png": {"traectory": (1, 0), "velocity": 2, "before_start": 0, "length": 300, "variation" :'Brown'},
    "Saw\Idle.png": {"traectory": (1, 0), "velocity": 2, "before_start": 0, "length": 300},
    "Spike\Idle.png": {},
    "Spiked Ball\Idle.png": {"traectory": (1, 0), "velocity": 2, "before_start": 0, "length": 300},
    "Trampoline\Idle.png": {"direction": "Up", "bounce_speed": 10},
}


FPS = 60
monitor_info = Tk()
WIDTH = 800
HEIGHT = 600
WIDTH_COEF = WIDTH / 800
HEIGHT_COEF = HEIGHT / 600
GRAVITY = 0.25 * HEIGHT_COEF
GROUND_DX = 0.15 * WIDTH_COEF
AIR_DX = 0.1 * WIDTH_COEF
MAX_DX = 4.0 * WIDTH_COEF
MAX_DY = 5.0 * HEIGHT_COEF
MAX_JUMP_HEIGHT = 20 * HEIGHT_COEF
ENEMY_DEFEAT_BOUNCE = 4 * HEIGHT_COEF
HP_CAP = 20
RESISTANCE = 0.25 * WIDTH_COEF
IFRAMES = 20
CONSTUCTOR_CAMERA_X = 5
CONSTUCTOR_CAMERA_Y = 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # экран
pygame.display.set_caption("Challenge Seeker")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
trap_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
special_group = pygame.sprite.Group()
background_group = pygame.sprite.Group()

nearest_blocks = pygame.sprite.Group()
nearest_traps = pygame.sprite.Group()
nearest_enemies = pygame.sprite.Group()

sound_lib = {
    name.split('.')[0]: pygame.mixer.Sound(rf"data\\Sounds\\{name}")
    for name in os.listdir(rf"data\\Sounds")
}