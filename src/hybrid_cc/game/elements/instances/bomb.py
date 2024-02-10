import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.elements.instances.button import Button
from hybrid_cc.game.request import DestroyRequest, LoseRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR, CHANNEL, RULE


class Bomb(Elem):
    kwarg_filter = (COLOR, RULE, CHANNEL)  # Retain these kwargs, drop the rest.

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

    def finish_enter(self, mob, p, d):
        key = (self.color, self.channel)
        toggle_state = Button.signal[key] % 2
        should_explode = (self.rule.value + toggle_state) % 2 == 0
        if should_explode:
            requests = [
                DestroyRequest(src=mob, tgt=self, p=p),
                DestroyRequest(src=self, tgt=mob, p=p)
            ]
            if mob.id == Id.PLAYER:
                requests.append(LoseRequest(cause=self, p=p))
            return requests
        else:
            return [
                DestroyRequest(src=mob, tgt=self, p=p)
            ]
