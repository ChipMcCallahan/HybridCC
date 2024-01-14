from PIL import Image

from hybrid_cc.gfx.sprite_assembly.gfx_assembler import GfxAssembler
from hybrid_cc.shared.space_rule import SpaceRule
from hybrid_cc.shared.stepping_stone_rule import SteppingStoneRule
from hybrid_cc.shared.thief_rule import ThiefRule
from hybrid_cc.shared.trap_rule import TrapRule
from hybrid_cc.shared.trick_wall_rule import TrickWallRule

CURRENT_STATE = "current_state"


class TerrainGfx:
    def __init__(self):
        self.assembler = GfxAssembler()

    def label(self, label, color):
        # Always label SE corner for Terrain layer
        return self.assembler.label_se(label, color)

    def space(self, elem, **kwargs):
        rule = elem.rule or SpaceRule.DEFAULT
        if rule == SpaceRule.DEFAULT:
            return Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        index = [SpaceRule.SOLID_BELOW, SpaceRule.MAYBE_SOLID_BELOW,
                 SpaceRule.DEADLY_BELOW].index(rule)
        return self.assembler.custom(index + 40)

    def floor(self, elem, **kwargs):
        base = self.assembler.cc2("FLOOR")
        return self.assembler.colorize(base, elem.color)

    def wall(self, elem, **kwargs):
        base = self.assembler.cc2("WALL")
        return self.assembler.colorize(base, elem.color)

    def exit(self, elem, **kwargs):
        base = self.assembler.cc2_series("EXIT", 4)
        return [self.assembler.colorize(frame, elem.color) for frame in base]

    def water(self, elem, **kwargs):
        return self.assembler.cc2_series("WATER", 4)

    def fire(self, elem, **kwargs):
        return self.assembler.cc2_series("FIRE", 4)

    def trick_wall(self, elem, **kwargs):
        rule = elem.rule
        if not kwargs.get("show_secrets"):
            if rule in (TrickWallRule.PERMANENTLY_INVISIBLE,
                        TrickWallRule.INVISIBLE_BECOMES_WALL):
                return self.floor(elem, **kwargs)
            rule = TrickWallRule.BECOMES_WALL
        index = [
            TrickWallRule.BECOMES_FLOOR,
            TrickWallRule.BECOMES_WALL,
            TrickWallRule.PASS_THRU,
            TrickWallRule.SOLID,
            TrickWallRule.PERMANENTLY_INVISIBLE,
            TrickWallRule.INVISIBLE_BECOMES_WALL
        ].index(rule)
        base = self.assembler.custom(index)
        return self.assembler.colorize(base, elem.color)

    def dirt(self, elem, **kwargs):
        base = self.assembler.custom(10)
        return self.assembler.colorize(base, elem.color)

    def ice(self, elem, **kwargs):
        return self.assembler.cc2("ICE")

    def force(self, elem, **kwargs):
        if elem.direction:
            base = self.assembler.cc2(f"FORCE_N")
            frames = [self.assembler.cc2(f"FORCE_{elem.direction.name}")]
            for i in range(1, 8):
                top_height = 32 * i // 8  # Height of the top part
                bottom_height = 32 - top_height  # Height of the bottom part

                # Split the image
                top_part = base.crop((0, 0, 32, top_height))
                bottom_part = base.crop(
                    (0, top_height, 32, 32))

                # Create a new image and paste the parts in swapped positions
                new_frame = Image.new('RGBA', (32, 32))
                new_frame.paste(bottom_part, (0, 0))
                new_frame.paste(top_part, (0, bottom_height))
                if elem.direction.name in "WSE":
                    amt = "NWSE".index(elem.direction.name) * 90
                    new_frame = new_frame.rotate(amt)
                frames.append(new_frame)
        else:
            frames = self.assembler.cc2_series(f"FORCE_RANDOM", 8)
        return [self.assembler.colorize(frame, elem.color) for frame in frames]

    def teleport(self, elem, **kwargs):
        floor = self.floor(elem, **kwargs)
        frames = [self.assembler.custom(i) for i in range(6, 10)]
        colored = [self.assembler.colorize(frame, elem.color) for frame in
                   frames]
        return [self.assembler.stack(floor, frame) for frame in colored]

    def trap(self, elem, **kwargs):
        current_state = kwargs.get(CURRENT_STATE, 0)
        index = [TrapRule.DEFAULT, TrapRule.STARTS_SHUT].index(
            elem.rule or TrapRule.DEFAULT)
        name = ["TRAP", "TRAP_SHUT"][(index + current_state) % 2]
        base = self.assembler.cc2(name)
        colored = self.assembler.colorize(base, elem.color)
        if elem.channel:
            label = self.label(elem.channel, elem.color)
            return self.assembler.stack(colored, label)
        return colored

    def thief(self, elem, **kwargs):
        if elem.rule == ThiefRule.KEYS:
            return self.assembler.cc2("KEY_THIEF")
        return self.assembler.cc2("THIEF")

    def gravel(self, elem, **kwargs):
        return self.assembler.custom(11)

    def pop_up_wall(self, elem, **kwargs):
        base = self.assembler.cc2("POP_UP_WALL")
        colored = self.assembler.colorize(base, elem.color)
        if elem.count and elem.count > 1:
            label = self.label(elem.count, elem.color)
            return self.assembler.stack(colored, label)
        return colored

    def stepping_stone(self, elem, **kwargs):
        top = self.assembler.custom(12)
        bottom = self.fire(
            elem) if elem.rule == SteppingStoneRule.FIRE else self.water(elem)
        combined = []
        for frame in bottom:
            combined.append(self.assembler.stack(frame, top))
        if elem.count and elem.count > 1:
            label = self.label(elem.count, elem.color)
            return [self.assembler.stack(frame, label) for frame in combined]
        return combined

    def hint(self, elem, **kwargs):
        return self.assembler.cc2("HINT")

    def cloner(self, elem, **kwargs):
        cloner = self.assembler.cc2("CLONER")
        d = elem.direction
        colored = self.assembler.colorize(cloner, elem.color)
        if d:
            arrow = self.assembler.cc2(f"CLONER_ARROW_{d.name}")
            colored.paste(arrow, (0, 0), arrow)
        if elem.channel:
            label = self.label(elem.channel, elem.color)
            return self.assembler.stack(colored, label)
        return colored
