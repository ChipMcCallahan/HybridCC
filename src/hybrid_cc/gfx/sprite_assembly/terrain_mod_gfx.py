from hybrid_cc.gfx.sprite_assembly.gfx_assembler import GfxAssembler
from hybrid_cc.shared.button_rule import ButtonRule
from hybrid_cc.shared.toggle_wall_rule import ToggleWallRule

CURRENT_STATE = "current_state"


class TerrainModGfx:
    def __init__(self):
        self.assembler = GfxAssembler()

    def label(self, label, color):
        # Always label SW corner for TerrainModifier layer
        return self.assembler.label_sw(label, color)

    def door(self, elem, **kwargs):
        base = self.assembler.custom(13)
        colored = self.assembler.colorize(base, elem.color)
        if elem.count and elem.count > 1:
            label = self.label(elem.count, elem.color)
            return self.assembler.stack(colored, label)
        return colored

    def socket(self, elem, **kwargs):
        base = self.assembler.custom(15)
        colored = self.assembler.colorize(base, elem.color)
        if elem.count and elem.count > 1:
            label = self.label(elem.count, elem.color)
            return self.assembler.stack(colored, label)
        return colored

    def button(self, elem, **kwargs):
        if elem.rule == ButtonRule.TOGGLE:
            current_state = kwargs.get(CURRENT_STATE, 0)
            base = self.assembler.custom(21 - current_state)
            colored = self.assembler.colorize(base, elem.color)
            if elem.channel:
                label = self.label(elem.channel, elem.color)
                return self.assembler.stack(colored, label)
            return colored
        else:
            index = ["HOLD_ALL", "HOLD_ONE", "DPAD"].index(elem.rule.name)
            base = self.assembler.custom(index + 22)
            colored = self.assembler.colorize(base, elem.color)
            if elem.channel:
                label = self.label(elem.channel, elem.color)
                return self.assembler.stack(colored, label)
            return colored

    def toggle_wall(self, elem, **kwargs):
        current_state = kwargs.get(CURRENT_STATE, 0)
        index = [ToggleWallRule.STARTS_OPEN, ToggleWallRule.STARTS_SHUT].index(
            elem.rule)
        is_wall = (index + current_state) % 2 != 0
        base = [self.assembler.custom(i) for i in range(25, 29)]
        if is_wall:
            base = [self.assembler.stack(frame, self.assembler.custom(29)) for
                    frame in base]

        colored = [self.assembler.colorize(frame, elem.color) for frame in base]
        if elem.channel:
            label = self.label(elem.channel, elem.color)
            return [self.assembler.stack(frame, label) for frame in colored]
        return colored
