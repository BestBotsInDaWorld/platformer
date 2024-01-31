from special.Special import *


class Start(Special):
    def __init__(self, pos_x, pos_y):
        super().__init__("Start", pos_x, pos_y)
        self.activated = False

    def update(self, **kwargs):
        if not self.activated:
            sound_lib[f"start{randint(1, 5)}"].play()
            self.activated = True
        self.animation("Moving")
