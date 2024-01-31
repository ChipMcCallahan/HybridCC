import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import MoveRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import DIRECTION, RULE, COLOR
from hybrid_cc.shared.tag import FORCED, OVERRIDDEN, SLIDING


class Force(Elem):
    kwarg_filter = (COLOR, RULE, DIRECTION)  # Retain these kwargs only.
    hovering = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.hovering.clear()

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------
    @classmethod
    def do_class_planning(cls, **kwargs):
        to_remove = []
        requests = []
        for mob_id, entry in cls.hovering.items():
            mob, direction = entry
            if not mob.exists():
                to_remove.append(mob_id)
            else:
                moves = MoveRequest.from_directions(mob_id,
                                                    (direction,))
                requests.extend(moves)
        for mob_id in to_remove:
            cls.instances.pop(mob_id, None)
        return requests, []

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def finish_exit(self, mob, position, direction):
        if (mob.id == Id.PLAYER and
                direction == self.direction and not
                mob.tools[Id.SUCTION_BOOTS]):
            mob.tag(FORCED)
        mob.untag(OVERRIDDEN)
        mob.untag(SLIDING)
        self.hovering.pop(mob.mob_id, None)

    def finish_enter(self, mob, position, direction):
        if mob.tools[Id.SUCTION_BOOTS]:
            return
        if mob.id != Id.PLAYER:
            mob.tag(OVERRIDDEN)
        mob.tag(SLIDING)
        self.hovering[mob.mob_id] = (mob, self.direction)
