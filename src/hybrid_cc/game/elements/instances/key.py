from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR, RULE, COUNT


class Key(Elem):
    kwarg_filter = (COLOR, RULE, COUNT)  # Retain these kwargs only.
    instances = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
