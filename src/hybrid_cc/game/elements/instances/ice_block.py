import logging

from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.game.request import MoveRequest
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import FAILED_MOVE, PUSHES, ENTERS_DIRT


class IceBlock(Mob):
    kwarg_filter = tuple()  # Retain these kwargs only.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag(ENTERS_DIRT)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    def do_planning(self, inputs="", tick=None, **kwargs):
        self.untag(FAILED_MOVE)

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    def test_enter(self, mob, position, direction):
        if self.tagged(FAILED_MOVE) == direction:
            return MoveResult.FAIL, []
        if mob.tagged(PUSHES) or mob.id == self.id:
            return MoveResult.PASS, []
        return MoveResult.FAIL, []

    def start_enter(self, mob, position, direction):
        return MoveResult.FAIL, [
            MoveRequest(mob_id=self.mob_id, direction=direction),
            MoveRequest(mob_id=mob.mob_id, direction=direction),
        ]

    # --------------------------------------------------------------------------
    # OTHER
    # --------------------------------------------------------------------------
    def on_failed_move(self, move_result, d):
        self.tag(FAILED_MOVE, d)
