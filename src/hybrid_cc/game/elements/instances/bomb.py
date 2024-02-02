import logging

from hybrid_cc.game.constants import DESTROY
from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest, LoseRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR


class Bomb(Elem):
    kwarg_filter = (COLOR,)  # Retain the COLOR kwarg, drop the rest.

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

    def finish_enter(self, mob, position, direction):
        requests = [
            DestroyRequest(target=self, pos=position),
            DestroyRequest(target=mob, pos=position)
        ]
        if mob.id == Id.PLAYER:
            requests.append(LoseRequest(cause=self, pos=position))
        return requests
