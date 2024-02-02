from dataclasses import dataclass
from typing import Tuple

from hybrid_cc.shared.color import Color


@dataclass(frozen=True)
class WinResult:
    color: Color
    position: Tuple[int, int, int]
    score: int
    tick: int


@dataclass(frozen=True)
class LoseResult:
    cause: str
    position: Tuple[int, int, int]
    tick: int
