from abc import ABC, abstractmethod

from hybrid_cc.game.elements.elem import Elem


class Mob(Elem):
    def __init__(self, _id, **kwargs):
        super().__init__(_id, **kwargs)

    def construct_at(self, pos, **kwargs):
        pass

    def destruct_at(self, pos, **kwargs):
        pass
