import importlib.resources
import unittest
from pathlib import Path

from cc_tools import TWSHandler

from hybrid_cc.game.gameboard import Gameboard
from hybrid_cc.levelset.dat_conversions.dat_converter import DATConverter
from hybrid_cc.replays.replay import Replay
from hybrid_cc.shared import Direction

SET = "CCLP1"
MODE = "MS"
# MODE = "LYNX"
POSTFIX = ".dac.tws"
# POSTFIX = "-lynx.dac.tws"


class TestTWSReplays(unittest.TestCase):
    tws = {}

    def test_set(self):
        package = 'hybrid_cc.sets.dat'
        package_dir = importlib.resources.files(package)
        converted_cclp1 = DATConverter.convert_levelset(
            package_dir / f"{SET}.dat")
        passed = 0
        failed = 0

        for i, level in enumerate(converted_cclp1.levels):  # TODO: DEBUG!
            replay = self.get_replay(f"{SET}.dat", i)
            if replay:
                fname = f"{SET}-{i+1}-{level.title}-{MODE}"
                home_dir = Path.home()
                save_dir = home_dir / "hybridcc_replays"
                replay.save_to_file(save_dir, level.title, fname)
            else:
                print(f"{i + 1}, {level.title}, INVALID, 0")
                continue

            gameboard = Gameboard(level, replay.seed)
            final_tick = replay.result["tick"]
            try:
                for tick in range(1, final_tick + 2):
                    inputs = replay.get(tick)
                    gameboard.do_logic(inputs.dirs())
                    if gameboard.state == Gameboard.State.LOSE:
                        failed += 1
                        # print(f"{i + 1}, {level.title}, FAIL, {tick}")
                        break
                    elif gameboard.state == Gameboard.State.WIN:
                        passed += 1
                        print(f"{i + 1}, {level.title}, PASS, {tick}")
                        break
            except Exception as e:
                print(e)
            # self.assertEqual(gameboard.result.color.name,
            #                  replay.result['color'])
            # self.assertEqual(gameboard.result.p,
            #                  tuple(replay.result['p']))
            # self.assertEqual(gameboard.result.score,
            #                  replay.result['score'])
            # self.assertEqual(gameboard.result.tick,
            #                  replay.result['tick'])

    def get_replay(self, set_name, index):
        package = 'hybrid_cc.solutions.tws'
        package_dir = importlib.resources.files(package)
        resources = package_dir.iterdir()
        setname = str(set_name).split(".")[0]

        tws = None
        if setname in self.tws:
            tws = self.tws[setname]
        else:
            title = f"{setname}{POSTFIX}"
            for resource in resources:
                if str(resource.name) == title:
                    tws = TWSHandler(resource).decode()
                    break

        if not tws:
            return None

        tws_replay = tws.replays[index]
        replay = Replay()
        tick = 0
        for move in tws_replay.moves:
            tick = (move.tick) // 2 + 1
            if move.direction < 8:
                d_str = ["N", "W", "S", "E", "NW", "SW", "NE", "SE"][
                    move.direction]
                replay.update(tick, [Direction[d] for d in d_str])
            else:
                return None
        replay.finalize({"tick": tick})
        return replay
