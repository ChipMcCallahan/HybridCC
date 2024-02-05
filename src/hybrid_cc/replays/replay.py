import json
import re
from dataclasses import asdict
from datetime import datetime
from enum import Enum

from hybrid_cc.replays.replay_input import ReplayInput
from hybrid_cc.shared.game_result import WinResult, LoseResult


class Replay:
    def __init__(self, seed=0):
        self.moves = {}  # tick: move
        self.seed = seed
        self.last_tick = None
        self.result = None

    def update(self, tick, inputs):
        if self.result:
            return
        curr_input = ReplayInput.from_inputs(inputs)
        last_input = self.moves.get(self.last_tick, None)
        if curr_input != last_input:
            self.moves[tick] = curr_input
            self.last_tick = tick

    def get(self, tick):
        t = tick
        while t not in self.moves:
            if t < 0:
                return ReplayInput.NONE
            t -= 1
        return self.moves[t]

    def finalize(self, result):
        self.result = result

    def to_json(self):
        # Convert the moves dict to a format that can be JSON serialized
        moves_json = {str(tick): move.name for tick, move in self.moves.items()}
        return json.dumps({
            'seed': self.seed,
            'moves': moves_json,
            'last_tick': self.last_tick,
            'result': self.result
        }, default=self.serialize_to_json)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        replay = cls(seed=data['seed'])
        replay.moves = {int(tick): ReplayInput.from_name(move) for tick, move in
                        data['moves'].items()}
        replay.last_tick = data['last_tick']
        replay.result = data['result']
        return replay

    def save_to_file(self, directory, level_title, name=None):
        json_str = self.to_json()
        now = datetime.now()
        timestamp_str = now.strftime("%y%m%d-%H%M%S")
        result = "UNFINISHED"
        if isinstance(self.result, WinResult):
            result = "WIN"
        elif isinstance(self.result, LoseResult):
            result = "LOSE"
        filename = name or f"{timestamp_str}-[{level_title}]-[{result}]"
        filename = self.sanitize_filename(filename) + ".json"
        with open(directory / filename, 'w') as f:
            f.write(json_str)
        return directory / filename

    @staticmethod
    def load_from_file(file_path):
        with open(file_path, 'r') as f:
            json_str = f.read()
        return Replay.from_json(json_str)

    @staticmethod
    def serialize_to_json(obj):
        """Serialize objects to JSON, including custom objects."""
        if isinstance(obj, Enum):
            return obj.name  # Convert Enum to its name for serialization
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        if hasattr(obj, "_asdict"):  # Specifically for dataclasses
            return asdict(obj)
        raise TypeError(
            f"Object of type {type(obj).__name__} is not JSON serializable")

    @staticmethod
    def sanitize_filename(filename):
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "")
        filename = filename.strip().rstrip(".")
        filename = re.sub(r'[^\w\s-]', '', filename)
        return filename
