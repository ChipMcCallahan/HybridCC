import logging
from collections import defaultdict

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import MoveRequest, UIInteractionRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR, CHANNEL
from hybrid_cc.shared.tag import SPEED_BOOST, FORCED


class Teleport(Elem):
    kwarg_filter = (COLOR, CHANNEL)  # Retain these kwargs only.
    positions = defaultdict(list)  # Map from (color, channel) to ordered
    # list of positions
    mobs = {}  # Map from mob_id to (mob, color, channel, position) for mobs in

    # need of teleportation.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.positions.clear()
        cls.mobs.clear()

    @classmethod
    def construct_at(cls, p, **kwargs):
        result = super().construct_at(p, **kwargs)
        color, channel = kwargs[COLOR], kwargs[CHANNEL]
        cls.positions[(color, channel)].append(p)
        # sort by z ascending, y descending, x descending
        cls.positions[(color, channel)].sort(key=lambda t: (t[2], -t[1], -t[0]))
        return result
    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    @classmethod
    def do_class_planning(cls, **kwargs):
        to_remove = []
        moves = []
        requests = []
        for mob_id, entry in cls.mobs.items():
            mob, color, channel, p = entry
            if not mob.exists():
                to_remove.append(mob_id)
                continue
            if mob.id == Id.PLAYER:
                requests = [UIInteractionRequest(src=mob, tgt=cls, p=mob.p,
                                                 type="use")]
            positions = cls.positions[(color, channel)]
            index = positions.index(p)
            start = (index + 1) % len(positions)
            choices = positions[start:] + positions[0:start]
            moves.extend([MoveRequest(mob_id=mob_id, d=mob.d,
                                      simulated_p=choice)
                          for choice in choices])
        for mob_id in to_remove:
            cls.mobs.pop(mob_id, None)
        return moves, requests

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    def finish_exit(self, mob, p, d):
        self.mobs.pop(mob.mob_id, None)

    def finish_enter(self, mob, p, d):
        if mob.id == Id.PLAYER:
            # Otherwise Player would get a free move
            mob.untag(SPEED_BOOST)
            mob.untag(FORCED)
        self.mobs[mob.mob_id] = (mob, self.color, self.channel, p)
