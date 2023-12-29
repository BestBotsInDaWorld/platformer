import pygame
import os
from math import hypot
from settings import all_sprites
from useful_funcs import load_image, cut_sheet
trap_group = pygame.sprite.Group()
# ссылки на изображения ловушек
trap_images = {key: dict(map(lambda x: (x.split(".")[0], rf"Traps\{key}\{x}"),
                             os.listdir(rf"data\Traps\{key}"))) for key in os.listdir(rf"data\Traps")}
with open("sheet_cuts.txt", "r") as image_file:
    for line in image_file.readlines():
        line = line.strip().split(";")
        trap_images[line[0]][line[1]] = cut_sheet(load_image(trap_images[line[0]][line[1]]), int(line[2]), int(line[3]))


class Trap(pygame.sprite.Sprite):
    def __init__(self, trap_type, pos_x, pos_y):
        super().__init__(trap_group, all_sprites)
        self.frames = trap_images[trap_type]
        self.image = self.frames["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect: pygame.Rect = self.image.get_rect().move(pos_x, pos_y)
        self.cur_frame = 0
        self.hit_type = False

        self.cycle_length = len(self.frames.get('On', [1]))
        self.frequency = 1

    def animation(self):
        self.cur_frame = (self.cur_frame + 1) % (self.cycle_length * self.frequency)
        self.image = self.frames['On'][self.cur_frame // self.frequency]

    def shorten_hitbox(self, x, y):
        self.rect.inflate_ip(-x, -y)
        self.rect.move_ip(x, y)


class Spike(Trap):
    def __init__(self, pos_x, pos_y):
        super().__init__("Spike", pos_x, pos_y)
        self.hit_type = 'Static_Hit'


class SpikedBall(Trap):
    def __init__(self, pos_x, pos_y, traectory=(1, 0), velocity=2, delay=0, length=300):
        super().__init__("Spiked Ball", pos_x, pos_y)
        self.image = self.frames['On'][0]

        self.edge = (pos_x, pos_y)
        self.dx, self.dy = traectory[0] * velocity, traectory[1] * velocity
        self.length = length
        self.cur_way = 0

        self.hit_type = 'Through_Hit'

        self.delay = delay
        self.frequency = 1

    def update(self):
        if not self.delay:
            self.rect = self.rect.move(self.dx, self.dy)
            self.cur_way += hypot(self.dx, self.dy)
            if self.cur_way > self.length:
                self.dx *= -1
                self.dy *= -1
                self.cur_way = 0

            self.animation()

        self.delay = max(self.delay - 1, 0)



class Saw(Trap):
    def __init__(self, pos_x, pos_y, traectory=(1, 0), velocity=2, delay=0, length=300):
        super().__init__("Saw", pos_x, pos_y)
        self.edge = (pos_x, pos_y)
        self.dx, self.dy = traectory[0] * velocity, traectory[1] * velocity
        self.delay = delay
        self.length = length
        self.cur_way = 0
        self.hit_type = 'Through_Hit'


    def update(self):
        if not self.delay:
            self.rect = self.rect.move(self.dx, self.dy)
            self.cur_way += hypot(self.dx, self.dy)
            if self.cur_way > self.length:
                self.dx *= -1
                self.dy *= -1
                self.cur_way = 0

            self.rect = self.image.get_rect(center=self.rect.center)
            self.animation()
        self.delay = max(self.delay - 1, 0)