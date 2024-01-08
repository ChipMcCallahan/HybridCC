import importlib.resources

from cc_tools import CC2SpriteSet
from PIL import Image

from hybrid_cc.gfx.gfx_utils import colorize
from hybrid_cc.gfx.label_maker import LabelMaker
from hybrid_cc.shared import Id
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.trap_rule import TrapRule
from hybrid_cc.shared.trick_wall_rule import TrickWallRule


class GfxProvider:
    def __init__(self):
        self.sprite_set = CC2SpriteSet.factory("flat.bmp")
        self.memoized = {}
        self.label_maker = LabelMaker.new()
        with importlib.resources.path("hybrid_cc.art", "custom.png") as path:
            image = Image.open(path)
            self.custom = image.convert('RGBA')

    def custom_tile(self, index):
        image = self.custom
        tiles_wide = image.width // 32
        x = (index % tiles_wide) * 32
        y = (index // tiles_wide) * 32
        return image.crop((x, y, x + 32, y + 32))

    def provide(self, elem):
        method = getattr(self, elem.id.name.lower())
        return method(elem)

    def cc2(self, name):
        return self.sprite_set.sprites[name]

    def cc2_series(self, base, n):
        return [self.cc2(name) for name in
                [f"{base}_{i}" if i > 0 else base for i in range(n)]]

    def process(self, elem, default_color, base_images):
        color = elem.color or default_color
        memo_name = hash(elem)
        if memo_name in self.memoized:
            return self.memoized[memo_name]

        if not isinstance(base_images, list):
            base_images = [base_images]

        processed_images = [
            colorize(img, color) for img
            in base_images]

        if elem.id == Id.TRAP and elem.channel is not None:
            label = str(elem.channel)
            self.label_maker.position = 9  # bottom right
            self.label_maker.text_color = elem.color.name.lower()
            processed_images = [
                self.label_maker.apply(img, label)
                for img in processed_images
            ]

        # If there's only one image, don't store it as a list
        result = processed_images if len(processed_images) > 1 else \
            processed_images[0]

        self.memoized[memo_name] = result
        return result

    def floor(self, elem):
        return self.process(elem, Color.GREY, self.cc2("FLOOR"))

    def wall(self, elem):
        return self.process(elem, Color.GREY, self.cc2("WALL"))

    def exit(self, elem):
        base = self.cc2_series("EXIT", 4)
        return self.process(elem, Color.BLUE, base)

    def water(self, elem):
        return self.cc2_series("WATER", 4)

    def fire(self, elem):
        return self.cc2_series("FIRE", 4)

    def trick_wall(self, elem):
        index = [
            TrickWallRule.BECOMES_FLOOR,
            TrickWallRule.BECOMES_WALL,
            TrickWallRule.PASS_THRU,
            TrickWallRule.SOLID,
            TrickWallRule.PERMANENTLY_INVISIBLE,
            TrickWallRule.INVISIBLE_BECOMES_WALL
        ].index(elem.rule)
        base = self.custom_tile(index)
        return self.process(elem, Color.GREY, base)

    def dirt(self, elem):
        return self.process(elem, Color.GREY, self.cc2("DIRT"))

    def ice(self, elem):
        return self.cc2("ICE")

    def force(self, elem):
        if elem.direction:
            base = self.cc2(f"FORCE_N")
            frames = [self.cc2(f"FORCE_{elem.direction.name}")]
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
            frames = self.cc2_series(f"FORCE_RANDOM", 8)
        return self.process(elem, Color.GREEN, frames)

    def teleport(self, elem):
        frames = [self.custom_tile(i) for i in range(6, 10)]
        return self.process(elem, Color.BLUE, frames)

    def trap(self, elem):
        name = "TRAP_SHUT" if elem.rule == TrapRule.SHUT else "TRAP"
        return self.process(elem, Color.TAN, self.cc2(name))

    def gravel(self, elem):
        return self.cc2("GRAVEL")
