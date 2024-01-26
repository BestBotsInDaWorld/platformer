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


KEY_BINDINGS = {
    "KEY_UP": pygame.K_UP,
    "KEY_DOWN": pygame.K_DOWN,
    "KEY_RIGHT": pygame.K_RIGHT,
    "KEY_LEFT": pygame.K_LEFT,
}
FPS = 60
WIDTH = 800
HEIGHT = 600
GRAVITY = 0.25
GROUND_DX = 0.15
AIR_DX = 0.1
MAX_DX = 5.0
MAX_DY = 5.0
MAX_JUMP_HEIGHT = 80
ENEMY_DEFEAT_BOUNCE = 3
RESISTANCE = 0.25
IFRAMES = 20
CONSTUCTOR_CAMERA_X = 5
CONSTUCTOR_CAMERA_Y = 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # экран
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
trap_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()