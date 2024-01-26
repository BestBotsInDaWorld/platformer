from enemies.Enemy import *


class AngryPig(Enemy):
    def __init__(self, pos_x, pos_y, velocity=2, targeting_range=300, dash_multiplier=3):
        super().__init__("Angry Pig", pos_x, pos_y)
        self.dx = -velocity
        self.walk_velocity = velocity
        self.dash_multiplier = dash_multiplier
        self.running = False
        self.cooldown = False
        self.targeting_range = targeting_range

    def update(self, **kwargs):
        if not self.on_ground:
            self.fall()
            return False
        hero = kwargs['hero']
        if not self.alive:
            self.death()
        elif self.cooldown:
            self.animation('Idle')
            if not self.cur_frame:
                self.cooldown = False

        elif not self.running:
            if self.direction == 'left':
                self.dx = -abs(self.dx)
            else:
                self.dx = abs(self.dx)
            self.animation('Walk')
            self.rect = self.rect.move(self.dx, 0)
            for block in block_group:
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
            for block in block_group:
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
        else:
            if self.direction == 'left':
                self.dx = -abs(self.walk_velocity * self.dash_multiplier)
            else:
                self.dx = abs(self.walk_velocity * self.dash_multiplier)
            self.animation('Run')
            self.rect = self.rect.move(self.dx, 0)
            for block in block_group:
                if self.rect.colliderect(block.rect):
                    if self.rect.right > block.rect.right:
                        self.direction = 'right'
                        self.rect.x = block.rect.right
                    else:
                        self.direction = 'left'
                        self.rect.x = block.rect.left - self.rect.width
                    self.dx = self.walk_velocity
                    self.running = False
                    break
            underground_rect = self.rect.move(-self.rect.width if self.dx < 0 else self.rect.width, 1)
            self.on_ground = False
            for block in block_group:
                if underground_rect.colliderect(block.rect):
                    self.on_ground = True
                    break
            if not self.on_ground:
                self.direction = 'left' if self.direction == 'right' else 'right'
                self.dx = self.walk_velocity
                self.cur_frame = 0
                self.running = False
                self.on_ground = True
