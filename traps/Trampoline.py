from traps.Trap import *


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