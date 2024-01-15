DIRECTION = "direction"
RULE = "rule"
COLOR = "color"
COUNT = "count"
CHANNEL = "channel"
SIDES = "sides"


class Kwargs:
    @staticmethod
    def filter(_filter, **kwargs):
        return {k: v for k, v in kwargs.items() if k in _filter}

    @staticmethod
    def to_tuple(**kwargs):
        return tuple(sorted(kwargs.items()))

    @staticmethod
    def from_tuple(_tuple):
        return {k: v for k, v in _tuple}
