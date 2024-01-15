from abc import ABC, abstractmethod


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

    @abstractmethod
    def construct_at(self, pos, **kwargs):
        pass

    @abstractmethod
    def destruct_at(self, pos, **kwargs):
        pass

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # UTILITIES
    # --------------------------------------------------------------------------
    @staticmethod
    def filtered_kwargs(_filter, **kwargs):
        return {k: v for k, v in kwargs.items() if k in _filter}
