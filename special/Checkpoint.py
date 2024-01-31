from special.Special import *


class Checkpoint(Special):
    def __init__(self, pos_x, pos_y, number=1):
        super().__init__("Checkpoint", pos_x, pos_y)
        self.activated = False
        self.number = number
        self.triggered = False

    def update(self, **kwargs):
        hero = kwargs["hero"]
        if not self.activated and self.rect.colliderect(hero.rect):
            hero.cur_checkpoint = self.number
            self.activated = True
        elif self.activated and not self.triggered:
            self.animation("Hit")
            if not self.cur_frame:
                self.triggered = True
        else:
            self.animation("Moving")
