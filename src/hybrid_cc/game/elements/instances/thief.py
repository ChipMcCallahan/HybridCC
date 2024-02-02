import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared.kwargs import RULE
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import ENTERS_DIRT
from hybrid_cc.shared.thief_rule import ThiefRule


class Thief(Elem):
    kwarg_filter = (RULE,)  # Retain these kwargs only.

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
    @staticmethod
    def test_enter(mob, p, direction):
        if mob.tagged(ENTERS_DIRT):
            return MoveResult.PASS, []
        return MoveResult.FAIL, []

    def finish_enter(self, mob, p, direction):
        if self.rule == ThiefRule.KEYS:
            mob.keys.clear()
        elif self.rule == ThiefRule.TOOLS:
            mob.tools.clear()
