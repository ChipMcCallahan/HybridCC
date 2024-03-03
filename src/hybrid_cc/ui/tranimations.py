from hybrid_cc.game.clock import Clock


class Tranimation:
    def __init__(self, item, effect):
        self.item = item
        self.effect = effect
        self.tick = Clock.tick
        self.strength = 8


class Tranimations:
    lower = {}
    upper = {}

    @staticmethod
    def __get(p, layer):
        tranim = layer.get(p, None)
        if tranim:
            tranim.strength -= 1
            if Clock.tick - tranim.tick > 1 or tranim.strength < 0:
                layer.pop(p)
                return None
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
