from traps.Trap import *


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