from dataclasses import dataclass
from typing import Tuple

from hybrid_cc.shared.color import Color


@dataclass(frozen=True)
class WinResult:
    color: Color
    p: Tuple[int, int, int]
    score: int
    tick: int


@dataclass(frozen=True)
class LoseResult:
    cause: str
    p: Tuple[int, int, int]
    tick: int
