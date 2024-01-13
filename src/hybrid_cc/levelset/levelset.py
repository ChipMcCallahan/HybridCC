from cc_tools import DATHandler

from hybrid_cc.levelset.level import Level


class Levelset:
    def __init__(self, name="Untitled Levelset"):
        self.name = name
        self.levels = []
