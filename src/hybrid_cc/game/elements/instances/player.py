import logging

from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.game.request import MoveRequest, DestroyRequest, LoseRequest
from hybrid_cc.shared.tag import PUSHING, PUSHES, COLLECTS_CHIPS, \
    COLLECTS_ITEMS, ENTERS_DIRT
from hybrid_cc.shared import Direction
from hybrid_cc.shared.kwargs import DIRECTION


class Player(Mob):
    kwarg_filter = (DIRECTION,)  # Retain these kwargs only.
    instance = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.__class__.instance:
            raise ValueError("Cannot have more than one Player instance!")
        self.__class__.instance = self
        self.tag(COLLECTS_CHIPS)
        self.tag(COLLECTS_ITEMS)
        self.tag(ENTERS_DIRT)
        self.tag(PUSHES)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.instance = None

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    def do_planning(self, inputs=None, tick=None, **kwargs):
        inputs = inputs or []
        self.untag(PUSHING)
        if None not in (tick, self.last_move_tick):
            if tick - self.last_move_tick <= 1:
                return [], []
        primary, secondary = (inputs + [None, None])[0:2]
        if self.direction in inputs and self.direction != primary:
            primary, secondary = secondary, primary
        moves = []
        if primary:
            moves.append(
                MoveRequest(mob_id=self.mob_id, direction=primary,
                            slap=secondary)
            )
        if secondary:
            moves.append(
                MoveRequest(mob_id=self.mob_id, direction=secondary)
            )
        return moves, []

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def finish_enter(self, mob, position, direction):
        return [
            DestroyRequest(target=self, pos=position),
            LoseRequest(cause=mob)
        ]

    # --------------------------------------------------------------------------
    # OTHER
    # --------------------------------------------------------------------------

    def on_completed_move(self, old_p, new_p, tick):
        super().on_completed_move(old_p, new_p, tick)
        self.untag(PUSHING)

    def on_failed_move(self, move_result, d):
        self.tag(PUSHING)
        self.direction = d
