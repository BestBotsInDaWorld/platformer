from traps.Trap import *


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
