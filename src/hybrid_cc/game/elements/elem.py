from abc import ABC

from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import DIRECTION, RULE, COLOR, COUNT, \
    CHANNEL, SIDES, Kwargs


# ABC enforces that all subclasses must implement @abstractmethod methods.
class Elem(ABC):
    class_id = Id.DEFAULT
    kwarg_filter = (DIRECTION, COLOR, COUNT, CHANNEL, RULE, SIDES)
    instances = {}

    def __init__(self, **kwargs):
        super().__init__()
        self._id = Id.from_class_name(self.__class__.__name__)
        self._kwargs = Kwargs.filter(self.__class__.kwarg_filter, **kwargs)

    @classmethod
    def class_lookup_key(cls, **kwargs):
        return Kwargs.to_tuple(id=cls.class_id,
                               **Kwargs.filter(cls.kwarg_filter, **kwargs))

    @property
    def lookup_key(self):
        return self.__class__.class_lookup_key(**self._kwargs)

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

    @classmethod
    def construct_at(cls, pos, **kwargs):
        lookup_key = cls.class_lookup_key(**kwargs)
        if lookup_key not in cls.instances:
            cls.instances[lookup_key] = cls(**kwargs)
        return cls.instances[lookup_key]

    @classmethod
    def destruct_at(cls, pos, **kwargs):
        pass
