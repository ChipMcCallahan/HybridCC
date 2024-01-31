import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import MoveRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.tag import SLIDING, OVERRIDDEN


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
        requests = []
        for mob_id, mob in cls.sliding.items():
            if not mob.exists():
                to_remove.append(mob_id)
            else:
                moves = MoveRequest.from_directions(mob_id,
                                                    (mob.direction,
                                                     mob.direction.reverse()))
                requests.extend(moves)
        for mob_id in to_remove:
            cls.instances.pop(mob_id, None)
        return requests, []

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def finish_exit(self, mob, position, direction):
        mob.untag(SLIDING)
        mob.untag(OVERRIDDEN)
        self.sliding.pop(mob.mob_id, None)

    def finish_enter(self, mob, position, direction):
        if not mob.tools[Id.SKATES]:
            mob.tag(SLIDING, self.id)
            mob.tag(OVERRIDDEN)
            self.sliding[mob.mob_id] = mob
