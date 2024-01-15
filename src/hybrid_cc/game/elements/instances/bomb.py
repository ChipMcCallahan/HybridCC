from hybrid_cc.game.constants import DESTROY
from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Id


class Bomb(Elem):
    instance = None

    def __init__(self, **kwargs):
        super().__init__(Id.BOMB)

    @classmethod
    def new(cls, **kwargs):
        if not cls.instance:
            cls.instance = cls(**kwargs)
        return cls.instance
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
