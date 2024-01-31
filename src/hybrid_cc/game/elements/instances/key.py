import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest
from hybrid_cc.shared.key_rule import KeyRule
from hybrid_cc.shared.kwargs import COLOR, RULE, COUNT
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import COLLECTS_ITEMS, ENTERS_DIRT


class Key(Elem):
    kwarg_filter = (COLOR, RULE, COUNT)  # Retain these kwargs only.

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
    def test_enter(self, mob, position, direction):
        if self.rule == KeyRule.ACTING_DIRT and not mob.tagged(ENTERS_DIRT):
            return MoveResult.FAIL, []
        return MoveResult.PASS, []

    def finish_enter(self, mob, position, direction):
        if mob.tagged(COLLECTS_ITEMS):
            if self.count == "+" or mob.keys[self.color] == "+":
                mob.keys[self.color] = "+"
            else:
                mob.keys[self.color] += self.count
            return [DestroyRequest(target=self, pos=position)]
