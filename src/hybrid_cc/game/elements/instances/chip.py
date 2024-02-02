from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest
from hybrid_cc.shared.kwargs import COLOR, COUNT
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import COLLECTS_CHIPS, ENTERS_DIRT


class Chip(Elem):
    kwarg_filter = (COLOR, COUNT)  # Retain these kwargs only.
    chips_collected = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        cls.chips_collected.clear()

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------


    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    @staticmethod
    def test_enter(mob, p, direction):
        if mob.tagged(ENTERS_DIRT):
            return MoveResult.PASS, []
        return MoveResult.FAIL, []

    def finish_enter(self, mob, p, direction):
        if mob.tagged(COLLECTS_CHIPS):
            current = self.chips_collected.get(self.color, 0)
            self.chips_collected[self.color] = current + self.count

            return [
                DestroyRequest(target=self, p=p),
            ]
