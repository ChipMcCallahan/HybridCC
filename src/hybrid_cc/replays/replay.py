from hybrid_cc.replays.replay_input import ReplayInput


class Replay:
    def __init__(self, seed=0):
        self.moves = {}  # tick: move
        self.seed = seed
        self.last_tick = None
        self.result = None

    def update(self, tick, inputs):
        if self.result:
            raise ValueError(
                f"Replay has result {self.result}, cannot update.")
        curr_input = ReplayInput.from_inputs(inputs)
        last_input = self.moves.get(self.last_tick, None)
        if curr_input != last_input:
            self.moves[tick] = curr_input
            self.last_tick = tick

    def get(self, tick):
        while tick not in self.moves:
            if tick == 0:
                raise ValueError(f"No move found in replay for tick {tick}")
            tick -= 1
        return self.moves[tick]

    def finalize(self, result):
        self.result = result
