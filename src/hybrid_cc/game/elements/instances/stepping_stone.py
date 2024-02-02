import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import CreateRequest, DestroyRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import RULE, COUNT
from hybrid_cc.shared.stepping_stone_rule import SteppingStoneRule


class SteppingStone(Elem):
    kwarg_filter = (RULE, COUNT)  # Retain these kwargs only.

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
    def finish_exit(self, mob, position, direction):
        if self.count > 1:
            create_request = CreateRequest(id=self.id,
                                           pos=position,
                                           count=self.count - 1,
                                           rule=self.rule)
        elif self.rule == SteppingStoneRule.WATER:
            create_request = CreateRequest(id=Id.WATER, pos=position)
        else:
            create_request = CreateRequest(id=Id.FIRE, pos=position)
        return [
            DestroyRequest(target=self, pos=position),
            create_request
        ]
