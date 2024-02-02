import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest, LoseRequest, CreateRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.monster_rule import MonsterRule
from hybrid_cc.shared.tag import SWIMMING


class Water(Elem):
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
    def finish_exit(mob, position, direction):
        mob.untag(SWIMMING)

    def finish_enter(self, mob, position, direction):
        if mob.id == Id.MONSTER and mob.rule == MonsterRule.GLIDER:
            return
        if mob.tools[Id.FLIPPERS]:
            mob.tag(SWIMMING)
            return

        requests = [DestroyRequest(target=mob, pos=position)]
        if mob.id == Id.PLAYER:
            requests.append(LoseRequest(cause=self, pos=position))
        elif mob.id == Id.DIRT_BLOCK:
            requests.extend([
                DestroyRequest(target=self, pos=position),
                CreateRequest(pos=position, id=Id.DIRT, color=mob.color)
            ])
        elif mob.id == Id.ICE_BLOCK:
            requests.extend([
                DestroyRequest(target=self, pos=position),
                CreateRequest(pos=position, id=Id.ICE)
            ])
        return requests
