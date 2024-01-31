import pygame
import os
from settings import WIDTH, HEIGHT, all_sprites, WIDTH_COEF, HEIGHT_COEF, background_group
from useful_funcs import load_image, cut_sheet
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


bg_images = {key.split(".")[0]: key for key in os.listdir(rf"data\Background")}
for key in bg_images.keys():
    bg_images[key] = load_image(rf"Background\{bg_images[key]}")


class Background(pygame.sprite.Sprite):
    def __init__(self, bg_name, pos_x, pos_y):
        super().__init__(background_group, all_sprites)
        image = bg_images[bg_name]  # строка с названием
        copy_rect = image.get_rect()
        self.image = pygame.transform.scale(image, (copy_rect.width * WIDTH_COEF, copy_rect.height * HEIGHT_COEF))
        self.rect = self.image.get_rect().move(
            pos_x * WIDTH_COEF, pos_y * HEIGHT_COEF)
