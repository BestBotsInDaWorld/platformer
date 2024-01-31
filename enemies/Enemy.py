import pygame
import os
from math import hypot
from settings import (all_sprites, enemy_group, nearest_blocks, block_group, WIDTH,
                      HEIGHT, GRAVITY, sound_lib, ENEMY_DEFEAT_BOUNCE, WIDTH_COEF, HEIGHT_COEF)
from useful_funcs import load_image, cut_sheet
from random import randint, choice
# ссылки на изображения врагов

enemy_images = {key: dict(map(lambda x: (x.split(".")[0], rf"Enemies\{key}\{x}"),
                             os.listdir(rf"data\Enemies\{key}")))
               for key in os.listdir(rf"data\Enemies")}
with open(rf"enemy_sheet_cuts.txt", "r") as image_file:
    for line in image_file.readlines():
        line = line.strip().split(";")
        enemy_images[line[0]][line[1]] = cut_sheet(load_image(enemy_images[line[0]][line[1]]),
                                                   int(line[2]), int(line[3]))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, pos_x, pos_y, precise_coords=False):
        super().__init__(enemy_group, all_sprites)
        self.frames_forward = enemy_images[enemy_type]
        self.frames_backwards = {key: [pygame.transform.flip(self.frames_forward[key][i], True, False)
                                       for i in range(len(self.frames_forward[key]))]
                                 for key in self.frames_forward.keys()}
        self.image = self.frames_forward["Idle"][0]
        self.mask = pygame.mask.from_surface(self.image)
        if not precise_coords:
            self.rect: pygame.Rect = self.image.get_rect().move(pos_x * WIDTH_COEF, pos_y * HEIGHT_COEF)
        else:
            self.rect: pygame.Rect = self.image.get_rect().move(pos_x, pos_y)
        self.action = "Idle"
        self.direction = 'left'

        self.dx = 0

        self.dy = 0
        self.on_ground = False
        self.alive = True

        self.hp = 1
        self.invincible = 0

        self.damaged = False
        self.cur_frame = 0
        self.frequency = 2

        self.is_active = True

    def check_hit(self, hero, direction="vertical"):  # проверка удара по врагу при вертикальном перемещении перса
        if self.alive:
            if not hero.invincible:
                if direction == "vertical":
                    if hero.rect.top < self.rect.top:
                        self.hp -= 1
                        self.cur_frame = 0
                        self.damaged = True
                        if not self.hp:
                            self.alive = False
                        sound_lib["enemy_hit"].play()
                        return "Enemy_Damaged"
                    else:
                        return "Hero_Damaged"
                elif direction == "horizontal":
                    return "Hero_Damaged"
            else:
                self.hp -= 1
                self.cur_frame = 0
                self.damaged = True
                if not self.hp:
                    self.alive = False
                return "Enemy_Damaged"
        else:
            return False

    def animation(self, animation_sprites='Idle'):  # On по умолчанию
        self.cur_frame = (self.cur_frame + 1) % (len(self.frames_forward[animation_sprites]) * self.frequency)
        if self.direction == 'left':
            self.image = self.frames_forward[animation_sprites][self.cur_frame // self.frequency]
        else:
            self.image = self.frames_backwards[animation_sprites][self.cur_frame // self.frequency]

    def death(self):
        self.animation('Hit')
        if not self.cur_frame:
            self.kill()

    def check_destruction(self):
        return False

    def fall(self):
        self.dy = max(1 * HEIGHT_COEF, self.dy + GRAVITY)
        self.rect = self.rect.move(0, self.dy)
        for block in block_group:
            if self.rect.colliderect(block):
                self.rect.y = block.rect.y - self.rect.height
                self.dy = 0
                self.on_ground = True
                return True
        return False

    def under_map_check(self, start):
        if self.rect.y - start.y > HEIGHT * 2:
            self.kill()

    def check_bottom(self, hero):
        checking_copy = self.rect.move(-self.dx, -self.dy)
        if self.rect.left < hero.rect.left:
            if (self.rect.left - checking_copy.left == 0 or hero.rect.left - checking_copy.left == 0 or
                    self.rect.right <= hero.rect.right):
                return True
            elif (checking_copy.bottom - self.rect.bottom) / (self.rect.left - checking_copy.left) <= (
                    checking_copy.bottom - hero.rect.bottom) / (hero.rect.left - checking_copy.left):
                return True
        elif self.rect.right > hero.rect.right:
            if (self.rect.right - checking_copy.right == 0 or checking_copy.right - hero.rect.right == 0 or
                    self.rect.left >= hero.rect.left):
                return True
            elif (checking_copy.bottom - self.rect.bottom) / (checking_copy.right - self.rect.right) <= (
                    checking_copy.bottom - hero.rect.bottom) / (checking_copy.right - hero.rect.right):
                return True
        else:
            return True
        return False

    def check_self_hit(self, hero):
        if self.rect.colliderect(hero.rect) and self.rect.bottom > hero.rect.bottom:
            if self.check_bottom(hero) and pygame.sprite.collide_mask(self, hero):
                hero.dy = -ENEMY_DEFEAT_BOUNCE
                hero.jump_number = 1
                self.alive = False
                sound_lib["enemy_hit"].play()
                return True
        return False