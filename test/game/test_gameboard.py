import importlib.resources
import unittest

from hybrid_cc.game.gameboard import Gameboard
from hybrid_cc.levelset.dat_conversions.dat_converter import DATConverter


class TestGameboard(unittest.TestCase):
    def test_cclp1(self):
        self.package = 'hybrid_cc.sets.dat'
        self.package_dir = importlib.resources.files(self.package)
        converted_cclp1 = DATConverter.convert_levelset(
            self.package_dir / "CCLP1.dat")
        for level in converted_cclp1.levels:
            Gameboard(level)
