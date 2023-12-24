import os
import sys
import pygame
from useful_funcs import *
from settings import KEY_BINDS

pygame.init()

FPS = 60
WIDTH = 800
HEIGHT = 600
GRAVITY = 0.25
MAX_JUMP_HEIGHT = 80
RESISTANCE = 0.25
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # экран
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
block_names = ([f"{name} Big" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]] +
              [f"{name} Big" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]])
block_images = {key: load_image(rf"Terrain\Square Blocks\{key}.png") for key in block_names}


class Block(pygame.sprite.Sprite):
    def __init__(self, block_type, pos_x, pos_y):
        super().__init__(block_group, all_sprites)
        self.image = block_images[block_type]  # строка с названием
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)  # получаем левый топ коорд холста и получаем передвинутый


class Hero(pygame.sprite.Sprite):
    def __init__(self, character, x, y):
        super().__init__(hero_group, all_sprites)

        path = rf"Main Characters\{character}\\"

        self.frames_forward = {"Run": self.cut_sheet(load_image(path + "Run.png"), 12, 1),
                               "Fall": self.cut_sheet(load_image(path + "Fall.png"), 1, 1),
                               "Hit": self.cut_sheet(load_image(path + "Hit.png"), 7, 1),
                               "Idle": self.cut_sheet(load_image(path + "Idle.png"), 11, 1),
                               "Jump": self.cut_sheet(load_image(path + "Jump.png"), 1, 1),
                               "Double Jump": self.cut_sheet(load_image(path + "Double Jump.png"), 6, 1)}
        self.frames_backwards = {key: [pygame.transform.flip(self.frames_forward[key][i], True, False)
                                       for i in range(len(self.frames_forward[key]))]
                                 for key in self.frames_forward.keys()}

        self.action = "Idle"

        self.direction = 'right'
        self.dx = 0

        self.dy = 0
        self.jump_number = 0
        self.jump_increase = 0
        self.cur_jump_height = 0
        self.on_ground = False

        self.cur_frame = 0
        self.image = self.frames_forward["Run"][self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        cycle = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frame = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                frame.set_colorkey(frame.get_at((0, 0)))
                cycle.append(frame)
        return cycle

    def set_image(self, direction, action):
        if self.direction == 'right':
            self.image = self.frames_forward[action][self.cur_frame]
        else:
            self.image = self.frames_backwards[action][self.cur_frame]


    def move_with_collision(self):
        self.rect = self.rect.move(self.dx, 0)
        for block in block_group:
            if self.rect.colliderect(block.rect):
                if self.dx > 0:
                    self.rect.x = block.rect.left - self.rect.width
                else:
                    self.rect.x = block.rect.right
                self.dx = 0
        self.rect = self.rect.move(0, self.dy)
        for block in block_group:
            if self.rect.colliderect(block.rect):
                if self.dy > 0:
                    self.rect.y = block.rect.top - self.rect.height
                    self.on_ground = True
                else:
                    self.rect.y = block.rect.bottom
                    self.cur_jump_height = MAX_JUMP_HEIGHT
                self.dy = 0
        self.on_ground = False
        underground_rect = self.rect.move(0, 1)
        for block in block_group:
            if underground_rect.colliderect(block.rect):
                self.on_ground = True
                break


    def update(self, *args):
        scancode: pygame.key.ScancodeWrapper = args[0]

        has_resistance = 1
        has_gravity = 1

        if scancode[KEY_BINDS["KEY_DOWN"]]:
            self.dy += 0.1

        if scancode[KEY_BINDS["KEY_UP"]]:
            self.jump_number = max(1, self.jump_number)
            if self.cur_jump_height != MAX_JUMP_HEIGHT and not (not self.jump_increase and self.cur_jump_height > 0):
                self.jump_increase = True
                self.dy = -5
                self.cur_jump_height = min(float(MAX_JUMP_HEIGHT), self.cur_jump_height - self.dy)
                has_gravity = False
            elif not self.jump_increase:
                if self.jump_number == 1:
                    self.jump_number += 1
                    self.cur_jump_height = 0
        else:
            self.jump_increase = False

        if scancode[KEY_BINDS["KEY_RIGHT"]]:
            self.direction = 'right'
            if self.on_ground:
                self.dx = min(5.0, self.dx + 0.15)
            else:
                self.dx = min(5.0, max(1.0, self.dx + 0.1))
            if self.dx >= 0:
                has_resistance = 0

        if scancode[KEY_BINDS["KEY_LEFT"]]:
            self.direction = 'left'
            if self.on_ground:
                self.dx = max(-5.0, self.dx - 0.15)
            else:
                self.dx = max(-5.0, min(-1.0, self.dx - 0.1))
            if self.dx <= 0:
                has_resistance = 0

        if has_resistance and self.dy == 0:
            if self.dx < 0:
                self.dx = min(0.0, self.dx + RESISTANCE)
            else:
                self.dx = max(0.0, self.dx - RESISTANCE)

        if has_gravity:
            self.dy = min(5.0, self.dy + GRAVITY)

        self.move_with_collision()

        if self.on_ground:
            self.dy = min(self.dy, 0)
            self.cur_jump_height = 0
            self.jump_number = 0

        if self.dy < 0:
            self.on_ground = False
            if self.jump_number == 1:
                self.action = "Jump"
            else:
                self.action = "Double Jump"
        elif self.dy > 0:
            self.on_ground = False
            self.action = "Fall"
        elif self.dx != 0:
            self.action = "Run"
        else:
            self.action = "Idle"

        self.cur_frame = (self.cur_frame + 1) % len(self.frames_forward[self.action])
        self.set_image(self.direction, self.action)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 6)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 1.2)


dragon = Hero("Mask Dude", 50, 50)
for i in range(20):
    block = Block("Autumn Big", 0 + i * 48, 500)

from random import randint
for i in range(20):
    block = Block("Fantasy Big", randint(0, 740), randint(0, 540))
running = True
start = True


def terminate():
    pygame.quit()
    sys.exit()


while running:
    camera = Camera()
    camera.update(dragon)
    for sprite in all_sprites:
        camera.apply(sprite)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color("orange"))
    hero_group.update(pygame.key.get_pressed())
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
