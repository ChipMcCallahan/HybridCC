from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.shared import Id


class Monster(Mob):
    def __init__(self):
        super().__init__(Id.MONSTER)