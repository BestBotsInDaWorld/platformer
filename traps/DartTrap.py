from traps.Trap import *


class DartTrap(Trap):
    def __init__(self, pos_x, pos_y, direction="Right", arrow_velocity=5, before_start=0, shot_delay=120):
        super().__init__("Dart Trap", pos_x, pos_y)
        self.image = self.frames[direction][0]
        self.hit_type = 'Static_Hit'
        self.direction = direction
        self.arrow_velocity = arrow_velocity * WIDTH_COEF if direction in ["Left",
                                                                           "Right"] else arrow_velocity * HEIGHT_COEF
        self.before_start = before_start
        self.shot_delay = shot_delay
        self.cur_shot_delay = 0

    def update(self, **kwargs):
        hero = kwargs['hero']
        if not self.before_start:
            if (not self.cur_shot_delay and abs(self.rect.x - hero.rect.x) <= WIDTH * 1.5
                    and abs(self.rect.y - hero.rect.y <= HEIGHT)):
                Arrow(self.rect.x, self.rect.y, self.direction, self.arrow_velocity)
                sound_lib["dart_shot"].play()
            self.cur_shot_delay = (self.cur_shot_delay + 1) % self.shot_delay
        self.before_start = max(self.before_start - 1, 0)


class Arrow(Trap):
    def __init__(self, pos_x, pos_y, direction, arrow_velocity):

        super().__init__("Arrow", pos_x, pos_y, precise_coords=True)
        self.arrow_velocity = arrow_velocity
        self.image = self.frames[direction][0]
        self.direction = direction
        self.hit_type = 'Through_Hit'

    def update(self, **kwargs):
        hero = kwargs["hero"]
        self.move_towards_direction(direction=self.direction, velocity=self.arrow_velocity)
        if abs(self.rect.x - hero.rect.x) > WIDTH * 2 or abs(self.rect.y - hero.rect.y) > HEIGHT * 2:
            self.kill()
        for block in nearest_blocks:
            if self.rect.colliderect(block.rect):
                self.kill()

    def check_destruction(self):
        self.kill()
