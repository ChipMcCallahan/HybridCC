import logging

from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.shared.tag import PUSHING
from hybrid_cc.shared import Direction
from hybrid_cc.shared.kwargs import DIRECTION


class Player(Mob):
    kwarg_filter = (DIRECTION,)  # Retain these kwargs only.
    instance = None
    collects_chips = True
    collects_items = True
    enters_dirt = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tags[PUSHING] = False
        if self.__class__.instance:
            raise ValueError("Cannot have more than one Player instance!")
        self.__class__.instance = self

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.instance = None

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    def do_planning(self, inputs="", tick=None, **kwargs):
        self.tags[PUSHING] = False
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
        self.tags[PUSHING] = False
        super().finalize_move(old_p, new_p, tick)

    def on_failed_move(self, move_result, d):
        self.tags[PUSHING] = True
        self.direction = d
