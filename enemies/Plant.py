from enemies.Enemy import *


class Plant(Enemy):
    def __init__(self, pos_x, pos_y, bullet_velocity=5, shot_delay=60,
                 min_shot_range_x=50, max_shot_range_x=500,
                 max_shot_range_y=300):
        super().__init__("Plant", pos_x, pos_y)
        self.bullet_velocity = bullet_velocity
        self.shot_delay = shot_delay
        self.cur_shot_delay = 0
        self.min_shot_range_x = min_shot_range_x * WIDTH_COEF
        self.max_shot_range_x = max_shot_range_x * WIDTH_COEF
        self.max_shot_range_y = max_shot_range_y * HEIGHT_COEF
        self.attacking = False
        self.shot_traectory = (0, 0)
        self.frequency = 3

    def update(self, **kwargs):
        if not self.on_ground:
            self.fall()
            return False
        if not self.alive:
            self.death()
        elif not self.is_active:
            pass
        elif self.attacking:
            self.animation('Attack')
            if self.cur_frame == 4 * self.frequency:
                if self.direction == 'left':
                    PlantBullet(self.rect.left + self.rect.width // 4, self.rect.y + self.rect.height // 3,
                                self.bullet_velocity, self.shot_traectory)
                else:
                    PlantBullet(self.rect.right - self.rect.width // 4, self.rect.y + self.rect.height // 3,
                                self.bullet_velocity, self.shot_traectory)
                sound_lib["plant_shot"].play()
            elif not self.cur_frame:
                self.attacking = False
                self.cur_frame = 0
        else:
            hero = kwargs['hero']
            if hero.rect.left < self.rect.left:
                self.direction = 'left'
            elif hero.rect.right > self.rect.right:
                self.direction = 'right'
            self.try_shooting(hero)
            self.animation('Normal')

    def try_shooting(self, hero):
        if not self.cur_shot_delay:
            dist_x = abs(self.rect.x - hero.rect.x)
            dist_y = abs(self.rect.y - hero.rect.y)
            if self.min_shot_range_x <= dist_x <= self.max_shot_range_x and dist_y <=  self.max_shot_range_y:
                self.attacking = True
                self.cur_frame = 0
                if self.rect.left > hero.rect.left:
                    x_direction = -1
                else:
                    x_direction = 1
                if self.rect.top > hero.rect.top:
                    y_direction = -1
                else:
                    y_direction = 1

                if dist_x > dist_y:
                    self.shot_traectory = (1 * x_direction, dist_y / dist_x * y_direction)
                else:
                    self.shot_traectory = (dist_x / dist_y * x_direction, 1 * y_direction)
            self.cur_shot_delay = 1

        else:
            self.cur_shot_delay = (self.cur_shot_delay + 1) % self.shot_delay


class PlantBullet(Enemy):
    def __init__(self, pos_x, pos_y, bullet_velocity, shot_traectory):
        super().__init__("Plant Bullet", pos_x, pos_y, precise_coords=True)
        self.bullet_velocity = bullet_velocity
        self.shot_traectory = (shot_traectory[0] * WIDTH_COEF, shot_traectory[1] * HEIGHT_COEF)

    def update(self, **kwargs):
        self.animation('Moving')
        hero, blocks = kwargs["hero"], kwargs["blocks"]
        self.rect = self.rect.move(self.shot_traectory[0] * self.bullet_velocity,
                                   self.shot_traectory[1] * self.bullet_velocity)
        if self.check_self_hit(hero):
            self.kill()
        if abs(self.rect.x - hero.rect.x) > WIDTH * 2 or abs(self.rect.y - hero.rect.y) > HEIGHT * 2:
            self.kill()
        for block in nearest_blocks:
            if self.rect.colliderect(block.rect):
                self.kill()

    def check_destruction(self):
        self.kill()