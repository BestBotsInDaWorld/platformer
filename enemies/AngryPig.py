from enemies.Enemy import *


class AngryPig(Enemy):
    def __init__(self, pos_x, pos_y, velocity=2, targeting_range=300, dash_multiplier=3):
        super().__init__("Angry Pig", pos_x, pos_y)
        self.dx = -velocity * WIDTH_COEF
        self.walk_velocity = velocity * WIDTH_COEF
        self.dash_multiplier = dash_multiplier
        self.running = False
        self.cooldown = False
        self.targeting_range = targeting_range * WIDTH_COEF

    def update(self, **kwargs):
        if not self.on_ground:
            self.fall()
            return False
        hero = kwargs['hero']
        if not self.alive:
            self.death()
        elif not self.is_active:
            pass
        elif self.cooldown:
            self.frequency = 4
            self.animation('Normal')
            if not self.cur_frame:
                self.cooldown = False
                self.frequency = 2

        elif not self.running:
            if self.direction == 'left':
                self.dx = -abs(self.dx)
            else:
                self.dx = abs(self.dx)
            self.animation('Walk')
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
            if (abs(self.rect.x - hero.rect.x) <= self.targeting_range and
                    abs(self.rect.y - hero.rect.y) <= self.rect.height):
                if (self.direction == 'left' and hero.rect.x < self.rect.x) or (
                        self.direction == 'right' and hero.rect.x > self.rect.x):
                    self.running = True
                    self.cur_frame = 0
                    sound_lib["pig_dash"].play()
        else:
            if self.direction == 'left':
                self.dx = -abs(self.walk_velocity * self.dash_multiplier)
            else:
                self.dx = abs(self.walk_velocity * self.dash_multiplier)
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
                    self.dx = self.walk_velocity
                    self.running = False
                    sound_lib["pig_dash_stop"].play()
                    self.cooldown = True
                    self.cur_frame = 0
                    break
            underground_rect = self.rect.move(-self.rect.width if self.dx < 0 else self.rect.width, 1)
            self.on_ground = False
            for block in nearest_blocks:
                if underground_rect.colliderect(block.rect):
                    self.on_ground = True
                    break
            if not self.on_ground:
                self.direction = 'left' if self.direction == 'right' else 'right'
                self.dx = self.walk_velocity
                self.cur_frame = 0
                self.running = False
                sound_lib["pig_dash_stop"].play()
                self.on_ground = True
                self.cooldown = True
