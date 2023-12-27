from useful_funcs import *
from settings import *
from menu import *
from traps import *
from set_settings import set_setting


pygame.init()
hero_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
block_names = ([f"{name} Big" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]] +
               [f"{name} Big" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]])
block_images = {key: load_image(rf"Terrain\Square Blocks\{key}.png") for key in block_names}

enemy_names = []


class Block(pygame.sprite.Sprite):
    def __init__(self, block_type, pos_x, pos_y):
        super().__init__(block_group, all_sprites)
        self.image = block_images[block_type]  # строка с названием
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)  # получаем левый топ коорд холста и получаем передвинутый


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
        self.rect = self.image.get_rect().move(pos_x, pos_y)

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

        for block in block_group:
            if self.rect.colliderect(block.rect):
                if self.dx > 0:
                    self.rect.x = block.rect.left - self.rect.width
                else:
                    self.rect.x = block.rect.right
                self.dx = 0

        for trap in trap_group:
            if self.rect.colliderect(trap.rect):
                if trap.check_hit(self) == 'Hit' and not self.invincible:  # TODO пофиксить шарики с шипами
                    self.hp -= 1
                    self.invincible = IFRAMES
                if self.dx > 0 or self.direction == 'right':
                    self.rect.x = trap.rect.left - self.rect.width
                else:
                    self.rect.x = trap.rect.right
                self.dx = -(self.dx)

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

        for trap in trap_group:
            if self.rect.colliderect(trap.rect):
                if trap.check_hit(self) == 'Hit' and not self.invincible:
                    self.hp -= 1
                    self.invincible = IFRAMES
                if self.dy > 0:
                    self.rect.y = trap.rect.top - self.rect.height
                else:
                    self.rect.y = trap.rect.bottom
                self.cur_jump_height = MAX_JUMP_HEIGHT
                self.dy = -(self.dy)

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
            self.dy += 1

        if scancode[KEY_BINDS["KEY_UP"]]:
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

        if scancode[KEY_BINDS["KEY_RIGHT"]]:
            self.direction = 'right'
            if self.on_ground:
                self.dx = min(MAX_DX, self.dx + GROUND_DX)
            else:
                self.dx = min(MAX_DX, max(1.0, self.dx + AIR_DX))
            if self.dx >= 0:
                has_resistance = 0

        if scancode[KEY_BINDS["KEY_LEFT"]]:
            self.direction = 'left'
            if self.on_ground:
                self.dx = max(-MAX_DX, self.dx - GROUND_DX)
            else:
                self.dx = max(-MAX_DX, min(-1.0, self.dx - AIR_DX))
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

        if self.on_ground:
            self.dy = min(self.dy, 0)
            self.cur_jump_height = 0
            self.jump_number = 0

        if self.dy != 0:
            self.on_ground = False

        self.set_image()
        self.invincible = max(0, self.invincible - 1)


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
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 1.5)


dragon = Hero("Mask Dude", 50, 50)
for i in range(20):
    block = Block("Autumn Big", 0 + i * 48, 500)

from random import randint

for i in range(20):
    block = SpikedBall(randint(0, 740), randint(0, 540), length=200, traectory=(0.5, 0.5))

running = True


while True:
    start = start_screen()
    if start:
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
            trap_group.update()
            hero_group.update(pygame.key.get_pressed())
            all_sprites.draw(screen)
            hero_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
    elif start is None:
        set_setting()
pygame.quit()
