import pygame
KEY_BINDS = {
    "KEY_UP": pygame.K_UP,
    "KEY_DOWN": pygame.K_DOWN,
    "KEY_LEFT": pygame.K_LEFT,
    "KEY_RIGHT": pygame.K_RIGHT,
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
RESISTANCE = 0.25
IFRAMES = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # экран
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()