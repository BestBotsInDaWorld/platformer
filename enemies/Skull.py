from enemies.Enemy import *


class Skull(Enemy):
    def __init__(self, pos_x, pos_y, velocity=4, bullet_velocity=1, top_centre_y=-400, recovery_cooldown=240,
                 dash_wall_x=200, berserk_speed_up=2, attacks_before_dash=2, aim_acceleration=0.25,
                 bullet_acceleration=(0.25, 0.25), max_bullet_dx=5, max_bullet_dy=5, dash_time=60, preparation_wait=120,
                 aim_particles_spawn_rate=24, dash_particles_spawn_rate=36, wall_knockback=(3, -3)):
        super().__init__("Skull", pos_x, pos_y)
        self.initial_dx = velocity * WIDTH_COEF
        self.initial_dy = velocity * HEIGHT_COEF
        self.dx = self.initial_dx * WIDTH_COEF
        self.dy = self.initial_dy * HEIGHT_COEF
        self.aim_acceleration = aim_acceleration * HEIGHT_COEF

        self.in_focus = False

        self.hp = 3
        self.in_knockback = False
        self.shieldless = False
        self.state = "Preparing"
        self.cur_preparation_wait = 0
        self.preparation_wait = preparation_wait
        self.hit_state = "Shield Off"

        self.centre = (self.rect.x, self.rect.y)
        self.top_centre = (self.rect.x, self.rect.y + top_centre_y * HEIGHT_COEF)
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

        self.aim_particles_spawn_rate = aim_particles_spawn_rate
        self.cur_acting_frame = 0

        self.dash_particles_spawn_rate = dash_particles_spawn_rate

        self.dash_traectory = (1, 1)
        self.dash_time = dash_time
        self.cur_dash_time = 0

        self.wall_knockback = wall_knockback

        self.cur_recovery_cooldown = 0
        self.recovery_cooldown = recovery_cooldown

        self.first_attack = False

        self.attack_cooldowns = {
            "Rain_Attack": 12,
            "Bullet_Spam_Attack": 30,
            "Aim_Attack": 30,
            "Aimed_Dash_Attack": 30,
            "Chaotic_Dash_Attack": 120,
            "Death": 120
        }
        self.cur_attack_cooldowns = {
            "Rain_Attack": 0,
            "Bullet_Spam_Attack": 0,
            "Aim_Attack": 1,
            "Aimed_Dash_Attack": 1,
            "Chaotic_Dash_Attack": 0,
            "Death": 0
        }
        self.attack_attempts = {
            "Rain_Attack": 50,
            "Bullet_Spam_Attack": 15,
            "Aim_Attack": 3,
            "Aimed_Dash_Attack": 4,
            "Chaotic_Dash_Attack": 2,
        }
        self.cur_attack_attempts = {
            "Rain_Attack": 0,
            "Bullet_Spam_Attack": 0,
            "Aim_Attack": 0,
            "Aimed_Dash_Attack": 0,
            "Chaotic_Dash_Attack": 0,
        }

    def check_hit(self, hero, direction="vertical"):
        if self.alive:
            if not hero.invincible:
                if direction == "vertical":
                    if self.shieldless and self.hit_state == "Recovery" and hero.rect.top < self.rect.top:
                        self.hp -= 1
                        self.berserk_upgrades()
                        self.cur_frame = 0
                        self.hit_state = "Shield On"
                        self.cur_recovery_cooldown = 0
                        if not self.hp:
                            self.alive = False
                            self.image = self.frames_forward["Recovery"][0]
                        sound_lib["enemy_hit"].play()
                        return "Enemy_Damaged"
                    elif self.shieldless:
                        return False
                    else:
                        return "Hero_Damaged"
                elif self.direction == "horizontal":
                    if self.shieldless:
                        return False
                    else:
                        return "Hero_Damaged"
            else:
                return False
        else:
            return False

    def death(self, shift_x=0, shift_y=0):
        if self.attack_cooldowns["Death"] >= 4:
            if not self.cur_attack_cooldowns["Death"]:
                self.rect.x = randint(self.left_dash[0], self.right_dash[0]) + shift_x
                self.rect.y = self.top_centre[1] + shift_y
                self.spawn_bullet_cluster()
                sound_lib["skull_exploding"].play()
                self.cur_attack_cooldowns["Death"] = 1
                self.attack_cooldowns["Death"] //= 1.1
                if self.attack_cooldowns["Death"] < 4:
                    self.cur_attack_cooldowns["Death"] = 30
                    return
            self.cur_attack_cooldowns["Death"] = ((self.cur_attack_cooldowns["Death"] + 1) %
                                                  self.attack_cooldowns["Death"])
        else:
            if not self.cur_attack_cooldowns["Death"]:
                for x_pos in [self.left_dash[0], (self.left_dash[0] + self.top_centre[0]) // 2, self.top_centre[0],
                              (self.top_centre[0] + self.right_dash[0]) // 2, self.right_dash[0]]:
                    self.rect.x = x_pos + shift_x
                    self.spawn_bullet_cluster()
                sound_lib["skull_death"].play()
                self.kill()
            self.cur_attack_cooldowns["Death"] -= 1

    def update(self, **kwargs):
        hero, start = kwargs['hero'], kwargs['start']
        shift_x, shift_y = start.x, start.y
        if not self.in_focus:
            if abs(self.rect.x - hero.rect.x) < WIDTH // 10 and self.rect.y < hero.rect.y:
                self.in_focus = True
        elif not self.alive:
            self.death(shift_x, shift_y)
            return
        elif self.shieldless:
            self.recovery()
            return
        elif self.state == "Preparing":
            self.attack_preparation(hero, shift_x, shift_y)
            self.rect.x, self.rect.y = shift_x + self.preparation_pos[0], shift_y + self.preparation_pos[1]
        elif self.cur_preparation_wait:
            self.cur_preparation_wait += 1
            if self.cur_preparation_wait == self.preparation_wait:
                self.cur_preparation_wait = 0
        elif self.state == "Rain_Attack":
            self.rain_attack(shift_x)
        elif self.state == "Bullet_Spam_Attack":
            self.bullet_spam_attack(hero)
        elif self.state == "Aim_Attack":
            self.aim_attack(hero, shift_y)
        elif self.state == "Aimed_Dash_Attack":
            self.aimed_dash_attack(hero)
        elif self.state == "Chaotic_Dash_Attack":
            self.chaotic_dash_attack()
        self.animation('Normal')

    def recovery(self):
        self.frequency = 4
        self.rect = self.rect.move(self.dx, self.dy)
        for block in nearest_blocks:
            if self.rect.colliderect(block.rect):
                self.dx = 0
                self.dy = 0
                self.in_knockback = False
        if self.in_knockback:
            self.dy += GRAVITY
        if self.hit_state == "Shield Off":
            self.animation('Shield Off')
            if not self.cur_frame:
                self.hit_state = "Recovery"
        elif self.hit_state == "Recovery":
            self.animation('Recovery')
            self.cur_recovery_cooldown += 1
            if self.cur_recovery_cooldown == self.recovery_cooldown:
                self.hit_state = "Shield On"
                self.cur_frame = 0
                self.cur_recovery_cooldown = 0
        else:
            self.animation('Shield On')
            if not self.cur_frame:
                self.hit_state = "Shield Off"
                self.shieldless = False
                self.cur_frame = 0

    def berserk_upgrades(self):
        for key in self.attack_cooldowns.keys():
            if key != "Aim_Attack" and key != "Death":
                self.attack_cooldowns[key] //= self.berserk_speed_up
        for key in self.attack_attempts.keys():
            if key != "Death" and key != "Aimed_Dash_Attack" and key != "Aim_Attack":
                self.attack_attempts[key] *= self.berserk_speed_up
        if self.hp == 2:
            self.aim_particles_spawn_rate //= self.berserk_speed_up
            self.attack_attempts["Aimed_Dash_Attack"] *= self.berserk_speed_up
            self.attack_attempts["Aim_Attack"] *= self.berserk_speed_up
        if self.hp == 1:
            self.attack_cooldowns["Aim_Attack"] //= self.berserk_speed_up
            self.dash_particles_spawn_rate //= self.berserk_speed_up
            self.preparation_wait //= self.berserk_speed_up
        self.attacks_before_dash *= self.berserk_speed_up

    def attack_preparation(self, hero, shift_x, shift_y):
        self.dx = self.initial_dx
        self.dy = self.initial_dx
        if self.cur_attack_count == self.attacks_before_dash:
            self.cur_attack_count = 0
            self.state = "Chaotic_Dash_Attack"
        else:
            if not self.first_attack:
                self.state = "Rain_Attack"
                self.first_attack = True
            else:
                self.state = choice(["Rain_Attack", "Bullet_Spam_Attack", "Aim_Attack", "Aimed_Dash_Attack"])
            self.cur_attack_count += 1
        if self.state == "Rain_Attack" or self.state == "Bullet_Spam_Attack":
            self.preparation_pos = self.top_centre
        elif self.state == "Aim_Attack":
            self.preparation_pos = self.top_centre
        elif self.state == "Aimed_Dash_Attack":
            self.preparation_pos = (self.rect.x - shift_x, self.rect.y - shift_y)
        elif self.state == "Chaotic_Dash_Attack":
            if abs(hero.rect.x - self.left_dash[0]) > abs(hero.rect.x - self.right_dash[0]):
                self.preparation_pos = self.left_dash
                self.direction = "right"
                self.dx = abs(self.initial_dx)
            else:
                self.preparation_pos = self.right_dash
                self.direction = "left"
                self.dx = -abs(self.initial_dx)
        self.cur_preparation_wait = 1
        sound_lib[self.state].play()

    def rain_attack(self, shift_x):
        if not self.cur_attack_cooldowns["Rain_Attack"]:
            SkullBullet(
                randint(shift_x + self.left_dash[0] - self.rect.width, shift_x + self.right_dash[0] + self.rect.width),
                self.rect.bottom, type="Red Particle", bullet_velocity=self.bullet_velocity,
                shot_traectory=(0, 1), acceleration=(0, self.bullet_acceleration[1]), max_dx=self.max_bullet_dx,
                max_dy=self.max_bullet_dy)
            self.cur_attack_attempts["Rain_Attack"] = ((self.cur_attack_attempts["Rain_Attack"] + 1) %
                                                       self.attack_attempts["Rain_Attack"])
            if self.hp == 3 or (self.hp == 2 and self.cur_attack_attempts["Rain_Attack"] % 2 == 0) or (
                    self.hp == 1 and self.cur_attack_attempts["Rain_Attack"] % 4 == 0):
                sound_lib["Rain_Attack_Attempt"].play()
            if not self.cur_attack_attempts["Rain_Attack"]:
                self.state = "Preparing"
                return False
        self.cur_attack_cooldowns["Rain_Attack"] = ((self.cur_attack_cooldowns["Rain_Attack"] + 1) %
                                                    self.attack_cooldowns["Rain_Attack"])

    def bullet_spam_attack(self, hero):
        if not self.cur_attack_cooldowns["Bullet_Spam_Attack"]:
            hero_mid = hero.rect.left + hero.rect.width // 2
            dist_x_left = abs(self.rect.left - self.rect.width // 3 - hero_mid)
            dist_x_centre = abs(self.rect.left + self.rect.width // 2 - hero_mid)
            dist_x_right = abs(self.rect.right + self.rect.width // 10 - hero_mid)
            dist_y = abs(self.rect.bottom + self.rect.height // 2 - hero.rect.bottom)
            dist_y_centre = abs(self.rect.bottom - hero.rect.top)
            if self.rect.left - self.rect.width // 3 > hero_mid:
                x_direction_left = -1
            else:
                x_direction_left = 1
            if self.rect.left + self.rect.width // 2 > hero_mid:
                x_direction_centre = -1
            else:
                x_direction_centre = 1
            if self.rect.right + self.rect.width // 10 > hero_mid:
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
                        max_dx=self.max_bullet_dx * 6, max_dy=self.max_bullet_dy * 6)
            SkullBullet(self.rect.left + self.rect.width // 2.5, self.rect.bottom,
                        type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                        shot_traectory=shot_traectory_centre, acceleration=(0, 0),
                        max_dx=self.max_bullet_dx * 6, max_dy=self.max_bullet_dy * 6)
            SkullBullet(self.rect.right + self.rect.width // 10, self.rect.top + self.rect.height // 2,
                        type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                        shot_traectory=shot_traectory_right, acceleration=(0, 0),
                        max_dx=self.max_bullet_dx * 6, max_dy=self.max_bullet_dy * 6)
            self.cur_attack_attempts["Bullet_Spam_Attack"] = ((self.cur_attack_attempts["Bullet_Spam_Attack"] + 1) %
                                                              self.attack_attempts["Bullet_Spam_Attack"])
            sound_lib["Bullet_Spam_Attack_Attempt"].play()
            if not self.cur_attack_attempts["Bullet_Spam_Attack"]:
                self.state = "Preparing"
                self.cur_frame = 0
                return False

        self.cur_attack_cooldowns["Bullet_Spam_Attack"] = ((self.cur_attack_cooldowns["Bullet_Spam_Attack"] + 1) %
                                                           self.attack_cooldowns["Bullet_Spam_Attack"])

    def aim_attack(self, hero, shift_y):
        if not self.cur_attack_cooldowns["Aim_Attack"]:
            self.rect = self.rect.move(0, self.dy)
            self.dy += self.aim_acceleration
            self.cur_acting_frame += 1
            for block in nearest_blocks:
                if self.rect.colliderect(block.rect):
                    self.cur_acting_frame = 0
                    self.rect.bottom = block.rect.top
                    self.dy = self.initial_dy
                    self.cur_attack_cooldowns["Aim_Attack"] = 1
                    self.cur_attack_attempts["Aim_Attack"] = (
                            (self.cur_attack_attempts["Aim_Attack"] + 1) %
                            self.attack_attempts["Aim_Attack"])
                    self.spawn_opposite_bullets()
                    sound_lib["Aim_Attack_Attempt"].play()
                    if not self.cur_attack_attempts["Aim_Attack"]:
                        self.state = "Preparing"
                        self.cur_frame = 0
                    break
            if self.cur_acting_frame:
                if ((self.cur_attack_attempts["Aim_Attack"] % 2 == 0 and
                     not self.cur_acting_frame % self.aim_particles_spawn_rate) or
                        (self.cur_attack_attempts["Aim_Attack"] % 2 and
                         self.cur_acting_frame % self.aim_particles_spawn_rate == self.aim_particles_spawn_rate // 3)):
                    self.spawn_opposite_bullets()

        else:
            self.rect.y = self.top_centre[1] + shift_y
            self.rect.x = hero.rect.x
            self.cur_attack_cooldowns["Aim_Attack"] = ((self.cur_attack_cooldowns["Aim_Attack"] + 1) %
                                                       self.attack_cooldowns["Aim_Attack"])

    def spawn_opposite_bullets(self):
        SkullBullet(self.rect.left - self.rect.width // 3, self.rect.top + self.rect.height // 3 * 2,
                    type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                    shot_traectory=(-1, 0), acceleration=(0.25, 0),
                    max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)
        SkullBullet(self.rect.right + self.rect.width // 10, self.rect.top + self.rect.height // 3 * 2,
                    type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                    shot_traectory=(1, 0), acceleration=(0.25, 0),
                    max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)

    def aimed_dash_attack(self, hero):
        if not self.cur_attack_cooldowns["Aimed_Dash_Attack"]:
            self.rect = self.rect.move(self.dash_traectory[0] * self.dx, self.dash_traectory[1] * self.dy)
            self.cur_dash_time = (self.cur_dash_time + 1) % self.dash_time
            if not self.cur_dash_time:
                self.cur_attack_attempts["Aimed_Dash_Attack"] = (
                        (self.cur_attack_attempts["Aimed_Dash_Attack"] + 1) %
                        self.attack_attempts["Aimed_Dash_Attack"])
                sound_lib["Aimed_Dash_Attack_Stop"].play()
                self.cur_attack_cooldowns["Aimed_Dash_Attack"] = 1
                self.spawn_bullet_cluster()
                if not self.cur_attack_attempts["Aimed_Dash_Attack"]:
                    self.state = "Preparing"
                    self.cur_frame = 0
                    return False
        else:
            if self.cur_attack_cooldowns["Aimed_Dash_Attack"] == self.attack_cooldowns["Aimed_Dash_Attack"] - 1:
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
                sound_lib["Aimed_Dash_Attack_Dashing"].play()
            self.cur_attack_cooldowns["Aimed_Dash_Attack"] = ((self.cur_attack_cooldowns["Aimed_Dash_Attack"] + 1) %
                                                              self.attack_cooldowns["Aimed_Dash_Attack"])

    def spawn_bullet_cluster(self):
        SkullBullet(self.rect.left - self.rect.width // 3, self.rect.top + self.rect.height // 3,
                    type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                    shot_traectory=(-1, 0), acceleration=(0.25, 0),
                    max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)
        SkullBullet(self.rect.right + self.rect.width // 10, self.rect.top + self.rect.height // 3,
                    type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                    shot_traectory=(1, 0), acceleration=(0.25, 0),
                    max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)
        SkullBullet(self.rect.left - self.rect.width // 3, self.rect.top - self.rect.height // 3,
                    type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                    shot_traectory=(-1, -1), acceleration=(0, 0),
                    max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)
        SkullBullet(self.rect.right + self.rect.width // 10, self.rect.top - self.rect.height // 3,
                    type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                    shot_traectory=(1, -1), acceleration=(0, 0),
                    max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)
        SkullBullet(self.rect.left - self.rect.width // 3, self.rect.bottom,
                    type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                    shot_traectory=(-1, 1), acceleration=(0, 0),
                    max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)
        SkullBullet(self.rect.right + self.rect.width // 10, self.rect.bottom,
                    type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                    shot_traectory=(1, 1), acceleration=(0, 0),
                    max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)
        SkullBullet(self.rect.left + self.rect.width // 2.5, self.rect.bottom,
                    type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                    shot_traectory=(0, 1), acceleration=(0, 0),
                    max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)
        SkullBullet(self.rect.left + self.rect.width // 2.5, self.rect.top - self.rect.height // 3,
                    type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                    shot_traectory=(0, -1), acceleration=(0, 0),
                    max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)

    def chaotic_dash_attack(self):
        if not self.cur_attack_cooldowns["Chaotic_Dash_Attack"]:
            self.rect = self.rect.move(self.dx, 0)
            self.cur_acting_frame += 1
            for block in nearest_blocks:
                if self.rect.colliderect(block.rect):
                    if self.dx < 0:
                        self.rect.x = block.rect.right
                    else:
                        self.rect.x = block.rect.left - self.rect.width
                    self.cur_attack_attempts["Chaotic_Dash_Attack"] = (
                            (self.cur_attack_attempts["Chaotic_Dash_Attack"] + 1) %
                            self.attack_attempts["Chaotic_Dash_Attack"])
                    sound_lib["Chaotic_Dash_Attack_Attempt"].play()
                    if not self.cur_attack_attempts["Chaotic_Dash_Attack"]:
                        self.cur_acting_frame = 0
                        self.state = "Preparing"
                        self.cur_frame = 0
                        self.shieldless = True
                        self.in_knockback = True
                        self.dx, self.dy = self.wall_knockback
                        self.dx = -self.dx if self.direction == "right" else self.dx
                        break
                    self.dx *= -1
                    self.direction = "right" if self.dx > 0 else "left"
            if ((self.cur_attack_attempts["Chaotic_Dash_Attack"] % 2 == 0 and
                 not self.cur_acting_frame % self.dash_particles_spawn_rate) or
                    (self.cur_attack_attempts["Chaotic_Dash_Attack"] % 2 and
                     self.cur_acting_frame % self.dash_particles_spawn_rate == self.dash_particles_spawn_rate // 2)):
                self.spawn_bullet_column((self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2), 3)
                sound_lib["Bullet_Spam_Attack_Attempt"].play()

        else:
            self.cur_attack_cooldowns["Chaotic_Dash_Attack"] = ((self.cur_attack_cooldowns["Chaotic_Dash_Attack"] + 1) %
                                                                self.attack_cooldowns["Chaotic_Dash_Attack"])

    def spawn_bullet_column(self, centre, amount):
        for i in range(amount):
            SkullBullet(centre[0], centre[1] + self.rect.height // 3 * i,
                        type="Red Particle", bullet_velocity=self.bullet_velocity * 6,
                        shot_traectory=(0, -1), acceleration=(0, 0.25),
                        max_dx=self.max_bullet_dx, max_dy=self.max_bullet_dy)


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
