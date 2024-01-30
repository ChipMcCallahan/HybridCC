import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.elements.instances.chip import Chip
from hybrid_cc.game.request import DestroyRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR, COUNT
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import ENTERS_DIRT


class Socket(Elem):
    kwarg_filter = (COLOR, COUNT)  # Retain these kwargs only.
    chips_required = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        cls.chips_required.clear()

    @classmethod
    def set_chips_required(cls, chips_required):
        cls.chips_required = chips_required

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def test_enter(self, mob, position, direction):
        if mob.tagged(ENTERS_DIRT):
            chips = Chip.chips_collected.get(self.color, 0)
            if chips >= self.chips_required[self.color]:
                return MoveResult.PASS, None
        return MoveResult.FAIL, None

    def finish_enter(self, mob, position, direction):
        return [
            DestroyRequest(target=self, pos=position),
        ]
