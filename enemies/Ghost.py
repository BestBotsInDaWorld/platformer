from enemies.Enemy import *


class Ghost(Enemy):
    def __init__(self, pos_x, pos_y, velocity=2, targeting_range_x=100, targeting_range_y=100, frames_dashing=60):
        super().__init__("Ghost", pos_x, pos_y)
        self.velocity = velocity * WIDTH_COEF
        self.cur_dash_time = 0
        self.frames_dashing = frames_dashing
        self.state = "Not Triggered"
        self.targeting_range_x = targeting_range_x * WIDTH_COEF
        self.targeting_range_y = targeting_range_y * HEIGHT_COEF
        self.dash_traectory = (1, 1)

    def update(self, **kwargs):
        hero = kwargs['hero']
        if not self.alive:
            self.death()
        elif not self.is_active:
            pass
        elif self.state == "Not Triggered":
            self.animation("Ghost Particles")
            if abs(self.rect.x - hero.rect.x) <= self.targeting_range_x and abs(
                    self.rect.x - hero.rect.x) <= self.targeting_range_y:
                self.state = "Appearing"
                sound_lib["ghost_appear"].play()
                self.direction = 'left' if self.rect.x > hero.rect.x else 'right'
                self.cur_frame = 0
        elif self.state == "Appearing":
            self.frequency = 10
            self.animation('Appear')
            if not self.cur_frame:
                self.hp = 1
                self.frequency = 2
                self.state = "Triggered"
        elif self.state == "Triggered":
            if not (abs(self.rect.x - hero.rect.x) <= self.targeting_range_x and abs(
                    self.rect.x - hero.rect.x) <= self.targeting_range_y):
                self.state = "Not Triggered"
                return False
            dist_x = abs(self.rect.x - hero.rect.x)
            dist_y = abs(self.rect.y - hero.rect.y)
            if self.rect.left > hero.rect.left:
                x_direction = -1
                self.direction = 'left'
            else:
                x_direction = 1
                self.direction = 'right'
            if self.rect.top > hero.rect.top:
                y_direction = -1
            else:
                y_direction = 1
            if dist_x > dist_y:
                self.dash_traectory = (1 * x_direction, dist_y / dist_x * y_direction)
            else:
                self.dash_traectory = (dist_x / dist_y * x_direction, 1 * y_direction)
            self.state = "Dashing"
            self.animation('Normal')
        else:
            self.rect = self.rect.move(self.dash_traectory[0] * self.velocity, self.dash_traectory[1] * self.velocity)
            if self.check_self_hit(hero):
                return False
            self.cur_dash_time += 1
            self.animation('Normal')
            if self.cur_dash_time == self.frames_dashing:
                self.cur_dash_time = 0
                self.state = "Triggered"

    def death(self):
        self.frequency = 10
        self.animation('Disappear')
        if not self.cur_frame:
            self.alive = True
            self.state = "Not Triggered"
            self.hp = 1
            self.frequency = 2
