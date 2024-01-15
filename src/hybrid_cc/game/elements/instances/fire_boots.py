from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Id


class FireBoots(Elem):
    instance = None

    def __init__(self, **kwargs):
        super().__init__(Id.FIRE_BOOTS)

    @classmethod
    def new(cls, **kwargs):
        if not cls.instance:
            cls.instance = cls(**kwargs)
        return cls.instance

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    def do_planning(self):
        raise NotImplementedError("Implement or remove.")

    # --------------------------------------------------------------------------
    # INSTANCE BOOKKEEPING
    # --------------------------------------------------------------------------
    def construct_at(self, position):
        raise NotImplementedError("Implement or remove.")

    def destruct_at(self, position):
        raise NotImplementedError("Implement or remove.")

    def clone(self):
        raise NotImplementedError("Implement or remove.")

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    def test_enter(self, position, other, direction):
        raise NotImplementedError("Implement or remove.")

    def test_exit(self, position, other, direction):
        raise NotImplementedError("Implement or remove.")

    def start_enter(self, position, other, direction):
        raise NotImplementedError("Implement or remove.")

    def start_exit(self, position, other, direction):
        raise NotImplementedError("Implement or remove.")

    def finish_exit(self, position, other, direction):
        raise NotImplementedError("Implement or remove.")

    def finish_enter(self, position, other, direction):
        raise NotImplementedError("Implement or remove.")
