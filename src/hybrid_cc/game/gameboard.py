"""Gameboard module."""
from collections import deque, defaultdict
from enum import Enum

from hybrid_cc.game.camera import Camera
from hybrid_cc.game.elements.instances.button import Button
from hybrid_cc.game.elements.instances.chip import Chip
from hybrid_cc.game.elements.instances.socket import Socket
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.game.map import Map
from hybrid_cc.game.move_handler import MoveHandler
from hybrid_cc.game.request import DestroyRequest, CreateRequest, WinRequest, \
    LoseRequest, MoveRequest, ShowHintRequest, HideHintRequest
from hybrid_cc.game.rng import RNG
from hybrid_cc.shared import Direction
from hybrid_cc.shared.move_result import MoveResult


class Gameboard:
    """Gameboard class."""

    class State(Enum):
        PLAY = 1
        WIN = 2
        LOSE = 3

    def __init__(self, level, seed=None):
        """Initialize a new Gameboard instance."""
        self._size = level.size
        self.map = Map(level)
        self.elems = self.map.elems
        self.move_handler = MoveHandler(self.map)
        self.author = ""
        self.title = level.title
        self.time = level.time
        self.hints = {}  # map from position to string
        self.hint = level.hint  # default hint if not in dict
        self.tick = 0
        self.state = Gameboard.State.PLAY
        self.camera = Camera(Mob.instances[0], self)
        self.show_hint = False
        RNG.reset(seed)

    @property
    def size(self):
        """Returns the size of this level's x, y, z dimensions."""
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    def is_oob(self, p):
        """Returns whether the position p is out of bounds on this level."""
        x, y, z = p
        return not (0 <= x < self.size[0] and
                    0 <= y < self.size[1] and
                    0 <= z < self.size[2])

    def get(self, p):
        """Get the contents of the cell at location p."""
        if self.is_oob(p):
            raise ValueError("Coordinates out of bounds")
        return self.map.get(p)

    def do_logic(self, inputs):
        if len(inputs) > 2:
            inputs = inputs[0:2]
        inputs = [Direction[d] for d in inputs]
        moves, requests = self.elems.collect_move_plans(inputs, self.tick)
        self.do_requests(requests)

        raw_moves = deque(moves)
        moved = set()
        debug_counts = defaultdict(int)
        while len(raw_moves) > 0:
            move = raw_moves.popleft()
            mob_id, d, slap = move.mob_id, move.direction, move.slap
            mob = self.elems.get_mob(mob_id)
            if (not mob) or (mob_id in moved):
                continue
            result, requests = self.move_handler.move(mob, d, self.tick, slap,
                                                      move.simulated_position)
            if result == MoveResult.RETRY:
                raw_moves.appendleft(move)
            debug_counts[mob.mob_id] += 1
            if debug_counts[mob.mob_id] > 1000:
                raise ValueError(
                    f"Break the infinite loop! {result} {requests}")

            raw_moves.extendleft(reversed(self.do_requests(requests)))
            if result == MoveResult.PASS:
                moved.add(mob_id)

        self.tick += 1
        if self.time > 0 and self.time_remaining() == 0:
            self.transition(Gameboard.State.LOSE)
        self.camera.update()
        Button.update()  # Update all the button signals at end of turn.

    def do_requests(self, requests):
        move_requests = []
        for request in requests:
            if isinstance(request, DestroyRequest):
                target, pos = request.target, request.pos
                self.map.destruct_at(pos, target)
            elif isinstance(request, CreateRequest):
                pos, eid, kwargs = request.pos, request.id, request.kwargs
                self.map.construct_at(pos, eid, **kwargs)
            elif isinstance(request, WinRequest):
                self.transition(Gameboard.State.WIN)
            elif isinstance(request, LoseRequest):
                self.transition(Gameboard.State.LOSE)
            elif isinstance(request, MoveRequest):
                move_requests.append(request)
            elif isinstance(request, ShowHintRequest):
                self.show_hint = True
            elif isinstance(request, HideHintRequest):
                self.show_hint = False
        return move_requests

    def transition(self, state):
        if self.state == Gameboard.State.PLAY:
            self.state = state

    def time_remaining(self):
        return max(self.time - self.tick // 10, 0)

    @staticmethod
    def chips_remaining():
        chips_remaining = {}
        for color, required in Socket.chips_required.items():
            collected = Chip.chips_collected.get(color, 0)
            remaining = max(0, required - collected)
            chips_remaining[color] = remaining
        return chips_remaining
