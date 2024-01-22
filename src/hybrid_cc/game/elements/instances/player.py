import logging

from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.shared import Id, Direction
from hybrid_cc.shared.kwargs import DIRECTION


class Player(Mob):
    kwarg_filter = (DIRECTION,)  # Retain these kwargs only.
    position = None  # Store position at the class level for easy finding.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pushing = False

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.position = None

    @classmethod
    def construct_at(cls, pos, **kwargs):
        cls.position = pos
        return super().construct_at(pos, **kwargs)

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    def do_planning(self, inputs="", tick=None, **kwargs):
        self.pushing = False
        if None not in (tick, self.last_move_tick):
            if tick - self.last_move_tick <= 1:
                return
        return self.mob_id, [Direction[d] for d in inputs]

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    def test_enter(self, mob, position, direction):
        raise NotImplementedError("Implement or remove.")

    def test_exit(self, mob, position, direction):
        raise NotImplementedError("Implement or remove.")

    def start_enter(self, mob, position, direction):
        raise NotImplementedError("Implement or remove.")

    def start_exit(self, mob, position, direction):
        raise NotImplementedError("Implement or remove.")

    def finish_exit(self, mob, position, direction):
        raise NotImplementedError("Implement or remove.")

    def finish_enter(self, mob, position, direction):
        raise NotImplementedError("Implement or remove.")

    # --------------------------------------------------------------------------
    # OTHER
    # --------------------------------------------------------------------------

    def finalize_move(self, old_p, new_p, tick):
        self.pushing = False
        super().finalize_move(old_p, new_p, tick)
        self.__class__.position = self.position

    def on_failed_move(self, move_result, d):
        self.pushing = True
        self.direction = d
