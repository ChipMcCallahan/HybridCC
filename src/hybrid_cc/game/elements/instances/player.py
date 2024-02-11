import logging

from hybrid_cc.game.clock import Clock
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.game.request import MoveRequest, DestroyRequest, LoseRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import PUSHING, PUSHES, COLLECTS_CHIPS, \
    COLLECTS_ITEMS, ENTERS_DIRT, FORCED, OVERRIDDEN, SLIDING, SPEED_BOOST
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
    @classmethod
    def do_class_planning(cls, **kwargs):
        # This method is a hack to allow Player to be overridden for the
        # first tick of the game if starting on a FF.
        overridden = cls.instance.tagged(OVERRIDDEN)
        on_ff = cls.instance.tagged(SLIDING) == Id.FORCE

        if overridden and on_ff and Clock.tick > 0:
            cls.instance.untag(OVERRIDDEN)
        return None, None

    def do_planning(self, **kwargs):
        inputs = kwargs.get("inputs", [])
        self.untag(PUSHING)

        if self.moved_last_n_ticks(n=1) and not self.tagged(
                FORCED) and not self.tagged(SPEED_BOOST):
            return [], []

        self.untag(SPEED_BOOST)
        if not self.tagged(OVERRIDDEN):
            self.untag(FORCED)
        self.last_move_tick = None

        primary, secondary = inputs
        if self.d in inputs and self.d != primary:
            primary, secondary = secondary, primary
        moves = []
        if primary:
            moves.append(
                MoveRequest(mob_id=self.mob_id, d=primary,
                            slap=secondary)
            )
        if secondary:
            moves.append(
                MoveRequest(mob_id=self.mob_id, d=secondary)
            )
        return moves, []

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    def test_enter(self, mob, p, d):
        if mob.id == Id.PLAYER:
            return MoveResult.FAIL, []
        return MoveResult.PASS, []

    def finish_enter(self, mob, p, d):
        return [
            DestroyRequest(src=mob, tgt=self, p=p),
            LoseRequest(cause=mob, p=p)
        ]

    # --------------------------------------------------------------------------
    # OTHER
    # --------------------------------------------------------------------------

    def on_completed_move(self, old_p, new_p, **kwargs):
        super().on_completed_move(old_p, new_p, **kwargs)
        self.untag(PUSHING)

    def on_failed_move(self, move_result, d):
        super().on_failed_move(move_result, d)
        self.d = d
        self.tag(PUSHING)
