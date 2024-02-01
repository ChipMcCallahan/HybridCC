import logging
from collections import defaultdict

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.elements.instances.button import Button
from hybrid_cc.game.request import MoveRequest
from hybrid_cc.shared import Direction
from hybrid_cc.shared.kwargs import COLOR, RULE, CHANNEL
from hybrid_cc.shared.move_result import MoveResult


class Trap(Elem):
    kwarg_filter = (COLOR, RULE, CHANNEL)  # Retain these kwargs only.
    mobs = defaultdict(lambda: None)  # position to mob
    last_signals = defaultdict(int)  # (color, channel) to int
    positions = defaultdict(list)  # (color, channel, rule) to [position]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.mobs.clear()
        cls.last_signals.clear()
        cls.positions.clear()

    @classmethod
    def construct_at(cls, pos, **kwargs):
        elem = super().construct_at(pos, **kwargs)
        key = (elem.color, elem.channel, elem.rule)
        cls.positions[key].append(pos)
        return elem

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------
    # noinspection PyUnresolvedReferences
    @classmethod
    def do_class_planning(cls, **kwargs):
        to_remove = []
        requests = []
        for key, positions in cls.positions.items():
            color, channel, rule = key
            signal = Button.signal[(color, channel)]
            last_signal = cls.last_signals[(color, channel)]

            cls.last_signals[(color, channel)] = signal
            can_exit = (rule.value + signal % 2) % 2 == 1
            if not can_exit or signal <= last_signal:
                continue

            dpad_direction, dpad_signal = Button.dpad_signal[
                (color, channel)]
            direction = None
            if dpad_signal and dpad_signal > last_signal:
                direction = dpad_direction
            for p in positions:
                mob = cls.mobs.get(p, None)
                if not mob:
                    continue
                if not mob.exists():
                    to_remove.append(p)
                    continue
                if direction and direction.is_cardinal():
                    mob.direction = direction
                requests.append(
                    MoveRequest(mob_id=mob.mob_id,
                                direction=mob.direction))
        for p in to_remove:
            cls.mobs.pop(p, None)
        return requests, []

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    def test_exit(self, mob, position, direction):
        key = (self.color, self.channel)
        signal = Button.signal[key]
        if (self.rule.value + signal % 2) % 2 == 1:
            return MoveResult.PASS, []
        return MoveResult.FAIL, []

    def finish_enter(self, mob, position, direction):
        self.mobs[position] = mob

    def finish_exit(self, mob, position, direction):
        self.mobs[position] = None

    # --------------------------------------------------------------------------
    # OTHER
    # --------------------------------------------------------------------------
    def construct_mob_here(self, mob, position):
        self.finish_enter(mob, position, mob.direction)
