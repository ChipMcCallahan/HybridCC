import logging
from abc import ABC

from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import DIRECTION, RULE, COLOR, COUNT, \
    CHANNEL, SIDES, Kwargs


# ABC enforces that all subclasses must implement @abstractmethod methods.
class Elem(ABC):
    class_id = Id.DEFAULT
    kwarg_filter = (DIRECTION, COLOR, COUNT, CHANNEL, RULE, SIDES)
    instances = {}  # memoization: map lookup key to instance

    def __init__(self, **kwargs):
        super().__init__()
        self._id = Id.from_class_name(self.__class__.__name__)
        self.kwargs = Kwargs.filter(self.__class__.kwarg_filter, **kwargs)

    @classmethod
    def class_lookup_key(cls, **kwargs):
        return Kwargs.to_tuple(id=Id.from_class_name(cls.__name__),
                               **Kwargs.filter(cls.kwarg_filter, **kwargs))

    @property
    def lookup_key(self):
        return self.__class__.class_lookup_key(**self.kwargs)

    @property
    def id(self):
        return self._id

    @property
    def layer(self):
        return self._id.layer()

    @property
    def d(self):
        return self.kwargs.get(DIRECTION)

    @d.setter
    def d(self, value):
        self.kwargs[DIRECTION] = value

    @property
    def rule(self):
        return self.kwargs.get(RULE)

    @rule.setter
    def rule(self, value):
        self.kwargs[RULE] = value

    @property
    def color(self):
        return self.kwargs.get(COLOR)

    @color.setter
    def color(self, value):
        self.kwargs[COLOR] = value

    @property
    def count(self):
        return self.kwargs.get(COUNT)

    @count.setter
    def count(self, value):
        self.kwargs[COUNT] = value

    @property
    def channel(self):
        return self.kwargs.get(CHANNEL)

    @channel.setter
    def channel(self, value):
        self.kwargs[CHANNEL] = value

    @property
    def sides(self):
        return self.kwargs.get(SIDES)

    @sides.setter
    def sides(self, value):
        self.kwargs[SIDES] = value

    @classmethod
    def construct_at(cls, p, **kwargs):
        lookup_key = cls.class_lookup_key(**kwargs)
        if lookup_key not in cls.instances:
            cls.instances[lookup_key] = cls(**kwargs)
        return cls.instances[lookup_key]

    @classmethod
    def destruct_at(cls, p, elem):
        pass

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.instances.clear()

    def __hash__(self):
        return hash(self.lookup_key)
