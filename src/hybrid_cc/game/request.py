from dataclasses import dataclass
from typing import Tuple, Optional, List, Type, Union

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Direction, Id
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.hashable_object import HashableObject


@dataclass
class DestroyRequest:
    src: Optional[Elem|HashableObject]
    tgt: Elem|HashableObject
    p: Tuple[int, int, int]


class CreateRequest:
    def __init__(self, *, p, id, **kwargs):
        self.p = p
        self.id = id
        self.kwargs = kwargs

    def __str__(self):
        # Filter out attributes that start with an underscore
        user_attrs = {k: v for k, v in self.__dict__.items() if
                      not k.startswith('_')}
        return f"({self.__class__.__name__}: {user_attrs})"


@dataclass
class MoveRequest:
    mob_id: int
    d: Direction
    slap: Optional[Direction] = None
    simulated_p: Optional[Tuple[int, int, int]] = None

    @staticmethod
    def from_dirs(mob_id, dirs) -> List['MoveRequest']:
        return [MoveRequest(mob_id=mob_id, d=d) for d in dirs]


@dataclass
class WinRequest:
    color: Color
    p: Tuple[int, int, int]


@dataclass
class LoseRequest:
    cause: Elem
    p: Tuple[int, int, int]


@dataclass
class ShowHintRequest:
    pass


@dataclass
class HideHintRequest:
    pass


@dataclass
class UIInteractionRequest:
    src: Elem
    tgt: Union[Elem, Type[Elem]]
    p: Tuple[int, int, int]
    type: str
