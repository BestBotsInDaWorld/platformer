import pygame
from settings import WIDTH, HEIGHT
from useful_funcs import load_image
tile_group = pygame.sprite.Group()
background = pygame.sprite.Group()
tiles = []


def animate_background(tiles):
    for tile in tiles:
        tile.move()


bg_colors = ["Pink", "Purple", "Blue", "Yellow", "Gray"]


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, x, y):
        super().__init__(tile_group, background)
        path = rf"Background\{tile}.png"
        self.x = x
        self.y = y
        self.image = load_image(path)
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect = self.rect.move(x, y)
        self.image = pygame.transform.scale(self.image, (50, 50))

    def move(self):
        if self.rect.x >= WIDTH or self.rect.y >= HEIGHT:
            self.rect.x = self.rect.x - WIDTH - 50
        else:
            self.rect.x += 1


def gen_background():
    current_color = 0
    for i in range(0, 1600, 50):
        for j in range(0, 1600, 50):
            current_color = (current_color + 1) % 5
            tile = Tile(bg_colors[current_color], i, j)
            tiles.append(tile)