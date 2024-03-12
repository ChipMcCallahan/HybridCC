import logging

from hybrid_cc.game.elements.instances.button import Button
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.game.request import DestroyRequest, LoseRequest, MoveRequest, \
    CreateRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR, CHANNEL, DIRECTION
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import SLIDING, OVERRIDDEN


class Tank(Mob):
    kwarg_filter = (COLOR, CHANNEL, DIRECTION)  # Retain these kwargs only.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_signal = 0
        self.facing = None

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    def do_planning(self, **kwargs):
        key = (self.color, self.channel)
        signal = Button.signal[key]
        dpad_d, dpad_signal = Button.dpad_signal[key]
        if dpad_signal and dpad_signal > self.last_signal:
            if not self.tagged(OVERRIDDEN):
                self.facing = dpad_d or self.d
            self.last_signal = dpad_signal
        if signal > self.last_signal:
            if (signal - self.last_signal) % 2 == 1 and not self.tagged(
                    SLIDING):
                if not self.tagged(OVERRIDDEN):
                    self.facing = self.d.reverse()
            self.last_signal = signal
        if self.tagged(SLIDING) or not self.moved_last_n_ticks(n=1):
            self.d = self.facing or self.d
            self.facing = None
        if self.moved_last_n_ticks(n=1):
            return [], []
        return [MoveRequest(mob_id=self.mob_id, d=self.d)], []

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    @staticmethod
    def test_enter(mob, p, d):
        if mob.id == Id.PLAYER:
            return MoveResult.PASS, []
        return MoveResult.FAIL, []

    def finish_enter(self, mob, p, d):
        if mob.id == Id.PLAYER:
            return [
                DestroyRequest(src=self, tgt=mob, p=p),
                DestroyRequest(src=mob, tgt=self, p=p),
                LoseRequest(cause=self, p=p)
            ]

    # --------------------------------------------------------------------------
    # OTHER
    # --------------------------------------------------------------------------

    def on_completed_move(self, old_p, new_p, **kwargs):
        super().on_completed_move(old_p, new_p, **kwargs)
        return [CreateRequest(p=old_p, id=Id.PLACEHOLDER)]
