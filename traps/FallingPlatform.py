from traps.Trap import *


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
                    self.rect = self.rect.move(0, max(abs(self.dy), 1) * 4)
                elif self.falling_time_cur < self.falling_time:
                    self.rect = self.rect.move(0, -max(abs(self.dy), 1) * 4)
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