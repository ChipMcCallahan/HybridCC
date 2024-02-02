import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import HideHintRequest, ShowHintRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import ENTERS_DIRT


class Hint(Elem):
    kwarg_filter = tuple()  # Retain these kwargs only.

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
    @staticmethod
    def test_enter(mob, p, d):
        if mob.tagged(ENTERS_DIRT):
            return MoveResult.PASS, []
        return MoveResult.FAIL, []

    @staticmethod
    def finish_exit(mob, p, d):
        if mob.id == Id.PLAYER:
            return [HideHintRequest()]

    @staticmethod
    def finish_enter(mob, p, d):
        if mob.id == Id.PLAYER:
            return [ShowHintRequest()]
