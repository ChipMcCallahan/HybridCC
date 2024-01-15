from abc import ABC, abstractmethod

from hybrid_cc.shared import Id


# ABC enforces that all subclasses must implement @abstractmethod methods.
class Elem(ABC):
    def __init__(self, _id):
        super().__init__()
        self._id = _id

    @property
    def id(self):
        return self._id

    @property
    def layer(self):
        return self._id.layer()