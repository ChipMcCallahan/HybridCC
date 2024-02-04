import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import MoveRequest, UIInteractionRequest
from hybrid_cc.game.rng import RNG
from hybrid_cc.shared import Id, Direction
from hybrid_cc.shared.force_rule import ForceRule
from hybrid_cc.shared.kwargs import DIRECTION, RULE, COLOR
from hybrid_cc.shared.tag import FORCED, OVERRIDDEN, SLIDING, SPEED_BOOST


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
        moves = []
        requests = []
        for mob_id, entry in cls.hovering.items():
            mob, d = entry
            if not mob.exists():
                to_remove.append(mob_id)
                continue
            if d:
                dirs = [d]
            else:
                pool = [Direction[d] for d in "NESW"]
                dirs = []
                while len(pool) > 0:
                    dirs.append(pool.pop(RNG.next() % len(pool)))
            if mob.id == Id.PLAYER:
                requests.append([UIInteractionRequest(src=mob, tgt=cls, p=mob.p,
                                                      type="slide")])
            new_moves = MoveRequest.from_dirs(mob_id, dirs)
            moves.extend(new_moves)
        for mob_id in to_remove:
            cls.instances.pop(mob_id, None)
        return moves, requests

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def finish_exit(self, mob, p, d):
        if (mob.id == Id.PLAYER and not
        mob.tools[Id.SUCTION_BOOTS]):
            if self.rule == ForceRule.RANDOM or self.d == d:
                mob.tag(FORCED)
                mob.tag(SPEED_BOOST)
        mob.untag(OVERRIDDEN)
        mob.untag(SLIDING)
        self.hovering.pop(mob.mob_id, None)

    def finish_enter(self, mob, p, d):
        if mob.tools[Id.SUCTION_BOOTS]:
            return [UIInteractionRequest(src=mob, tgt=self, p=p, type="step")]
        if mob.id != Id.PLAYER:
            mob.tag(OVERRIDDEN)
        mob.tag(SLIDING, self.id)
        if self.rule == ForceRule.RANDOM:
            self.hovering[mob.mob_id] = (mob, None)
        else:
            mob.d = self.d
            self.hovering[mob.mob_id] = (mob, self.d)

    # --------------------------------------------------------------------------
    # OTHER
    # --------------------------------------------------------------------------
    def construct_mob_here(self, mob, p):
        if mob.id == Id.PLAYER:
            mob.tag(OVERRIDDEN)  # Prevent move on first tick.
        self.finish_enter(mob, p, mob.d)
