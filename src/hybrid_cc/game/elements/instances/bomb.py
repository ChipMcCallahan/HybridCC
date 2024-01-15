from hybrid_cc.game.constants import DESTROY
from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Id


class Bomb(Elem):
    instances = {}

    def __init__(self):
        super().__init__(Id.BOMB)

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # INSTANCE BOOKKEEPING
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def finish_enter(self, position, other, direction):
        return ((DESTROY, self, position),
                (DESTROY, other, position))
