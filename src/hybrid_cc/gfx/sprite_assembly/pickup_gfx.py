from PIL import Image

from hybrid_cc.gfx.sprite_assembly.gfx_assembler import GfxAssembler
from hybrid_cc.shared.key_rule import KeyRule


class PickupGfx:
    def __init__(self):
        self.assembler = GfxAssembler()

    def label(self, label, color):
        # Always label NE corner for Pickup layer
        return self.assembler.label_ne(label, color)

    def bomb(self, elem):
        base = self.assembler.custom(16)
        return self.assembler.colorize(base, elem.color)

    def key(self, elem):
        index = {
            KeyRule.DEFAULT: 17,
            KeyRule.FRAGILE: 18,
            KeyRule.ACTING_DIRT: 19,
        }[elem.rule]
        base = self.assembler.custom(index)
        colored = self.assembler.colorize(base, elem.color)
        if elem.count and elem.count > 1:
            label = self.label(elem.count, elem.color)
            return self.assembler.stack(colored, label)
        return colored

    def tool(self, elem):
        name = ["FLIPPERS", "FIRE_BOOTS", "SKATES", "SUCTION_BOOTS"][
            elem.rule.value - 1]
        base = self.assembler.cc2(name)
        if elem.count and elem.count > 1:
            label = self.label(elem.count, elem.color)
            return self.assembler.stack(base, label)
        return base
