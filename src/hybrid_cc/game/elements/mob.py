from abc import ABC, abstractmethod

from hybrid_cc.game.elements.elem import Elem


class Mob(Elem):
    def __init__(self, _id):
        super().__init__(_id)

    def construct_at(self, pos, **kwargs):
        pass

    def destruct_at(self, pos, **kwargs):
        pass
