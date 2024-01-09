from PIL import Image

from hybrid_cc.gfx.sprite_assembly.gfx_assembler import GfxAssembler
from hybrid_cc.shared.button_rule import ButtonRule
from hybrid_cc.shared.thief_rule import ThiefRule


class TerrainModGfx:
    def __init__(self):
        self.assembler = GfxAssembler()

    def label(self, label, color):
        # Always label SW corner for TerrainModifier layer
        return self.assembler.label_sw(label, color)

    def door(self, elem):
        base = self.assembler.custom(13)
        colored = self.assembler.colorize(base, elem.color)
        if elem.count and elem.count > 1:
            label = self.label(elem.count, elem.color)
            return self.assembler.stack(colored, label)
        return colored

    # TODO: If this is in TerrainMod, it should float over the terrain!
    def thief(self, elem):
        if elem.rule == ThiefRule.KEYS:
            return self.assembler.custom(14)
        return self.assembler.cc2("THIEF")

    def socket(self, elem):
        base = self.assembler.custom(15)
        colored = self.assembler.colorize(base, elem.color)
        if elem.count and elem.count > 1:
            label = self.label(elem.count, elem.color)
            return self.assembler.stack(colored, label)
        return colored

    def button(self, elem):
        if elem.rule == ButtonRule.TOGGLE:
            frames = [self.assembler.custom(i) for i in range(20, 22)]
            colored = [self.assembler.colorize(f, elem.color) for f in frames]
            if elem.channel:
                label = self.label(elem.channel, elem.color)
                return [self.assembler.stack(f, label) for f in colored]
            return colored
        else:
            index = ["HOLD_ALL", "HOLD_ONE", "DPAD"].index(elem.rule.name)
            base = self.assembler.custom(index + 22)
            colored = self.assembler.colorize(base, elem.color)
            if elem.channel:
                label = self.label(elem.channel, elem.color)
                return self.assembler.stack(colored, label)
            return colored
