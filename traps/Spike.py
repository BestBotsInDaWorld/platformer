from traps.Trap import *


class Spike(Trap):
    def __init__(self, pos_x, pos_y):
        super().__init__("Spike", pos_x, pos_y)
        self.hit_type = 'Through_Hit'