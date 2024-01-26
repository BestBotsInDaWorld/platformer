import pygame
from settings import block_group, all_sprites
from useful_funcs import load_image
block_names = ([f"{name} Big" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]] +
               [f"{name} Big" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]])
block_images = {key: load_image(rf"Terrain\Square Blocks\{key}.png") for key in block_names}


class Block(pygame.sprite.Sprite):
    def __init__(self, block_type, pos_x, pos_y):
        super().__init__(block_group, all_sprites)
        self.image = block_images[block_type]  # строка с названием
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)  # получаем левый топ коорд холста и получаем передвинутый
        self.dx = 0
        self.dy = 0
