from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Id


class Thief(Elem):
    instance = None

    def __init__(self, **kwargs):
        super().__init__(Id.THIEF)

    @classmethod
    def construct_at(cls, pos, **kwargs):
        if not cls.instance:
            cls.instance = cls(**kwargs)
        return cls.instance

    @classmethod
    def destruct_at(cls, pos, **kwargs):
        pass

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    def do_planning(self):
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
