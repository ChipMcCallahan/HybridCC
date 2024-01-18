from hybrid_cc.game.constants import DESTROY
from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR


class Bomb(Elem):
    kwarg_filter = (COLOR,)  # Retain the COLOR kwarg, drop the rest.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def finish_enter(self, position, other, direction):
        return ((DESTROY, self, position),
                (DESTROY, other, position))
