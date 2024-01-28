from traps.Trap import *


class Saw(Trap):
    def __init__(self, pos_x, pos_y, traectory=(1, 0), velocity=2, before_start=0, length=300):
        super().__init__("Saw", pos_x, pos_y)
        self.dx, self.dy = traectory[0] * velocity * WIDTH_COEF, traectory[1] * velocity * HEIGHT_COEF
        self.before_start = before_start
        if abs(self.dx) > abs(self.dy):
            if self.dy == 0:
                coef = 0
            else:
                coef = abs(self.dx / self.dy)
            self.length = length * (1 / (coef + 1)) * WIDTH_COEF + length * (coef / (coef + 1)) * HEIGHT_COEF
        else:
            if self.dx == 0:
                coef = 0
            else:
                coef = abs(self.dy / self.dx)
            self.length = length * (coef / (coef + 1)) * WIDTH_COEF + length * (1 / (coef + 1)) * HEIGHT_COEF
        self.cur_way = 0
        self.hit_type = 'Through_Hit'

    def update(self, **kwargs):
        if not self.before_start:
            copy_rect = self.rect.move(self.dx, self.dy)
            self.cur_way += hypot(self.rect.right - copy_rect.right, self.rect.bottom - copy_rect.bottom)
            self.rect = copy_rect
            if self.cur_way > self.length:
                self.dx *= -1
                self.dy *= -1
                self.cur_way = 0

            self.animation()
        self.before_start = max(self.before_start - 1, 0)