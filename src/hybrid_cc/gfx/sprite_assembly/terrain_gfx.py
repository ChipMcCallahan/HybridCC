from PIL import Image

from hybrid_cc.gfx.sprite_assembly.gfx_assembler import GfxAssembler
from hybrid_cc.shared.trap_rule import TrapRule
from hybrid_cc.shared.trick_wall_rule import TrickWallRule


class TerrainGfx:
    def __init__(self):
        self.assembler = GfxAssembler()

    def label(self, label, color):
        # Always label SE corner for Terrain layer
        return self.assembler.label_se(label, color)

    def floor(self, elem):
        base = self.assembler.cc2("FLOOR")
        return self.assembler.colorize(base, elem.color)

    def wall(self, elem):
        base = self.assembler.cc2("WALL")
        return self.assembler.colorize(base, elem.color)

    def exit(self, elem):
        base = self.assembler.cc2_series("EXIT", 4)
        return [self.assembler.colorize(frame, elem.color) for frame in base]

    def water(self, elem):
        return self.assembler.cc2_series("WATER", 4)

    def fire(self, elem):
        return self.assembler.cc2_series("FIRE", 4)

    def trick_wall(self, elem):
        index = [
            TrickWallRule.BECOMES_FLOOR,
            TrickWallRule.BECOMES_WALL,
            TrickWallRule.PASS_THRU,
            TrickWallRule.SOLID,
            TrickWallRule.PERMANENTLY_INVISIBLE,
            TrickWallRule.INVISIBLE_BECOMES_WALL
        ].index(elem.rule)
        base = self.assembler.custom(index)
        return self.assembler.colorize(base, elem.color)

    def dirt(self, elem):
        base = self.assembler.custom(10)
        return self.assembler.colorize(base, elem.color)

    def ice(self, elem):
        return self.assembler.cc2("ICE")

    def force(self, elem):
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

    def teleport(self, elem):
        frames = [self.assembler.custom(i) for i in range(6, 10)]
        return [self.assembler.colorize(frame, elem.color) for frame in frames]

    def trap(self, elem):
        base = self.assembler.cc2(
            "TRAP_SHUT" if elem.rule == TrapRule.SHUT else "TRAP")
        colored = self.assembler.colorize(base, elem.color)
        if elem.channel:
            label = self.label(elem.channel, elem.color)
            return self.assembler.stack(colored, label)
        return colored

    def gravel(self, elem):
        return self.assembler.custom(11)

    def pop_up_wall(self, elem):
        base = self.assembler.cc2("POP_UP_WALL")
        colored = self.assembler.colorize(base, elem.color)
        if elem.count and elem.count > 1:
            label = self.label(elem.count, elem.color)
            return self.assembler.stack(colored, label)
        return colored

    def stepping_stone(self, elem):
        top = self.assembler.custom(12)
        bottom = self.fire(elem) if elem.rule == "fire" else self.water(elem)
        combined = []
        for frame in bottom:
            combined.append(self.assembler.stack(frame, top))
        if elem.count and elem.count > 1:
            label = self.label(elem.count, elem.color)
            return [self.assembler.stack(frame, label) for frame in combined]
        return combined

    def hint(self, elem):
        return self.assembler.cc2("HINT")

    def cloner(self, elem):
        cloner = self.assembler.cc2("CLONER")
        d = elem.direction
        processed = self.assembler.colorize(cloner, elem.color)
        if d:
            arrow = self.assembler.cc2(f"CLONER_ARROW_{d.name}")
            processed.paste(arrow, (0, 0), arrow)
        return processed
