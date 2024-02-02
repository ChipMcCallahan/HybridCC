import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest, LoseRequest, CreateRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.monster_rule import MonsterRule
from hybrid_cc.shared.move_result import MoveResult


class Fire(Elem):
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
    def test_enter(mob, position, direction):
        if mob.id == Id.MONSTER and mob.rule != MonsterRule.FIREBALL:
            return MoveResult.FAIL, None
        return MoveResult.PASS, None

    def finish_enter(self, mob, position, direction):
        if mob.id == Id.PLAYER and not mob.tools[Id.FIRE_BOOTS]:
            return [DestroyRequest(target=mob, pos=position),
                    LoseRequest(cause=self, pos=position)]
        if mob.id == Id.ICE_BLOCK:
            return [DestroyRequest(target=self, pos=position),
                    DestroyRequest(target=mob, pos=position),
                    CreateRequest(id=Id.WATER, pos=position)]
