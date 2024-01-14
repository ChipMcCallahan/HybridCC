from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Id


class ToggleWall(Elem):
    def __init__(self):
        super().__init__(Id.TOGGLE_WALL)
