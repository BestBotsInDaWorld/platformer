from enemies.Enemy import *


class Skull(Enemy):
    def __init__(self, pos_x, pos_y, velocity=2, bullet_velocity=1, top_centre_y=-400, chaotic_dash_y=400,
                 dash_wall_x=300, berserk_speed_up=2, attacks_before_dash=2, bullet_acceleration=(0.25, 0.25),
                 max_bullet_dx=5, max_bullet_dy=5):
        super().__init__("Skull", pos_x, pos_y)
        self.dx = -velocity * WIDTH_COEF
        self.dy = -velocity * HEIGHT_COEF

        self.shieldless = False
        self.state = "Preparing"

        self.centre = (self.rect.x, self.rect.y)
        self.top_centre = (self.rect.x, self.rect.y + top_centre_y * HEIGHT_COEF)
        self.chaotic_dash_y = self.rect.y + chaotic_dash_y * HEIGHT_COEF
        self.left_dash, self.right_dash = ((self.rect.x - dash_wall_x * WIDTH_COEF, self.rect.y),
                                               (self.rect.x + dash_wall_x * WIDTH_COEF, self.rect.y))
        self.preparation_pos = (self.rect.x, self.rect.y)

        self.cur_attack_count = 0
        self.attacks_before_dash = attacks_before_dash
        self.berserk_speed_up = berserk_speed_up

        self.bullet_velocity = bullet_velocity
        self.bullet_acceleration = (bullet_acceleration[0] * WIDTH_COEF, bullet_acceleration[1] * HEIGHT_COEF)
        self.max_bullet_dx = max_bullet_dx * WIDTH_COEF
        self.max_bullet_dy = max_bullet_dy * HEIGHT_COEF

        self.attack_cooldowns = {
            "Rain_Attack": 3,
            "Bullet_Spam_Attack": 12,
            "Aim_Attack": 120,
            "Chaotic_Dash_Attack": 120,
            "Aimed_Dash": 120
        }
        self.cur_attack_cooldowns = {
            "Rain_Attack": 0,
            "Bullet_Spam_Attack": 0,
            "Aim_Attack": 0,
            "Chaotic_Dash_Attack": 0,
            "Aimed_Dash": 0
        }
        self.attack_attempts = {
            "Rain_Attack": 50,
            "Bullet_Spam_Attack": 50,
            "Aim_Attack": 3,
            "Chaotic_Dash_Attack": 6,
            "Aimed_Dash": 2,
        }
        self.cur_attack_attempts = {
            "Rain_Attack": 0,
            "Bullet_Spam_Attack": 0,
            "Aim_Attack": 0,
            "Chaotic_Dash_Attack": 0,
            "Aimed_Dash": 0,
        }


    def check_hit(self, hero):
        if self.alive:
            if not hero.invincible:
                if self.shieldless and hero.rect.top < self.rect.top:
                    self.hp -= 1
                    self.cur_frame = 0
                    self.damaged = True
                    self.shieldless = False
                    if not self.hp:
                        self.alive = False
                    sound_lib["enemy_hit"].play()
                    return "Enemy_Damaged"
                else:
                    return "Hero_Damaged"
            else:
                return False
        else:
            return False

    def update(self, **kwargs):
        hero, start = kwargs['hero'], kwargs['start']
        shift_x, shift_y = start.x, start.y

        if self.shieldless:
            pass
        elif self.state == "Preparing":
            self.attack_preparation(hero)
            self.rect.x, self.rect.y = shift_x + self.preparation_pos[0], shift_y + self.preparation_pos[1]
            print(self.rect.x, self.rect.y)
            ...
        elif self.state == "Rain_Attack":
            self.rain_attack(shift_x)
        else:
            self.bullet_spam_attack(hero)

    def attack_preparation(self, hero):
        if self.cur_attack_count == self.attacks_before_dash:
            self.cur_attack_count = 0
            self.state = "Aimed_Dash_Attack"
        else:
            self.state = choice(["Rain_Attack", "Bullet_Spam_Attack"])
            self.cur_attack_count += 1
        if self.state == "Rain_Attack" or self.state == "Bullet_Spam_Attack":
            self.preparation_pos = self.top_centre
        elif self.state == "Aim_Attack":
            self.preparation_pos = (self.rect.x, self.top_centre[1])
        elif self.state == "Chaotic_Dash_Attack":
            self.preparation_pos = (self.rect.x, self.chaotic_dash_y)
        elif self.state == "Aimed_Dash_Attack":
            if abs(hero.rect.x - self.left_dash[0]) > abs(hero.rect.x - self.right_dash[0]):
                self.preparation_pos = self.right_dash
            else:
                self.preparation_pos = self.left_dash
        print(self.state)

    def rain_attack(self, shift_x):
        if not self.cur_attack_cooldowns["Rain_Attack"]:
            SkullBullet(randint(shift_x + self.left_dash[0], shift_x + self.right_dash[0]),
                        self.rect.bottom, type="Red Particle", bullet_velocity=self.bullet_velocity,
                        shot_traectory=(0, 1), acceleration=(0, self.bullet_acceleration[1]), max_dx=self.max_bullet_dx,
                        max_dy=self.max_bullet_dy)
            self.cur_attack_attempts["Rain_Attack"] = ((self.cur_attack_attempts["Rain_Attack"] + 1) %
                                        self.attack_attempts["Rain_Attack"])
            if not self.cur_attack_attempts["Rain_Attack"]:
                self.state = "Preparing"
                return False
        self.cur_attack_cooldowns["Rain_Attack"] = ((self.cur_attack_cooldowns["Rain_Attack"] + 1) %
                                                    self.attack_cooldowns["Rain_Attack"])

    def bullet_spam_attack(self, hero):
        if not self.cur_attack_cooldowns["Bullet_Spam_Attack"]:
            dist_x_left = abs(self.rect.left - self.rect.width // 3 - hero.rect.left)
            dist_x_centre = abs(self.rect.left + self.rect.width // 2 - hero.rect.left)
            dist_x_right = abs(self.rect.right + self.rect.width // 10 - hero.rect.right)
            dist_y = abs(self.rect.top + self.rect.height // 2 - hero.rect.top)
            dist_y_centre = abs(self.rect.bottom - hero.rect.top)
            if self.rect.left - self.rect.width // 3 > hero.rect.left:
                x_direction_left = -1
            else:
                x_direction_left = 1
            if self.rect.left + self.rect.width // 2 > hero.rect.left + hero.rect.width // 2:
                x_direction_centre = -1
            else:
                x_direction_centre = 1
            if self.rect.right + self.rect.width // 10 > hero.rect.right:
                x_direction_right = -1
            else:
                x_direction_right = 1
            if self.rect.top + self.rect.height // 2 > hero.rect.top:
                y_direction = -1
            else:
                y_direction = 1
            if self.rect.bottom > hero.rect.top:
                y_direction_centre = -1
            else:
                y_direction_centre = 1

            if dist_x_left > dist_y:
                shot_traectory_left = (1 * x_direction_left, dist_y / dist_x_left * y_direction)
            else:
                shot_traectory_left = (dist_x_left / dist_y * x_direction_left, 1 * y_direction)
            if dist_x_centre > dist_y_centre:
                shot_traectory_centre = (1 * x_direction_centre, dist_y_centre / dist_x_centre * y_direction_centre)
            else:
                shot_traectory_centre = (dist_x_centre / dist_y_centre * x_direction_centre, 1 * y_direction_centre)
            if dist_x_right > dist_y:
                shot_traectory_right = (1 * x_direction_right, dist_y / dist_x_right * y_direction)
            else:
                shot_traectory_right = (dist_x_right / dist_y * x_direction_right, 1 * y_direction)
            SkullBullet(self.rect.left - self.rect.width // 3, self.rect.top + self.rect.height // 2,
                        type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                        shot_traectory=shot_traectory_left, acceleration=(0, 0),
                        max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)
            SkullBullet(self.rect.left + self.rect.width // 2.5, self.rect.bottom,
                        type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                        shot_traectory=shot_traectory_centre, acceleration=(0, 0),
                        max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)
            SkullBullet(self.rect.right + self.rect.width // 10, self.rect.top + self.rect.height // 2,
                        type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                        shot_traectory=shot_traectory_right, acceleration=(0, 0),
                        max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)
            self.cur_attack_attempts["Bullet_Spam_Attack"] = ((self.cur_attack_attempts["Bullet_Spam_Attack"] + 1) %
                                                              self.attack_attempts["Bullet_Spam_Attack"])
            if not self.cur_attack_attempts["Bullet_Spam_Attack"]:
                self.state = "Preparing"
                return False

        self.cur_attack_cooldowns["Bullet_Spam_Attack"] = ((self.cur_attack_cooldowns["Bullet_Spam_Attack"] + 1) %
                                                           self.attack_cooldowns["Bullet_Spam_Attack"])


class SkullBullet(Enemy):
    def __init__(self, pos_x, pos_y, type, bullet_velocity, shot_traectory, acceleration, max_dx, max_dy):
        super().__init__(type, pos_x, pos_y, precise_coords=True)
        self.shot_traectory = shot_traectory
        self.dx = self.shot_traectory[0] * bullet_velocity * WIDTH_COEF
        self.dy = self.shot_traectory[1] * bullet_velocity * HEIGHT_COEF
        self.acceleration = acceleration
        self.max_dx = max_dx
        self.max_dy = max_dy

    def update(self, **kwargs):
        self.animation('Moving')
        hero = kwargs["hero"]
        self.rect = self.rect.move(self.dx, self.dy)
        if abs(self.rect.x - hero.rect.x) > WIDTH * 2 or abs(self.rect.y - hero.rect.y) > HEIGHT * 2:
            self.kill()
        for block in nearest_blocks:
            if self.rect.colliderect(block.rect):
                self.kill()
        if self.dx < 0:
            self.dx = max(self.dx - self.acceleration[0], -self.max_dx)
        elif self.dx > 0:
            self.dx = min(self.dx + self.acceleration[0] * self.shot_traectory[0], self.max_dx)
        if self.dy < 0:
            self.dy = max(self.dy - self.acceleration[1], -self.max_dy)
        elif self.dy > 0:
            self.dy = min(self.dy + self.acceleration[1] * self.shot_traectory[1], self.max_dy)

    def check_destruction(self):
        self.kill()