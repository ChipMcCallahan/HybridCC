import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest
from hybrid_cc.shared.kwargs import COLOR, COUNT
from hybrid_cc.shared.move_result import MoveResult


class Door(Elem):
    kwarg_filter = (COLOR, COUNT)  # Retain these kwargs only.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    def test_enter(self, mob, p, direction):
        if self.color in mob.keys:
            count = mob.keys[self.color]
            if count == "+" or count >= self.count:
                return MoveResult.PASS, []
        return MoveResult.FAIL, []

    def finish_enter(self, mob, p, direction):
        if self.color in mob.keys:
            count = mob.keys[self.color]
            if count != "+" and count >= self.count:
                mob.keys[self.color] -= self.count
                if mob.keys[self.color] <= 0:
                    mob.keys.pop(self.color)
            return [
                DestroyRequest(target=self, p=p)
            ]
