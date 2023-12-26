import pygame
import os
from math import hypot
from settings import all_sprites
from useful_funcs import load_image, cut_sheet
trap_group = pygame.sprite.Group()
trap_images = {key: dict(map(lambda x: (x.split(".")[0], load_image(rf"Traps\{key}\{x}", color_key=-1)),
                             os.listdir(rf"data\Traps\{key}"))) for key in os.listdir(rf"data\Traps")}


class Trap(pygame.sprite.Sprite):
    def __init__(self, trap_type, pos_x, pos_y):
        super().__init__(trap_group, all_sprites)
        self.frames = trap_images[trap_type]
        self.image = self.frames["Idle"]
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.cur_frame = 0
        self.deadly = False

    def check_hit(self, entity):
        return False


class Spikes(Trap):
    def __init__(self, pos_x, pos_y):
        super().__init__("Spikes", pos_x, pos_y)

    def check_hit(self, entity):
        return 'Hit'


class SpikedBall(Trap):
    def __init__(self, pos_x, pos_y, traectory=(1, 0), velocity=2, delay=0, length=300):
        super().__init__("Spiked Ball", pos_x, pos_y)
        self.edge = (pos_x, pos_y)
        self.dx, self.dy = traectory[0] * velocity, traectory[1] * velocity
        self.delay = delay
        self.length = length
        self.cur_way = 0

    def check_hit(self, entity):
        return 'Hit'

    def update(self):
        if not self.delay:
            self.rect = self.rect.move(self.dx, self.dy)
            self.cur_way += hypot(self.dx, self.dy)
            if self.cur_way > self.length:
                self.dx *= -1
                self.dy *= -1
                self.cur_way = 0

            self.rect = self.image.get_rect(center=self.rect.center)
        self.delay = max(self.delay - 1, 0)