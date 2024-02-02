import logging

from hybrid_cc.game.elements.instances.button import Button
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.game.request import DestroyRequest, LoseRequest, MoveRequest, \
    CreateRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR, CHANNEL, DIRECTION
from hybrid_cc.shared.move_result import MoveResult


class Tank(Mob):
    kwarg_filter = (COLOR, CHANNEL, DIRECTION)  # Retain these kwargs only.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_signal = 0

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    def do_planning(self, tick, **kwargs):
        if self.moved_last_n_ticks(tick, n=1):
            return [], []

        key = (self.color, self.channel)
        signal = Button.signal[key]
        dpad_direction, dpad_signal = Button.dpad_signal[key]
        if dpad_signal and dpad_signal > self.last_signal:
            self.direction = dpad_direction or self.direction
            self.last_signal = dpad_signal
        if signal > self.last_signal:
            self.direction = self.direction.reverse()
            self.last_signal = signal
        return [MoveRequest(mob_id=self.mob_id, direction=self.direction)], []

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    @staticmethod
    def test_enter(mob, p, direction):
        if mob.id == Id.PLAYER:
            return MoveResult.PASS, []
        return MoveResult.FAIL, []

    def finish_enter(self, mob, p, direction):
        if mob.id == Id.PLAYER:
            return [
                DestroyRequest(target=mob, p=p),
                DestroyRequest(target=self, p=p),
                LoseRequest(cause=self, p=p)
            ]

    # --------------------------------------------------------------------------
    # OTHER
    # --------------------------------------------------------------------------

    def on_completed_move(self, old_p, new_p, tick, **kwargs):
        super().on_completed_move(old_p, new_p, tick, **kwargs)
        return [CreateRequest(p=old_p, id=Id.PLACEHOLDER)]
