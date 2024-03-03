from dataclasses import dataclass

from hybrid_cc.game.elements.elem import Elem


class Tranimation:
    def __init__(self, item, effect):
        self.item = item
        self.effect = effect
        self.strength = 8


class Tranimations:
    lower = {}
    upper = {}

    @staticmethod
    def __get(p, layer):
        tranim = layer.get(p, None)
        if tranim:
            tranim.strength -= 1
            if tranim.strength == 0:
                layer.pop(p)
        return tranim

    @classmethod
    def add_lower(cls, p, tranim):
        cls.lower[p] = tranim

    @classmethod
    def get_lower(cls, p):
        return cls.__get(p, cls.lower)

    @classmethod
    def add_upper(cls, p, tranim):
        cls.upper[p] = tranim

    @classmethod
    def get_upper(cls, p):
        return cls.__get(p, cls.upper)

    @classmethod
    def reset(cls):
        cls.lower.clear()
        cls.upper.clear()
