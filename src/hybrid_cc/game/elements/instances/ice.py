import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import MoveRequest, UIInteractionRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.tag import SLIDING, OVERRIDDEN, SPEED_BOOST


class Ice(Elem):
    kwarg_filter = tuple()  # Retain these kwargs only.
    sliding = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.sliding.clear()

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------
    @classmethod
    def do_class_planning(cls, **kwargs):
        to_remove = []
        moves = []
        requests = []
        for mob_id, mob in cls.sliding.items():
            if not mob.exists():
                to_remove.append(mob_id)
            else:
                if mob.id == Id.PLAYER:
                    requests.append(
                        UIInteractionRequest(src=mob, tgt=cls, p=mob.p,
                                             type="slide"))
                new_moves = MoveRequest.from_dirs(mob_id,
                                                  (mob.d, mob.d.reverse()))
                moves.extend(new_moves)
        for mob_id in to_remove:
            cls.instances.pop(mob_id, None)
        return moves, requests

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def finish_exit(self, mob, p, d):
        mob.untag(SLIDING)
        mob.untag(OVERRIDDEN)
        self.sliding.pop(mob.mob_id, None)
        if mob.id == Id.PLAYER and not mob.tools[Id.SKATES]:
            mob.tag(SPEED_BOOST)

    def finish_enter(self, mob, p, d):
        if mob.tools[Id.SKATES]:
            return [UIInteractionRequest(src=mob, tgt=self, p=p, type="step")]
        mob.tag(SLIDING, self.id)
        mob.tag(OVERRIDDEN)
        self.sliding[mob.mob_id] = mob
