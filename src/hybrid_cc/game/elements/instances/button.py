import logging
from collections import defaultdict

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared.button_rule import ButtonRule
from hybrid_cc.shared.kwargs import COLOR, RULE, CHANNEL


class Button(Elem):
    kwarg_filter = (COLOR, RULE, CHANNEL)  # Retain these kwargs only.
    state = defaultdict(int)
    hold_one_counts = defaultdict(int)
    hold_all_counts = defaultdict(int)
    dpad_directions = defaultdict(lambda: (None, None))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.state.clear()

    @classmethod
    def construct_at(cls, pos, **kwargs):
        elem = super().construct_at(pos, **kwargs)
        rule = kwargs[RULE]
        if rule == ButtonRule.HOLD_ALL:
            color, channel = kwargs[COLOR], kwargs[CHANNEL]
            cls.hold_all_counts[(color, channel)] += 1
        return elem

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def finish_exit(self, mob, position, direction):
        key = (self.color, self.channel)
        if self.rule == ButtonRule.HOLD_ONE:
            self.hold_one_counts[key] -= 1
            if self.hold_one_counts[key] == 0:
                self.activate()
        elif self.rule == ButtonRule.HOLD_ALL:
            if self.hold_all_counts[key] == 0:
                self.activate()
            self.hold_all_counts[key] += 1

    def finish_enter(self, mob, position, direction):
        key = (self.color, self.channel)
        if self.rule == ButtonRule.TOGGLE:
            self.activate()
        elif self.rule == ButtonRule.HOLD_ONE:
            if self.hold_one_counts[key] == 0:
                self.activate()
            self.hold_one_counts[key] += 1
        elif self.rule == ButtonRule.HOLD_ALL:
            self.hold_all_counts[key] -= 1
            if self.hold_all_counts[key] == 0:
                self.activate()
        elif self.rule == ButtonRule.DPAD:
            self.activate()  # DPAD acts as a global toggle
            signal = self.state[key]
            # noinspection PyTypeChecker
            self.dpad_directions[key] = (direction, signal)

    def activate(self):
        self.state[(self.color, self.channel)] += 1
