import logging
from collections import defaultdict

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared.button_rule import ButtonRule
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.kwargs import COLOR, RULE, CHANNEL
from hybrid_cc.shared.tag import SLIDING


class Button(Elem):
    kwarg_filter = (COLOR, RULE, CHANNEL)  # Retain these kwargs only.
    deferred_signals = set()  # we don't want to update the signal until next turn

    # we need to defer this 1-2 ticks depending on mob speed.

    signal = defaultdict(int)
    hold_one_counts = defaultdict(int)
    hold_all_counts = defaultdict(int)
    dpad_signal = defaultdict(lambda: (None, 0))

    class DeferredSignal:
        def __init__(self, color, channel, *, defer=0, direction=None):
            self.color = color
            self.channel = channel
            self.direction = direction
            self.defer = defer

        @property
        def key(self):
            return self.color, self.channel

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.signal.clear()
        cls.hold_all_counts.clear()
        cls.hold_one_counts.clear()
        cls.dpad_signal.clear()
        cls.deferred_signals.clear()

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

    @classmethod
    def update(cls, **kwargs):
        to_remove = []
        for pending in cls.deferred_signals:
            if pending.defer == 0:
                cls.signal[pending.key] += 1
                if pending.direction:
                    cls.dpad_signal[pending.key] = (
                        pending.direction, cls.signal[pending.key])
                to_remove.append(pending)
            else:
                pending.defer -= 1
        for signal in to_remove:
            cls.deferred_signals.remove(signal)

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def finish_exit(self, mob, position, direction):
        key = (self.color, self.channel)
        if self.rule == ButtonRule.HOLD_ONE:
            self.hold_one_counts[key] -= 1
            if self.hold_one_counts[key] == 0:
                self.activate(mob)
        elif self.rule == ButtonRule.HOLD_ALL:
            # HOLD_ALL buttons can only be held by colored blocks or tanks!
            if self.color not in (Color.GREY, mob.color):
                return
            if self.hold_all_counts[key] == 0:
                self.activate(mob)
            self.hold_all_counts[key] += 1

    def finish_enter(self, mob, position, direction):
        key = (self.color, self.channel)
        if self.rule == ButtonRule.TOGGLE:
            self.activate(mob)
        elif self.rule == ButtonRule.HOLD_ONE:
            if self.hold_one_counts[key] == 0:
                self.activate(mob)
            self.hold_one_counts[key] += 1
        elif self.rule == ButtonRule.HOLD_ALL:
            # HOLD_ALL buttons can only be held by colored blocks or tanks!
            if self.color not in (Color.GREY, mob.color):
                return
            self.hold_all_counts[key] -= 1
            if self.hold_all_counts[key] == 0:
                self.activate(mob)
        elif self.rule == ButtonRule.DPAD:
            self.activate(mob, direction)

    def activate(self, mob, direction=None):
        kwargs = {
            "defer": 0 if mob.tagged(SLIDING) else 1
        }
        if direction and direction.is_cardinal():
            kwargs["direction"] = direction
        signal = self.DeferredSignal(self.color, self.channel, **kwargs)
        self.deferred_signals.add(signal)

    # --------------------------------------------------------------------------
    # OTHER
    # --------------------------------------------------------------------------
    def construct_mob_here(self, mob, position):
        if self.rule in (ButtonRule.HOLD_ONE, ButtonRule.HOLD_ALL):
            self.finish_enter(mob, position, mob.direction)