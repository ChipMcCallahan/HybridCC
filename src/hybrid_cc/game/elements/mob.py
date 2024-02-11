import logging
from collections import defaultdict

from hybrid_cc.game.clock import Clock
from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Direction


class Mob(Elem):
    _next_mob_id = 0
    instances = {}
    collects_chips = False
    collects_items = False
    enters_dirt = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tags = {}
        self.mob_id = Mob._next_mob_id
        Mob.instances[self.mob_id] = self
        Mob._next_mob_id += 1
        self._p = None
        self.last_move_tick = None
        self.keys = defaultdict(int)
        self.tools = defaultdict(int)

    def on_completed_move(self, old_p, new_p, *, simulated_p=None):
        self.p = new_p
        self.d = Direction.from_move(simulated_p or old_p, new_p)
        self.last_move_tick = Clock.tick

    def on_failed_move(self, move_result, d):
        self.last_move_tick = None

    def exists(self):
        return self.mob_id in Mob.instances

    def moved_last_n_ticks(self, *, n=1):
        return (self.last_move_tick is not None
                and Clock.tick - self.last_move_tick <= n)

    def tag(self, tag, value=True):
        self.tags[tag] = value

    def untag(self, tag):
        return self.tags.pop(tag, None)

    def tagged(self, tag):
        return self.tags.get(tag, False)

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, p):
        self._p = p

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.instances.clear()
        cls._next_mob_id = 0

    @classmethod
    def construct_at(cls, p, **kwargs):
        # mobs instantiate a new instance every time
        mob = cls(**kwargs)
        mob.p = p
        return mob

    @classmethod
    def destruct_at(cls, elem, p):
        cls.instances.pop(elem.mob_id, None)

    @classmethod
    def get_mob(cls, mob_id):
        return cls.instances.get(mob_id, None)
