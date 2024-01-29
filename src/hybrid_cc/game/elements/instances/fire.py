import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest, LoseRequest
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
    @classmethod
    def do_class_planning(cls, **kwargs):
        pass
    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    @staticmethod
    def test_enter(mob, position, direction):
        if mob.id == Id.MONSTER and mob.rule != MonsterRule.FIREBALL:
            return MoveResult.FAIL, None
        return MoveResult.PASS, None

    def finish_enter(self, mob, position, direction):
        if mob.id == Id.MONSTER and mob.rule == MonsterRule.GLIDER:
            return
        if mob.tools[Id.FIRE_BOOTS]:
            return

        requests = [DestroyRequest(target=mob, pos=position)]
        if mob.id == Id.PLAYER:
            requests.append(LoseRequest(cause=self.id))
        return requests
