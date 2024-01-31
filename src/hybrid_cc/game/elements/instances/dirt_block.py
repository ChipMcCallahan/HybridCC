import logging

from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.game.request import MoveRequest
from hybrid_cc.shared import Id, Direction
from hybrid_cc.shared.kwargs import COLOR
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import PUSHES, FAILED_MOVE, MOVED, PUSHABLE


class DirtBlock(Mob):
    kwarg_filter = (COLOR,)  # Retain these kwargs only.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag(PUSHABLE)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------
    def do_planning(self, inputs="", tick=None, **kwargs):
        self.untag(MOVED)
        for d in "NESW":
            self.untag((FAILED_MOVE, Direction[d]))
        return [], []

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def test_enter(self, mob, position, direction):
        if self.tagged(MOVED) or self.tagged((FAILED_MOVE, direction)):
            return MoveResult.FAIL, []
        if mob.tagged(PUSHES):
            return MoveResult.PASS, []
        return MoveResult.FAIL, []

    def start_enter(self, mob, position, direction):
        return MoveResult.RETRY, [
            MoveRequest(mob_id=self.mob_id, direction=direction),
        ]

    # --------------------------------------------------------------------------
    # OTHER
    # --------------------------------------------------------------------------
    def on_completed_move(self, old_p, new_p, tick):
        super().on_completed_move(old_p, new_p, tick)
        self.tag(MOVED)

    def on_failed_move(self, move_result, d):
        self.tag((FAILED_MOVE, d))
