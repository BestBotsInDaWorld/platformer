from traps.Trap import *


class JumpRefresher(Trap):
    def __init__(self, pos_x, pos_y, refresh_time=300):
        super().__init__("Jump Refresher", pos_x, pos_y)
        self.image = self.frames['On'][0]
        self.hit_type = "Special"
        self.refresh_time = refresh_time
        self.cur_refresh = 0
        self.frequency = 3

    def update(self, **kwargs):
        if not self.cur_refresh:
            self.animation("On")
        else:
            self.animation("Hit")
            self.cur_refresh += 1
            if self.cur_refresh == self.refresh_time:
                self.cur_refresh = 0
                self.hit_type = "Special"

    def special_behaviour(self, object):
        if hasattr(object, 'jump_number'):
            object.jump_number = min(object.jump_number, 1)
            self.cur_frame = 0
            self.cur_refresh = 1
            self.hit_type = "Inactive"
            sound_lib["jump_refresh"].play()