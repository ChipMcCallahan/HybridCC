import importlib.resources
import unittest

from hybrid_cc.game.gameboard import Gameboard
from hybrid_cc.game.rng import RNG
from hybrid_cc.levelset.dat_conversions.dat_converter import DATConverter
from hybrid_cc.replays.replay import Replay


class TestGameboard(unittest.TestCase):
    def test_cclp1(self):
        package = 'hybrid_cc.sets.dat'
        package_dir = importlib.resources.files(package)
        set_name = "CCLP1.dat"
        converted_cclp1 = DATConverter.convert_levelset(
            package_dir / set_name)
        for i, level in enumerate(converted_cclp1.levels):
            replay = self.get_replay(set_name, i, level)
            if replay:
                print(f"Replaying level {i + 1} ({level.title}).")
            else:
                print(
                    f"Skipping level {i + 1} ({level.title}) due to no replay.")
                continue
            gameboard = Gameboard(level, replay.seed)
            final_tick = replay.result["tick"]
            for tick in range(1, final_tick + 2):
                inputs = replay.get(tick)
                gameboard.do_logic(inputs.dirs())
            self.assertEqual(gameboard.result.color.name,
                             replay.result['color'])
            self.assertEqual(gameboard.result.p,
                             tuple(replay.result['p']))
            self.assertEqual(gameboard.result.score,
                             replay.result['score'])
            self.assertEqual(gameboard.result.tick,
                             replay.result['tick'])

    def get_replay(self, set_name, index, level):
        package = 'hybrid_cc.json.official_replays'
        package_dir = importlib.resources.files(package)
        resources = package_dir.iterdir()
        setname = str(set_name).split(".")[0]
        title = f"{setname}-{index + 1}-{level.title}.json"
        for resource in resources:
            if str(resource.name) == title:
                return Replay.load_from_file(resource)
        return None
