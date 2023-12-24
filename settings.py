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
MAX_JUMP_HEIGHT = 80
RESISTANCE = 0.25
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # экран
clock = pygame.time.Clock()