from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.shared import Id


class Tank(Mob):
    def __init__(self):
        super().__init__(Id.TANK)