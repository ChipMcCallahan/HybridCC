import logging
from abc import ABC, abstractmethod

from hybrid_cc.game.elements.elem import Elem


class Mob(Elem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.instances.clear()

    @classmethod
    def construct_at(cls, pos, **kwargs):
        # mobs instantiate a new instance every time
        return cls(**kwargs)
