from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Id


class Hint(Elem):
    def __init__(self):
        super().__init__(Id.HINT)