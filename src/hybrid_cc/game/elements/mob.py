import logging
from collections import defaultdict

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
        self.tags = set()
        self.mob_id = Mob._next_mob_id
        Mob.instances[self.mob_id] = self
        Mob._next_mob_id += 1
        self._position = None
        self.last_move_tick = None
        self.keys = defaultdict(int)
        self.tools = defaultdict(int)

    def finalize_move(self, old_p, new_p, tick):
        self.position = new_p
        self.direction = Direction.from_move(old_p, new_p)
        self.last_move_tick = tick

    def tag(self, tag):
        self.tags.add(tag)

    def untag(self, tag):
        self.tags.discard(tag)

    def tagged(self, tag):
        return tag in self.tags

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.instances.clear()
        cls._next_mob_id = 0

    @classmethod
    def construct_at(cls, pos, **kwargs):
        # mobs instantiate a new instance every time
        mob = cls(**kwargs)
        mob.position = pos
        return mob

    @classmethod
    def destruct_at(cls, elem, pos):
        cls.instances.pop(elem.mob_id)

    @classmethod
    def get_mob(cls, mob_id):
        return cls.instances.get(mob_id, None)

    @classmethod
    def exists(cls, mob_id):
        return mob_id in cls.instances
