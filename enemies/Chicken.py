from enemies.Enemy import *


class Chicken(Enemy):
    def __init__(self, pos_x, pos_y, velocity=2, targeting_range_x=300,
                 targeting_range_y=300, max_running_time=60):
        super().__init__("Chicken", pos_x, pos_y)
        self.dx = -velocity * WIDTH_COEF
        self.walk_velocity = velocity * WIDTH_COEF
        self.running_time = 0
        self.max_running_time = max_running_time
        self.running = False
        self.targeting_range_x = targeting_range_x * WIDTH_COEF
        self.targeting_range_y = targeting_range_y * HEIGHT_COEF

    def update(self, **kwargs):
        if not self.on_ground:
            self.fall()
            return False
        hero = kwargs['hero']
        if not self.alive:
            self.death()
        elif not self.is_active:
            pass
        elif not self.running:
            if abs(self.rect.x - hero.rect.x) <= self.targeting_range_x and abs(
                    self.rect.x - hero.rect.x) <= self.targeting_range_y:
                self.running = True
                sound_lib["chicken_targeting"].play()
                self.direction = 'left' if self.rect.x > hero.rect.x else 'right'
                self.cur_frame = 0
            self.animation('Normal')
        else:
            if self.direction == 'left':
                self.dx = -abs(self.dx)
            else:
                self.dx = abs(self.dx)
            self.animation('Run')
            self.rect = self.rect.move(self.dx, 0)
            if self.check_self_hit(hero):
                return False
            for block in nearest_blocks:
                if self.rect.colliderect(block.rect):
                    if self.rect.right > block.rect.right:
                        self.direction = 'right'
                        self.rect.x = block.rect.right
                    else:
                        self.direction = 'left'
                        self.rect.x = block.rect.left - self.rect.width
                    break
            underground_rect = self.rect.move(-self.rect.width if self.dx < 0 else self.rect.width, 1)
            self.on_ground = False
            for block in nearest_blocks:
                if underground_rect.colliderect(block.rect):
                    self.on_ground = True
                    break
            if not self.on_ground:
                self.direction = 'left' if self.direction == 'right' else 'right'
                self.on_ground = True
            self.running_time += 1
            if self.running_time == self.max_running_time:
                if abs(self.rect.x - hero.rect.x) <= self.targeting_range_x and abs(
                        self.rect.x - hero.rect.x) <= self.targeting_range_y:
                    self.direction = 'left' if self.rect.x > hero.rect.x else 'right'
                else:
                    self.running = False
                self.running_time = 0