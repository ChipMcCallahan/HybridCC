from hybrid_cc.replays.replay_input import ReplayInput


class Replay:
    def __init__(self):
        self.moves = {}  # tick: move

    def append(self, tick, inputs):
        self.moves[tick] = ReplayInput.from_inputs(inputs)

    def get(self, tick):
        while tick not in self.moves:
            if tick == 0:
                raise ValueError(f"No move found in replay for tick {tick}")
            tick -= 1
        return self.moves[tick]
