from traps.Trap import *


class Platform(Trap):
    def __init__(self, pos_x, pos_y, traectory=(1, 0), velocity=2, before_start=0, length=300, variation='Brown'):
        super().__init__("Platform", pos_x, pos_y)
        self.image = self.frames[f'{variation} On'][0]
        self.variation = variation

        self.edge = (pos_x, pos_y)
        self.dx, self.dy = traectory[0] * velocity * WIDTH_COEF, traectory[1] * velocity * HEIGHT_COEF
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

        self.hit_type = False

        self.before_start = before_start
        self.frequency = 1

        self.standing_objects = []

    def update(self, **kwargs):
        if not self.before_start:
            hero = kwargs['hero']

            self.rect = self.rect.move(self.dx, 0)
            if self.rect.colliderect(hero.rect):
                self.change_collision_x(hero)

            for object in self.standing_objects:
                object.rect = object.rect.move(self.dx, self.dy)
            copy_rect = self.rect.move(self.dx, self.dy)
            self.cur_way += hypot(self.rect.right - copy_rect.right, self.rect.bottom - copy_rect.bottom)
            self.rect = copy_rect
            if self.rect.colliderect(hero.rect):
                self.change_collision_y(hero)
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

    def change_collision_x(self, hero):  # TODO для любых движущихся объектов
        if hero.rect.left < self.rect.left:
            hero.rect.x = self.rect.left - hero.rect.width
        else:
            hero.rect.x = self.rect.right

    def change_collision_y(self, hero):
        if hero.rect.top < self.rect.top:
            hero.rect.y = self.rect.top - hero.rect.height
        else:
            hero.rect.y = self.rect.bottom
        hero.cur_jump_height = hero.MAX_JUMP_HEIGHT