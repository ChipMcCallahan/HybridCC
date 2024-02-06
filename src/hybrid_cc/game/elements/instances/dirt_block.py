import logging

from hybrid_cc.game.elements.instances.player import Player
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.game.request import MoveRequest, UIInteractionRequest
from hybrid_cc.shared import Direction, Id
from hybrid_cc.shared.kwargs import COLOR, DIRECTION
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import PUSHES, FAILED_MOVE, MOVED, PUSHABLE, SLIDING, \
    PUSHED, RETRY_MOVE


class DirtBlock(Mob):
    kwarg_filter = (COLOR, DIRECTION)  # Retain these kwargs only.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tag(PUSHABLE)
        self.mobs_to_untag = []

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------
    def do_planning(self, tick, **kwargs):
        self.untag(MOVED)
        for d in "NESW":
            self.untag((FAILED_MOVE, Direction[d]))
        for mob in self.mobs_to_untag:
            mob.untag(RETRY_MOVE)
        self.mobs_to_untag.clear()
        return [], []

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def test_enter(self, mob, p, d):
        if mob.tagged(PUSHES):
            return MoveResult.PASS, []
        return MoveResult.FAIL, []

    def start_enter(self, mob, p, d):
        # if we already failed in this direction, don't retry unless sliding
        if self.tagged((FAILED_MOVE, d)) and not self.tagged(SLIDING):
            return MoveResult.FAIL, []

        # if we already moved, don't move again. exception if we are sliding
        # and the push is orthogonal
        if self.tagged(MOVED):
            if not (self.tagged(SLIDING) and self.d in (
                    d.right(), d.left())):
                return MoveResult.FAIL, []
        self.tag(PUSHED, mob)
        if mob.tagged(RETRY_MOVE) != self:
            mob.tag(RETRY_MOVE, self)
            self.mobs_to_untag.append(mob)
            return MoveResult.RETRY, [
                MoveRequest(mob_id=self.mob_id, d=d),
            ]
        else:
            mob.untag(RETRY_MOVE)
            return MoveResult.FAIL, []

    # --------------------------------------------------------------------------
    # OTHER
    # --------------------------------------------------------------------------
    def on_completed_move(self, old_p, new_p, tick, **kwargs):
        super().on_completed_move(old_p, new_p, tick, **kwargs)
        self.tag(MOVED)
        pusher = self.untag(PUSHED)
        if pusher:
            return [UIInteractionRequest(src=pusher, tgt=self, p=new_p,
                                         type="push")]

    def on_failed_move(self, move_result, d):
        super().on_failed_move(move_result, d)
        self.tag((FAILED_MOVE, d))
