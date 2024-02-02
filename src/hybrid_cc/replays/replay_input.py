from enum import Enum

from hybrid_cc.shared import Direction


class ReplayInput(Enum):
    NONE = 0
    NW = 1
    N = 2
    NE = 3
    EN = 4
    E = 5
    ES = 6
    SE = 7
    S = 8
    SW = 9
    WS = 10
    W = 11
    WN = 12

    @property
    def directions(self):
        dirs = [None, None]
        if self != ReplayInput.NONE:
            dirs = [Direction[d] for d in self.name] + dirs
        return tuple(dirs[0:2])

    @staticmethod
    def from_inputs(inputs):
        if len(inputs) == 0 or set(inputs) == {None,}:
            return ReplayInput.NONE
        s = ""
        for d in inputs:
            s = d.name + s if d else s
        return ReplayInput[s]
