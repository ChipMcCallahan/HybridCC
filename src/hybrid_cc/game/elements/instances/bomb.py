from hybrid_cc.game.constants import DESTROY
from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR


class Bomb(Elem):
    kwarg_filter = (COLOR,)  # Retain the COLOR kwarg, drop the rest.
    instances = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def construct_at(cls, pos, **kwargs):
        lookup_key = cls.class_lookup_key(**kwargs)
        if lookup_key not in cls.instances:
            cls.instances[lookup_key] = cls(**kwargs)
        return cls.instances[lookup_key]

    @classmethod
    def destruct_at(cls, pos, **kwargs):
        pass

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def finish_enter(self, position, other, direction):
        return ((DESTROY, self, position),
                (DESTROY, other, position))
