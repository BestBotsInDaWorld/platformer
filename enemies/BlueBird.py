from enemies.Enemy import *


class BlueBird(Enemy):
    def __init__(self, pos_x, pos_y, velocity=3, traectory=(1, 0), length=300):
        super().__init__("Blue Bird", pos_x, pos_y)
        self.dx, self.dy = traectory[0] * velocity * WIDTH_COEF, traectory[1] * velocity * HEIGHT_COEF
        self.direction = 'left' if self.dx < 0 else 'right'
        self.length_change = hypot(self.dx, self.dy)
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
        self.sound_count = randint(0, 240)

    def update(self, **kwargs):
        hero = kwargs['hero']
        if not self.alive:
            self.death()
        else:
            copy_rect = self.rect.move(self.dx, self.dy)
            self.cur_way += hypot(self.rect.right - copy_rect.right, self.rect.bottom - copy_rect.bottom)
            self.rect = copy_rect
            if self.is_active and self.check_self_hit(hero):
                return False
            if self.cur_way > self.length:
                self.dx *= -1
                self.dy *= -1
                self.cur_way = 0
                self.direction = 'left' if self.direction == 'right' else 'right'
            self.animation('Flying')
            self.sound_count = (self.sound_count + 1) % 240
            if (not self.sound_count and abs(self.rect.x - hero.rect.x) <= WIDTH and
                    abs(self.rect.y - hero.rect.y) <= HEIGHT):
                sound_lib["bird_flying"].play()
