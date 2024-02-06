import importlib.resources
import logging
import unittest
from pathlib import Path

from cc_tools import TWSHandler

from hybrid_cc.game.gameboard import Gameboard
from hybrid_cc.levelset.dat_conversions.dat_converter import DATConverter
from hybrid_cc.replays.replay import Replay
from hybrid_cc.shared import Direction


# MODE = "MS"
# mode = "LYNX"
# POSTFIX = ".dac.json"
# postfix = "-lynx.dac.json"


class TestTWSReplays(unittest.TestCase):
    tws = {}

    def test_cclp1_ms(self):
        self.do_set("CCLP1", "MS", ".dac.json")

    def test_cclp1_lynx(self):
        self.do_set("CCLP1", "LYNX", "-lynx.dac.json")

    def test_cclxp2_ms(self):
        self.do_set("CCLXP2", "MS", ".dac.json")

    def test_cclp3_ms(self):
        self.do_set("CCLP3", "MS", ".dac.json")

    def test_cclp3_lynx(self):
        self.do_set("CCLP3", "LYNX", "-lynx.dac.json")

    def test_cclp4_ms(self):
        self.do_set("CCLP4", "MS", ".dac.json")

    def test_cclp4_lynx(self):
        self.do_set("CCLP4", "LYNX", "-lynx.dac.json")

    def do_set(self, set_name, mode, postfix):
        package = 'hybrid_cc.sets.dat'
        package_dir = importlib.resources.files(package)
        converted_cclp = DATConverter.convert_levelset(
            package_dir / f"{set_name}.dat")

        passed = 0
        failed = 0
        results = {}
        for i, level in enumerate(converted_cclp.levels):
            replay = self.get_replay(f"{set_name}.dat", i, postfix)
            key = (i + 1, level.title)

            if not replay:
                results[key] = ("INVALID", 0, 0)
                continue

            gameboard = Gameboard(level, replay.seed)
            final_tick = replay.result["tick"]
            try:
                for tick in range(1, final_tick + 2):
                    inputs = replay.get(tick)
                    gameboard.do_logic(inputs.dirs())
                    if gameboard.state == Gameboard.State.LOSE:
                        failed += 1
                        results[key] = ("LOSE", gameboard.tick, final_tick)
                        break
                    elif gameboard.state == Gameboard.State.WIN:
                        passed += 1
                        results[key] = ("WIN", gameboard.tick, final_tick)
                        break
                if key not in results:
                    results[key] = ("TIME", gameboard.tick, final_tick)
            except ValueError as e:
                if not str(e).startswith("Break the infinite loop!"):
                    raise AssertionError(
                        f"Unexpected error: '{str(e)}'")
                results[key] = ("INFINITE_LOOP", 0, 0)

            fname = f"{set_name}-{i + 1}-{level.title}-{mode}"
            if results[key][0] != "WIN":
                fname += f"-{results[key][0]}"
            home_dir = Path.home()
            save_dir = home_dir / "hybridcc_replays"
            replay.save_to_file(save_dir, level.title, fname)

        for k, v in results.items():
            print(f"{k[0]}, {k[1]}, {v[0]}, {v[1]}/{v[2]}")

    def get_replay(self, set_name, index, postfix):
        package = 'hybrid_cc.solutions.tws'
        package_dir = importlib.resources.files(package)
        setname = str(set_name).split(".")[0]

        def load_and_map_numbers_to_moves(file_path):
            import json

            with open(file_path, 'r') as file:
                data = json.load(file)
            number_to_moves = {}
            for item in data['solutions']:
                number = item.get('number')
                moves = item.get('moves')
                if number is not None and moves is not None:
                    number_to_moves[number] = moves
            return number_to_moves

        result = None
        if setname in self.tws:
            result = self.tws[setname]
        else:
            title = f"{setname}{postfix}"
            result = load_and_map_numbers_to_moves(package_dir / title)
            self.tws[setname] = result

        if not result or index + 1 not in result:
            return None

        json_moves = list(result[index + 1])

        try:
            return JsonInputParser.parse(json_moves)
        except ValueError as e:
            print(e)
            return None


class JsonInputParser:
    multiplier = {'L': 2, 'R': 2, 'U': 2, 'D': 2, '.': 2,
                  'l': 1, 'r': 1, 'u': 1, 'd': 1, ',': 1}
    dirs = {'L': 'W', 'R': 'E', 'D': 'S', 'U': 'N'}

    @classmethod
    def parse(cls, chars):
        # https://github.com/magical/tws2json/blob/master/format.txt
        replay = Replay()
        tick = 1

        while len(chars) > 0:
            frames = 1
            i = 0
            for i, c in enumerate(chars):
                if not c.isdigit():
                    if i > 0:
                        frames = int(''.join(chars[:i]))
                    break
            chars = chars[i:]
            d1, d2 = chars.pop(0), None
            if d1 == "*":
                raise ValueError("Mouse move handling is not implemented.")

            if len(chars) > 0 and chars[0] == "+":
                _, d2 = chars.pop(0), chars.pop(0)

            frames *= cls.multiplier[d1]

            d1 = cls.dirs.get(d1.upper(), None)
            d2 = cls.dirs.get(d2.upper(), None) if d2 else None
            d1 = Direction[d1] if d1 else None
            d2 = Direction[d2] if d2 else None
            replay.update(tick, [d1, d2])
            tick += frames
        replay.finalize({"tick": tick})
        return replay
