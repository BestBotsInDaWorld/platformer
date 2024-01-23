from create_level import create_level
from useful_funcs import *
from settings import *
from menu import *
from traps import *
from blocks import Block
from config_change import set_settings
pygame.init()
hero_group = pygame.sprite.Group()

class Hero(pygame.sprite.Sprite):
    def __init__(self, character, pos_x, pos_y):
        super().__init__(hero_group, all_sprites)

        path = rf"Main Characters\{character}\\"

        self.frames_forward = {"Run": cut_sheet(load_image(path + "Run.png"), 12, 1),
                               "Fall": cut_sheet(load_image(path + "Fall.png"), 1, 1),
                               "Hit": cut_sheet(load_image(path + "Hit.png"), 7, 1),
                               "Idle": cut_sheet(load_image(path + "Idle.png"), 11, 1),
                               "Jump": cut_sheet(load_image(path + "Jump.png"), 1, 1),
                               "Double Jump": cut_sheet(load_image(path + "Double Jump.png"), 6, 1)}
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

        self.hp = 100
        self.invincible = 0

        self.cur_frame = 0
        self.image = self.frames_forward["Run"][self.cur_frame]
        self.rect: pygame.Rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def check_masks(self, other):
        if self.rect.colliderect(other.rect):
            if pygame.sprite.collide_mask(self, other):
                return True
        return False

    def set_image(self):

        if self.invincible:
            self.action = "Hit"
            self.cur_frame = len(self.frames_forward["Hit"]) - self.invincible // 3 - 1

        elif self.dy < 0:
            if self.jump_number == 1:
                self.action = "Jump"
            else:
                self.action = "Double Jump"
        elif self.dy > 0:
            self.action = "Fall"
        elif self.dx != 0:
            self.action = "Run"
        else:
            self.action = "Idle"

        self.cur_frame %= len(self.frames_forward[self.action])
        if self.direction == 'right':
            self.image = self.frames_forward[self.action][self.cur_frame]
        else:
            self.image = self.frames_backwards[self.action][self.cur_frame]
        self.cur_frame += 1

    def move_with_collision(self):
        self.rect = self.rect.move(self.dx, 0)
        cur_hit = False
        for block in block_group:
            if self.rect.colliderect(block.rect):
                self.change_collision_x(block)
                self.dx = 0

        for trap in trap_group:
            if self.check_masks(trap):
                if trap.hit_type == 'Static_Hit':
                    self.damage_try()
                    self.change_collision_x(trap)
                    self.dx = -(self.dx)
                elif trap.hit_type == 'Through_Hit':
                    if self.damage_try():
                        cur_hit = True
                        self.dx = -(self.dx)
                elif trap.hit_type == "Special":
                    trap.special_behaviour(self)
                trap.check_destruction()
            elif not trap.hit_type and self.rect.colliderect(trap.rect):
                self.change_collision_x(trap)
                self.dx = 0


        self.rect = self.rect.move(0, self.dy)

        for block in block_group:
            if self.rect.colliderect(block.rect):
                self.change_collision_y(block)
                self.dy = 0

        for trap in trap_group:
            if self.check_masks(trap) and trap.hit_type:
                if trap.hit_type == 'Static_Hit':
                    self.damage_try()
                    self.change_collision_y(trap)
                    self.dy = -(self.dy)
                    self.cur_jump_height = MAX_JUMP_HEIGHT
                elif trap.hit_type == 'Through_Hit':
                    if self.damage_try() or cur_hit:  # под неуязвимостью не отталкивает
                        self.dy = -(self.dy)
                        self.cur_jump_height = MAX_JUMP_HEIGHT
                trap.check_destruction()

            elif self.rect.colliderect(trap.rect) and not trap.hit_type:
                self.change_collision_y(trap)
                self.dy = 0


    def damage_try(self):
        if not self.invincible:
            self.hp -= 1
            self.invincible = IFRAMES
            return True
        return False

    def change_collision_x(self, object):
        if self.rect.left < object.rect.left:
            self.rect.x = object.rect.left - self.rect.width
        else:
            self.rect.x = object.rect.right

    def change_collision_y(self, object):
        if self.rect.top < object.rect.top:
            self.rect.y = object.rect.top - self.rect.height
        else:
            self.rect.y = object.rect.bottom
        self.cur_jump_height = MAX_JUMP_HEIGHT

    def update(self, *args):
        scancode: pygame.key.ScancodeWrapper = args[0]


        has_resistance = 1
        has_gravity = 1

        if scancode[KEY_BINDINGS["KEY_DOWN"]]:
            self.dy += 1

        if scancode[KEY_BINDINGS["KEY_UP"]]:
            self.jump_number = max(1, self.jump_number)
            if self.cur_jump_height != MAX_JUMP_HEIGHT and not (not self.jump_increase and self.cur_jump_height > 0):
                self.jump_increase = True
                self.dy = -MAX_DY
                self.cur_jump_height = min(float(MAX_JUMP_HEIGHT), self.cur_jump_height - self.dy)
                has_gravity = False
            elif not self.jump_increase:
                if self.jump_number == 1:
                    self.jump_number += 1
                    self.cur_jump_height = 0
        else:
            self.jump_increase = False

        if scancode[KEY_BINDINGS["KEY_RIGHT"]]:
            self.direction = 'right'
            if self.on_ground:
                if self.dx <= MAX_DX:  # не действуют трамплины и т.д.
                    self.dx = min(MAX_DX, self.dx + GROUND_DX)
                else:
                    self.dx = min(MAX_DX * 2, self.dx + GROUND_DX)
            else:
                if self.dx <= MAX_DX:
                    self.dx = min(MAX_DX, max(1.0, self.dx + AIR_DX))
                else:
                    self.dx = min(MAX_DX * 2, self.dx + AIR_DX)
            if self.dx >= 0:
                has_resistance = 0

        if scancode[KEY_BINDINGS["KEY_LEFT"]]:
            self.direction = 'left'
            if self.on_ground:
                if self.dx >= -MAX_DX:
                    self.dx = max(-MAX_DX, self.dx - GROUND_DX)
                else:
                    self.dx = max(-MAX_DX * 2, self.dx - GROUND_DX)
            else:
                if self.dx >= -MAX_DX:
                    self.dx = max(-MAX_DX, min(-1.0, self.dx - AIR_DX))
                else:
                    self.dx = max(-MAX_DX * 2, self.dx - AIR_DX)
            if self.dx <= 0:
                has_resistance = 0

        if has_resistance and self.dy == 0:
            if self.dx < 0:
                self.dx = min(0.0, self.dx + RESISTANCE)
            else:
                self.dx = max(0.0, self.dx - RESISTANCE)

        if has_gravity:
            self.dy = min(MAX_DY, self.dy + GRAVITY)

        self.move_with_collision()

        fall_without_jump = True if self.on_ground and not self.jump_number else False
        self.on_ground = False
        underground_rect = self.rect.move(0, 1)
        for block in block_group:  # проверка остановки на блоке
            if underground_rect.colliderect(block.rect):
                self.on_ground = True
                fall_without_jump = False
                break
        for trap in trap_group:  # проверка остановки на платформах/неактивных ловушках
            if trap.fix_standing(self):
                self.on_ground = True
                fall_without_jump = False
                break
        if fall_without_jump:
            self.cur_jump_height = MAX_JUMP_HEIGHT

        if self.on_ground:
            self.dy = min(self.dy, 0)
            self.cur_jump_height = 0
            self.jump_number = 0

        self.set_image()
        self.invincible = max(0, self.invincible - 1)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 6 -
                    min(WIDTH // 6, abs(start_point.left - target.rect.left)))
        start_point.x += self.dx
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 1.2)
        start_point.y += self.dy


dragon = Hero("Mask Dude", 50, 50)
start_point = pygame.Rect(0, HEIGHT, 1, 1)

for i in range(20):
    block = Block.Block("Autumn Big", 0 + i * 48, 400)

from random import randint, choice

#  for i in range(20):
#     block = SpikedBall(randint(0, 740), randint(0, 300), traectory=(1, 1), velocity=0.5, before_start=0, length=200)
#  for i in range(20):
#      block = DartTrap(randint(0, 740), randint(0, 300), direction="Up")
#  for i in range(5):
#      block = FallingPlatform.FallingPlatform(randint(0, 740), randint(0, 300), traectory=(0.5, 0.5), velocity=2)

create_level()
running = True
KEY_BINDINGS = get_keys()
load_ost("ost_1.mp3")

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
    trap_group.update(hero=dragon, blocks=block_group)
    all_sprites.draw(screen)
    hero_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
