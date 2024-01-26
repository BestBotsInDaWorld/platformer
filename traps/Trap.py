import pygame
import os
from math import hypot
from settings import all_sprites, trap_group, WIDTH, HEIGHT
from useful_funcs import load_image, cut_sheet

# ссылки на изображения ловушек

trap_images = {key: dict(map(lambda x: (x.split(".")[0], rf"Traps\{key}\{x}"),
                             os.listdir(rf"data\Traps\{key}")))
               for key in os.listdir(rf"data\Traps")}

with open(rf"trap_sheet_cuts.txt", "r") as image_file:
    for line in image_file.readlines():
        line = line.strip().split(";")
        if line[1] == "All Directions":
            for direction in ["Left", "Right", "Up", "Down"]:
                trap_images[line[0]][direction] = cut_sheet(load_image(trap_images[line[0]][direction]),
                                                            int(line[2]), int(line[3]))
        elif line[1] == "All Directions On":
            for direction in ["Left On", "Right On", "Up On", "Down On"]:
                if direction == "Left On" or direction == "Right On":
                    trap_images[line[0]][direction] = cut_sheet(load_image(trap_images[line[0]][direction]),
                                                                int(line[3]), int(line[2]))
                else:
                    trap_images[line[0]][direction] = cut_sheet(load_image(trap_images[line[0]][direction]),
                                                                int(line[2]), int(line[3]))

                if "Left" in direction or "Down" in direction:
                    trap_images[line[0]][direction].reverse()
        else:
            trap_images[line[0]][line[1]] = cut_sheet(load_image(trap_images[line[0]][line[1]],),
                                                      int(line[2]), int(line[3]))


# TODO прописывать в sheet_cuts спрайты
class Trap(pygame.sprite.Sprite):
    def __init__(self, trap_type, pos_x, pos_y):
        super().__init__(trap_group, all_sprites)
        self.frames = trap_images[trap_type]
        self.image = self.frames["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect: pygame.Rect = self.image.get_rect().move(pos_x, pos_y)
        self.cur_frame = 0
        self.hit_type = False
        self.dx = 0
        self.dy = 0
        self.frequency = 1

    def animation(self, animation_sprites='On'):  # On по умолчанию
        self.cur_frame = (self.cur_frame + 1) % (len(self.frames[animation_sprites]) * self.frequency)
        self.image = self.frames[animation_sprites][self.cur_frame // self.frequency]

    def shorten_hitbox(self, x, y):
        self.rect.inflate_ip(-x, -y)
        self.rect.move_ip(x, y)

    def move_towards_direction(self, direction, velocity):
        if direction == "Right":
            self.rect.move_ip(velocity, 0)
        elif direction == "Left":
            self.rect.move_ip(-velocity, 0)
        elif direction == "Up":
            self.rect.move_ip(0, -velocity)
        else:
            self.rect.move_ip(0, velocity)

    def check_destruction(self):
        return False

    def fix_standing(self, object):
        return False