import pygame
from useful_funcs import *


pygame.init()

KEY_BINDS = {}
with open("key_binds", "r") as f:
    f = f.read()
    keys = f.split()
    # Преобразование каждого значения в объект типа pygame

    KEY_UP = getattr(pygame, keys[0])
    KEY_UP = pygame.key.key_code(keys[0][2:])

    KEY_DOWN = getattr(pygame, keys[1])
    KEY_DOWN = pygame.key.key_code(keys[1][2:])
    KEY_LEFT = getattr(pygame, keys[2])
    KEY_LEFT = pygame.key.key_code(keys[2][2:])
    KEY_RIGHT = getattr(pygame, keys[3])
    KEY_RIGHT = pygame.key.key_code(keys[3][2:])

    # Создание словаря с преобразованными значениями
    KEY_BINDS = {
        "KEY_UP": KEY_UP,
        "KEY_DOWN": KEY_DOWN,
        "KEY_LEFT": KEY_LEFT,
        "KEY_RIGHT": KEY_RIGHT
    }

print(KEY_BINDS)
FPS = 60
WIDTH = 800
HEIGHT = 600
GRAVITY = 0.25
GROUND_DX = 0.15
AIR_DX = 0.1
MAX_DX = 5.0
MAX_DY = 5.0
MAX_JUMP_HEIGHT = 80
RESISTANCE = 0.25
IFRAMES = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # экран
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()



