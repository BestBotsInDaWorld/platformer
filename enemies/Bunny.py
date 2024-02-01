from enemies.Enemy import *


class Bunny(Enemy):
    def __init__(self, pos_x, pos_y, velocity=2, targeting_range=300, max_dy=5, jump_dy=7, target_jump=30):
        super().__init__("Bunny", pos_x, pos_y)
        self.dx = -velocity * WIDTH_COEF
        self.walk_velocity = velocity * WIDTH_COEF
        self.jump_dy = jump_dy * HEIGHT_COEF
        self.target_jump = target_jump * HEIGHT_COEF
        self.max_dy = max_dy * HEIGHT_COEF
        self.jumping = False
        self.targeting_range = targeting_range * WIDTH_COEF

    def update(self, **kwargs):
        hero = kwargs['hero']
        if not self.alive:
            self.death()
        elif not self.on_ground:
            self.fall()
        elif not self.is_active:
            pass
        elif not self.jumping:
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
            if (abs(self.rect.x - hero.rect.x) <= self.targeting_range and
                    self.target_jump <= self.rect.y - hero.rect.y <= HEIGHT):
                if (self.direction == 'left' and hero.rect.x < self.rect.x) or (
                        self.direction == 'right' and hero.rect.x > self.rect.x):
                    self.jumping = True
                    sound_lib["bunny_jump"].play()
                    self.dy = -self.jump_dy
                    self.cur_frame = 0
        else:
            if self.direction == 'left':
                self.dx = -abs(self.dx)
            else:
                self.dx = abs(self.dx)
            if self.dy > 0:
                self.animation('Jump')
            else:
                self.animation('Fall')
            self.rect = self.rect.move(self.dx, 0)
            for block in nearest_blocks:
                if self.rect.colliderect(block.rect):
                    if self.rect.right > block.rect.right:
                        self.direction = 'right'
                        self.rect.x = block.rect.right
                    else:
                        self.direction = 'left'
                        self.rect.x = block.rect.left - self.rect.width
                break
            self.rect = self.rect.move(0, self.dy)
            if self.check_self_hit(hero):
                return False
            self.dy = min(self.dy + GRAVITY, self.max_dy)
            for block in nearest_blocks:
                if self.rect.colliderect(block.rect):
                    if self.rect.top < block.rect.top:
                        self.rect.y = block.rect.top - self.rect.height
                        self.jumping = False
                        self.cur_frame = 0
                        self.dy = 0
                    else:
                        self.rect.y = block.rect.bottom
                    break
