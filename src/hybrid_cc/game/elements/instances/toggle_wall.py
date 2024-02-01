import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.elements.instances.button import Button
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR, RULE, CHANNEL
from hybrid_cc.shared.move_result import MoveResult


class ToggleWall(Elem):
    kwarg_filter = (COLOR, RULE, CHANNEL)  # Retain these kwargs only.

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
        key = (self.color, self.channel)
        toggle_state = Button.signal[key] % 2
        if (self.rule.value + toggle_state) % 2 == 0:
            return MoveResult.PASS, []
        return MoveResult.FAIL, []
