import importlib.resources
import unittest

from hybrid_cc.game.gameboard import Gameboard
from hybrid_cc.levelset.dat_conversions.dat_converter import DATConverter
from hybrid_cc.replays.replay import Replay


class TestCCLPReplays(unittest.TestCase):
    def test_cclp1(self):
        self.do_cclp("CCLP1.dat")

    def test_cclxp2(self):
        self.do_cclp("CCLXP2.dat")

    def test_cclp3(self):
        self.do_cclp("CCLP3.dat")

    def test_cclp4(self):
        self.do_cclp("CCLP4.dat")

    def do_cclp(self, set_name):
        package = 'hybrid_cc.sets.dat'
        package_dir = importlib.resources.files(package)
        converted_cclp1 = DATConverter.convert_levelset(
            package_dir / set_name)
        results = {}
        failures = False
        for i, level in enumerate(converted_cclp1.levels):
            replay = self.get_replay(set_name, i, level)
            if not replay:
                print(
                    f"--> Skipping level {i + 1} ({level.title}) due to no replay.")
                continue
            gameboard = Gameboard(level, replay.seed)
            final_tick = replay.result["tick"]
            try:
                for tick in range(1, final_tick + 2):
                    inputs = replay.get(tick)
                    gameboard.do_logic(inputs.dirs())
            except Exception as e:
                failures = True
                print(level.title, e)

            result = []
            if (not gameboard.result) or (
                    not hasattr(gameboard.result, 'color')):
                result = [False, False, False, False]
            else:
                result.append(
                    gameboard.result.color.name == replay.result['color'])
                result.append(gameboard.result.p == tuple(replay.result['p']))
                result.append(gameboard.result.score == replay.result['score'])
                result.append(gameboard.result.tick == replay.result['tick'])
            results[(i, level.title)] = result
            print((i+1, level.title), result)
        for _, v in results.items():
            self.assertFalse(False in v)
        self.assertFalse(failures)

    def get_replay(self, set_name, index, level):
        package = 'hybrid_cc.solutions.official'
        package_dir = importlib.resources.files(package)
        resources = package_dir.iterdir()
        setname = str(set_name).split(".")[0]
        title = f"{setname}-{index + 1}-{level.title}"
        title = Replay.sanitize_filename(title) + ".json"
        for resource in resources:
            if str(resource.name) == title:
                return Replay.load_from_file(resource)
        return None
