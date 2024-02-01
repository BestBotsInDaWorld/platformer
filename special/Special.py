import pygame
import os
from math import hypot
from settings import all_sprites, special_group, WIDTH, HEIGHT, sound_lib, WIDTH_COEF, HEIGHT_COEF, HP_CAP
from useful_funcs import load_image, cut_sheet
from random import randint
# ссылки на изображения ловушек

special_images = {key: dict(map(lambda x: (x.split(".")[0], rf"Items\Checkpoints\{key}\{x}"),
                                os.listdir(rf"data\Items\Checkpoints\{key}")))
                  for key in os.listdir(rf"data\Items\Checkpoints")}

with open(rf"special_sheet_cuts.txt", "r") as image_file:
    for line in image_file.readlines():
        line = line.strip().split(";")
        special_images[line[0]][line[1]] = cut_sheet(load_image(special_images[line[0]][line[1]], ),
                                                     int(line[2]), int(line[3]))


# TODO прописывать в sheet_cuts спрайты
class Special(pygame.sprite.Sprite):
    def __init__(self, special_type, pos_x, pos_y):
        super().__init__(special_group, all_sprites)
        self.frames = special_images[special_type]
        self.image = self.frames["Idle"][0]
        self.rect: pygame.Rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.cur_frame = 0
        self.frequency = 2

    def animation(self, animation_sprites='On'):  # On по умолчанию
        self.cur_frame = (self.cur_frame + 1) % (len(self.frames[animation_sprites]) * self.frequency)
        self.image = self.frames[animation_sprites][self.cur_frame // self.frequency]