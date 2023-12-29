import pygame

pygame.init()

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


KEY_BINDINGS = get_keys()
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


