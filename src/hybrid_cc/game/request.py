from dataclasses import dataclass, field
from typing import Tuple, Optional, List

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Direction
from hybrid_cc.shared.color import Color


@dataclass
class DestroyRequest:
    target: Elem
    pos: Tuple[int, int, int]


class CreateRequest:
    def __init__(self, *, pos, id, **kwargs):
        self.pos = pos
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
    direction: Direction
    slap: Optional[Direction] = None
    simulated_position: Optional[Tuple[int, int, int]] = None

    @staticmethod
    def from_directions(mob_id, directions) -> List['MoveRequest']:
        return [MoveRequest(mob_id=mob_id, direction=d) for d in directions]


@dataclass
class WinRequest:
    color: Color
    pos: Tuple[int, int, int]


@dataclass
class LoseRequest:
    cause: Elem
    pos: Tuple[int, int, int]


@dataclass
class ShowHintRequest:
    pass


@dataclass
class HideHintRequest:
    pass
