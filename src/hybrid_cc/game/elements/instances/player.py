from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.shared import Id


class Player(Mob):
    def __init__(self):
        super().__init__(Id.PLAYER)
