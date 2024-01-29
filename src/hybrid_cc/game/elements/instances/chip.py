import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR, COUNT
from hybrid_cc.shared.move_result import MoveResult


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
    @classmethod
    def do_class_planning(cls, **kwargs):
        pass

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    @staticmethod
    def test_enter(mob, position, direction):
        if mob.enters_dirt:
            return MoveResult.PASS, []
        return MoveResult.FAIL, []

    def finish_enter(self, mob, position, direction):
        if mob.collects_chips:
            current = self.chips_collected.get(self.color, 0)
            self.chips_collected[self.color] = current + self.count

            return [
                DestroyRequest(target=self, pos=position),
            ]
