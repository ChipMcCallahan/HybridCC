from abc import ABC, abstractmethod

from hybrid_cc.shared.kwargs import DIRECTION, RULE, COLOR, COUNT, \
    CHANNEL, SIDES


# ABC enforces that all subclasses must implement @abstractmethod methods.
class Elem(ABC):
    def __init__(self, _id, **kwargs):
        super().__init__()
        self._id = _id
        self._kwargs = kwargs

    @property
    def id(self):
        return self._id

    @property
    def layer(self):
        return self._id.layer()

    @property
    def direction(self):
        return self._kwargs[DIRECTION]

    @direction.setter
    def direction(self, value):
        self._kwargs[DIRECTION] = value

    @property
    def rule(self):
        return self._kwargs[RULE]

    @rule.setter
    def rule(self, value):
        self._kwargs[RULE] = value

    @property
    def color(self):
        return self._kwargs[COLOR]

    @color.setter
    def color(self, value):
        self._kwargs[COLOR] = value

    @property
    def count(self):
        return self._kwargs[COUNT]

    @count.setter
    def count(self, value):
        self._kwargs[COUNT] = value

    @property
    def channel(self):
        return self._kwargs[CHANNEL]

    @channel.setter
    def channel(self, value):
        self._kwargs[CHANNEL] = value

    @property
    def sides(self):
        return self._kwargs[SIDES]

    @sides.setter
    def sides(self, value):
        self._kwargs[SIDES] = value

    @abstractmethod
    def construct_at(self, pos, **kwargs):
        pass

    @abstractmethod
    def destruct_at(self, pos, **kwargs):
        pass
