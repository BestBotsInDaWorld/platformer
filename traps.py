import pygame
import os
from math import hypot
from settings import all_sprites, WIDTH, HEIGHT
from useful_funcs import load_image, cut_sheet
trap_group = pygame.sprite.Group()
# ссылки на изображения ловушек
trap_images = {key: dict(map(lambda x: (x.split(".")[0], rf"Traps\{key}\{x}"),
                             os.listdir(rf"data\Traps\{key}"))) for key in os.listdir(rf"data/Traps")}
with open("sheet_cuts.txt", "r") as image_file:
    for line in image_file.readlines():
        line = line.strip().split(";")
        if line[1] == "All Directions":
            for direction in ["Left", "Right", "Up", "Down"]:
                trap_images[line[0]][direction] = cut_sheet(load_image(trap_images[line[0]][direction]), int(line[2]),
                                                            int(line[3]))
        elif line[1] == "All Directions On":
            for direction in ["Left On", "Right On", "Up On", "Down On"]:
                if direction == "Left On" or direction == "Right On":
                    trap_images[line[0]][direction] = cut_sheet(load_image(trap_images[line[0]][direction]),
                                                                int(line[3]),
                                                                int(line[2]))
                else:
                    trap_images[line[0]][direction] = cut_sheet(load_image(trap_images[line[0]][direction]),
                                                                int(line[2]),
                                                                int(line[3]))

                if "Left" in direction or "Down" in direction:
                    trap_images[line[0]][direction].reverse()
        else:
            trap_images[line[0]][line[1]] = cut_sheet(load_image(trap_images[line[0]][line[1]]),
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


class Spike(Trap):
    def __init__(self, pos_x, pos_y):
        super().__init__("Spike", pos_x, pos_y)
        self.hit_type = 'Static_Hit'


class SpikedBall(Trap):
    def __init__(self, pos_x, pos_y, traectory=(1, 0), velocity=2, before_start=0, length=300):
        super().__init__("Spiked Ball", pos_x, pos_y)
        self.image = self.frames['On'][0]

        self.edge = (pos_x, pos_y)
        self.dx, self.dy = traectory[0] * velocity, traectory[1] * velocity
        self.length = length
        self.cur_way = 0

        self.hit_type = 'Through_Hit'

        self.before_start = before_start
        self.frequency = 1

    def update(self, **kwargs):
        if not self.before_start:
            self.rect = self.rect.move(self.dx, self.dy)
            self.cur_way += hypot(self.dx, self.dy)
            if self.cur_way > self.length:
                self.dx *= -1
                self.dy *= -1
                self.cur_way = 0

            self.animation()

        self.before_start = max(self.before_start - 1, 0)


class Saw(Trap):
    def __init__(self, pos_x, pos_y, traectory=(1, 0), velocity=2, before_start=0, length=300):
        super().__init__("Saw", pos_x, pos_y)
        self.edge = (pos_x, pos_y)
        self.dx, self.dy = traectory[0] * velocity, traectory[1] * velocity
        self.before_start = before_start
        self.length = length
        self.cur_way = 0
        self.hit_type = 'Through_Hit'

    def update(self, **kwargs):
        if not self.before_start:
            self.rect = self.rect.move(self.dx, self.dy)
            self.cur_way += hypot(self.dx, self.dy)
            if self.cur_way > self.length:
                self.dx *= -1
                self.dy *= -1
                self.cur_way = 0

            self.rect = self.image.get_rect(center=self.rect.center)
            self.animation()
        self.before_start = max(self.before_start - 1, 0)


class DartTrap(Trap):
    def __init__(self, pos_x, pos_y, direction="Right", arrow_velocity=5, before_start=0, shot_delay=120):
        super().__init__("Dart Trap", pos_x, pos_y)
        self.image = self.frames[direction][0]
        self.hit_type = 'Static_Hit'
        self.direction = direction
        self.arrow_velocity = arrow_velocity
        self.before_start = before_start
        self.shot_delay = shot_delay
        self.cur_shot_delay = 0

    def update(self, **kwargs):
        if not self.before_start:
            if not self.cur_shot_delay:
                Arrow(self.rect.x, self.rect.y, self.direction, self.arrow_velocity)
            self.cur_shot_delay = (self.cur_shot_delay + 1) % self.shot_delay
        self.before_start = max(self.before_start - 1, 0)


class Arrow(Trap):
    def __init__(self, pos_x, pos_y, direction, arrow_velocity):

        super().__init__("Arrow", pos_x, pos_y)
        self.arrow_velocity = arrow_velocity
        self.image = self.frames[direction][0]
        self.direction = direction
        self.hit_type = 'Through_Hit'

    def update(self, **kwargs):
        hero, blocks = kwargs["hero"], kwargs["blocks"]
        self.move_towards_direction(direction=self.direction, velocity=self.arrow_velocity)
        if abs(self.rect.x - hero.rect.x) > WIDTH * 2 or abs(self.rect.y - hero.rect.y) > HEIGHT * 2:
            self.kill()
        for block in blocks:
            if self.rect.colliderect(block.rect):
                self.kill()

    def check_destruction(self):
        self.kill()


class FireMaker(Trap):
    def __init__(self, pos_x, pos_y, before_start=0, shot_delay=60, warning_time=32, damaging_time=60):
        super().__init__("Fire Maker", pos_x, pos_y)
        self.hit_type = False
        self.before_start = before_start
        self.shot_delay = shot_delay
        self.warning_time = warning_time
        self.damaging_time = damaging_time
        self.half_cycle = self.shot_delay + self.warning_time + self.warning_time

    def update(self, **kwargs):
        if not self.before_start:
            if self.shot_delay + self.warning_time <= self.cur_frame < self.half_cycle + self.damaging_time:
                if self.shot_delay + self.warning_time == self.cur_frame:
                    Fire(self.rect.x, self.rect.y - self.rect.height, self.damaging_time)
                self.animation('Damaging')
            elif self.shot_delay <= self.cur_frame < self.half_cycle + self.damaging_time + self.warning_time:
                self.animation('Warning')
            else:
                self.animation('Delay')
            self.cur_frame = (self.cur_frame + 1) % (self.half_cycle * 2)
        self.before_start = max(self.before_start - 1, 0)

    def animation(self, state):
        if state == 'Damaging':
            if self.cur_frame < self.half_cycle:
                current = self.cur_frame - self.shot_delay - self.warning_time
            else:
                current = self.damaging_time - (self.cur_frame - self.half_cycle) - 1
            self.image = self.frames['On'][current // (self.damaging_time // 3)]
        elif state == 'Warning':
            if self.cur_frame < self.half_cycle:
                current = self.cur_frame - self.shot_delay
            else:
                current = self.warning_time - (self.cur_frame - self.half_cycle - self.damaging_time) - 1
            self.image = self.frames['Hit'][current // (self.warning_time // 4)]
        else:
            self.image = self.frames['Idle'][0]


class Fire(Trap):
    def __init__(self, pos_x, pos_y, damaging_time=60):
        super().__init__("Fire", pos_x, pos_y)
        self.damaging_time = damaging_time * 2
        self.hit_type = 'Through_Hit'

    def update(self, **kwargs):
        if self.cur_frame == self.damaging_time:
            self.kill()
        if self.cur_frame < self.damaging_time // 2:
            self.image = self.frames['On'][self.cur_frame // (self.damaging_time // 3)]
        else:
            self.image = self.frames['On'][(self.damaging_time - (self.cur_frame - self.damaging_time // 2) - 1)
                                           // (self.damaging_time // 3)]
        self.cur_frame += 1


class Platform(Trap):
    def __init__(self, pos_x, pos_y, traectory=(1, 0), velocity=2, before_start=0, length=300, variation='Brown'):
        super().__init__("Platform", pos_x, pos_y)
        self.image = self.frames[f'{variation} On'][0]
        self.variation = variation

        self.edge = (pos_x, pos_y)
        self.dx, self.dy = traectory[0] * velocity, traectory[1] * velocity
        self.length = length
        self.cur_way = 0

        self.hit_type = False

        self.before_start = before_start
        self.frequency = 1

        self.standing_objects = []

    def update(self, **kwargs):
        if not self.before_start:
            self.rect = self.rect.move(self.dx, self.dy)
            for object in self.standing_objects:
                object.rect = object.rect.move(self.dx, self.dy)
            self.cur_way += hypot(self.dx, self.dy)
            if self.cur_way > self.length:
                self.dx *= -1
                self.dy *= -1
                self.cur_way = 0

            self.animation(f'{self.variation} On')

        self.before_start = max(self.before_start - 1, 0)

    def fix_standing(self, object):
        if object.rect.colliderect(self.rect.move(0, -1)):
            if object not in self.standing_objects:
                self.standing_objects.append(object)
            return True
        else:
            if object in self.standing_objects:
                self.standing_objects.remove(object)
            return False


class Trampoline(Trap):
    def __init__(self, pos_x, pos_y, direction="Up", bounce_speed=10):
        super().__init__("Trampoline", pos_x, pos_y)
        self.image = self.frames[f'{direction}'][0]
        self.bounce_speed = bounce_speed
        self.direction = direction
        self.activated = False
        self.frequency = 2

        self.hit_type = "Special"

    def update(self, **kwargs):
        if self.cur_frame:
            self.animation(f'{self.direction} On')
        else:
            self.hit_type = "Special"

    def special_behaviour(self, object):
        self.cur_frame = 1
        self.hit_type = "Inactive"
        if self.direction == "Up":
            object.dy += -self.bounce_speed  # TODO изменить если потребуется
        elif self.direction == "Down":
            object.dy += self.bounce_speed
        elif self.direction == "Left":
            object.dx += -self.bounce_speed
        else:
            object.dx += self.bounce_speed
        if hasattr(object, 'jump_number'):
            object.jump_number = min(object.jump_number, 1)


class JumpRefresher(Trap):
    def __init__(self, pos_x, pos_y, refresh_time=300):
        super().__init__("Jump Refresher", pos_x, pos_y)
        self.image = self.frames['On'][0]
        self.hit_type = "Special"
        self.refresh_time = refresh_time
        self.cur_refresh = 0
        self.frequency = 3

    def update(self, **kwargs):
        if not self.cur_refresh:
            self.animation("On")
        else:
            self.animation("Hit")
            self.cur_refresh += 1
            if self.cur_refresh == self.refresh_time:
                self.cur_refresh = 0
                self.hit_type = "Special"

    def special_behaviour(self, object):
        if hasattr(object, 'jump_number'):
            object.jump_number = min(object.jump_number, 1)
            self.cur_frame = 0
            self.cur_refresh = 1
            self.hit_type = "Inactive"


class FallingPlatform(Trap):
    def __init__(self, pos_x, pos_y, traectory=(1, 0), velocity=1, before_start=0,
                 length=300, before_fall=90, refresh_time=300, falling_time=300):
        super().__init__("Falling Platform", pos_x, pos_y)
        self.image = self.frames['On'][0]

        self.edge = (pos_x, pos_y)
        self.dx, self.dy = traectory[0] * velocity, traectory[1] * velocity
        self.length = length
        self.cur_way = 0

        self.hit_type = False

        self.before_start = before_start
        self.before_fall_cur = 0
        self.before_fall = before_fall
        self.refresh_time = refresh_time
        self.frequency = 3

        self.falling_time = falling_time
        self.falling_time_cur = 0
        self.standing_objects = []

    def update(self, **kwargs):
        if not self.before_start:
            if self.before_fall_cur != self.before_fall:
                self.rect = self.rect.move(self.dx, self.dy)
                for object in self.standing_objects:
                    object.rect = object.rect.move(self.dx, self.dy)
                self.cur_way += hypot(self.dx, self.dy)
                if self.cur_way > self.length:
                    self.dx *= -1
                    self.dy *= -1
                    self.cur_way = 0

                if self.before_fall_cur:
                    self.before_fall_cur += 1
            else:
                self.hit_type = "Inactive"
                self.falling_time_cur += 1
                if self.falling_time_cur < self.falling_time // 2:
                    self.rect = self.rect.move(0, abs(self.dy) * 4)
                elif self.falling_time_cur < self.falling_time:
                    self.rect = self.rect.move(0, -abs(self.dy) * 4)
                else:
                    self.falling_time_cur = 0
                    self.before_fall_cur = 0
                    self.hit_type = False
            self.animation('On')

        self.before_start = max(self.before_start - 1, 0)

    def fix_standing(self, object):
        if self.hit_type == "Inactive":
            self.standing_objects = []
            return False
        if object.rect.colliderect(self.rect.move(0, -1)):
            if object not in self.standing_objects:
                self.standing_objects.append(object)
            self.before_fall_cur = max(self.before_fall_cur, 1)
            return True
        else:
            if object in self.standing_objects:
                self.standing_objects.remove(object)
            return False