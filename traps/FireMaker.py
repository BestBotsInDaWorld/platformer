from traps.Trap import *


class FireMaker(Trap):
    def __init__(self, pos_x, pos_y, before_start=0,
                 shot_delay=60, warning_time=32, damaging_time=60):
        super().__init__("Fire Maker", pos_x, pos_y)
        self.hit_type = False
        self.before_start = before_start
        self.shot_delay = shot_delay
        self.warning_time = warning_time
        self.damaging_time = damaging_time
        self.half_cycle = self.shot_delay + self.warning_time + self.warning_time

    def update(self, **kwargs):
        hero = kwargs['hero']
        if not self.before_start:
            if self.shot_delay + self.warning_time <= self.cur_frame < self.half_cycle + self.damaging_time:
                if self.shot_delay + self.warning_time == self.cur_frame:
                    if abs(self.rect.x - hero.rect.x) <= WIDTH and abs(self.rect.y - hero.rect.y) <= HEIGHT:
                        sound_lib["fire_on"].play()
                    Fire(self.rect.x, self.rect.y - self.rect.height, self.damaging_time)
                self.animation('Damaging')
            elif self.shot_delay <= self.cur_frame < self.half_cycle + self.damaging_time + self.warning_time:
                self.animation('Warning')
            else:
                self.animation('Delay')
            self.cur_frame = (self.cur_frame + 1) % (self.half_cycle * 2)
        self.before_start = max(self.before_start - 1, 0)

    def animation(self, state):
        if state == 'Damaging':
            if self.cur_frame < self.half_cycle:
                current = self.cur_frame - self.shot_delay - self.warning_time
            else:
                current = self.damaging_time - (self.cur_frame - self.half_cycle) - 1
            self.image = self.frames['On'][current // (self.damaging_time // 3)]
        elif state == 'Warning':
            if self.cur_frame < self.half_cycle:
                current = self.cur_frame - self.shot_delay
            else:
                current = self.warning_time - (self.cur_frame - self.half_cycle - self.damaging_time) - 1
            self.image = self.frames['Hit'][current // (self.warning_time // 4)]
        else:
            self.image = self.frames['Idle'][0]

    def fix_standing(self, object):
        if object.rect.colliderect(self.rect.move(0, -1)):
            return True


class Fire(Trap):
    def __init__(self, pos_x, pos_y, damaging_time=60):
        super().__init__("Fire", pos_x, pos_y, precise_coords=True)
        self.damaging_time = damaging_time * 2
        self.hit_type = 'Through_Hit'

    def update(self, **kwargs):
        if self.cur_frame == self.damaging_time:
            hero = kwargs['hero']
            if abs(self.rect.x - hero.rect.x) <= WIDTH and abs(self.rect.y - hero.rect.y) <= HEIGHT:
                sound_lib["fire_off"].play()
            self.kill()
        if self.cur_frame < self.damaging_time // 2:
            self.image = self.frames['On'][self.cur_frame // (self.damaging_time // 3)]
        else:
            self.image = self.frames['On'][(self.damaging_time - (self.cur_frame - self.damaging_time // 2) - 1)
                                           // (self.damaging_time // 3)]
        self.cur_frame += 1
