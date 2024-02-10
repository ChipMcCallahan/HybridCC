from hybrid_cc.gfx.sprite_assembly.gfx_assembler import GfxAssembler
from hybrid_cc.shared.bomb_rule import BombRule
from hybrid_cc.shared.key_rule import KeyRule
from hybrid_cc.shared.tool_rule import ToolRule

CURRENT_STATE = "current_state"


class PickupGfx:
    def __init__(self):
        self.assembler = GfxAssembler()

    def label(self, label, color, **kwargs):
        # Always label NE corner for Pickup layer
        return self.assembler.label_ne(label, color)

    def bomb(self, elem, **kwargs):
        current_state = kwargs.get(CURRENT_STATE, 0)
        index = [BombRule.STARTS_ARMED, BombRule.STARTS_DISARMED].index(
            elem.rule)
        is_armed = (index + current_state) % 2 == 0
        base = self.assembler.custom(16 if is_armed else 48)
        colored = self.assembler.colorize(base, elem.color)
        if elem.channel:
            label = self.label(elem.channel, elem.color)
            return self.assembler.stack(colored, label)
        return colored

    def chip(self, elem, **kwargs):
        base = self.assembler.custom(14)
        colored = self.assembler.colorize(base, elem.color)
        if elem.count and elem.count != 1:
            label = self.label(elem.count, elem.color)
            return self.assembler.stack(colored, label)
        return colored

    def key(self, elem, **kwargs):
        index = {
            KeyRule.DEFAULT: 17,
            KeyRule.FRAGILE: 18,
            KeyRule.ACTING_DIRT: 19,
        }[elem.rule or KeyRule.DEFAULT]
        base = self.assembler.custom(index)
        colored = self.assembler.colorize(base, elem.color)
        if elem.count and elem.count != 1:
            label = self.label(elem.count, elem.color)
            return self.assembler.stack(colored, label)
        return colored

    def tool(self, elem, **kwargs):
        name = elem.id.name
        base = self.assembler.cc2(name)
        rule = elem.rule
        if rule == ToolRule.ITEM_BARRIER:
            barrier = self.assembler.cc2("NOT_ALLOWED_MARKER")
            return self.assembler.stack(base, barrier)
        if elem.count and elem.count != 1:
            label = self.label(elem.count, "white")
            return self.assembler.stack(base, label)
        return base

    def flippers(self, elem, **kwargs):
        return self.tool(elem, **kwargs)

    def fire_boots(self, elem, **kwargs):
        return self.tool(elem, **kwargs)

    def skates(self, elem, **kwargs):
        return self.tool(elem, **kwargs)

    def suction_boots(self, elem, **kwargs):
        return self.tool(elem, **kwargs)
