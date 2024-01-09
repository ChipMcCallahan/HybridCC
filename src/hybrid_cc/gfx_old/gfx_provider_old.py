import importlib.resources

from cc_tools import CC2SpriteSet
from PIL import Image

from hybrid_cc.gfx.sprite_assembly.gfx_utils import colorize
from hybrid_cc.gfx.sprite_assembly.label_maker import LabelMaker
from hybrid_cc.shared import Id
from hybrid_cc.shared.button_rule import ButtonRule
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.key_rule import KeyRule
from hybrid_cc.shared.thief_rule import ThiefRule
from hybrid_cc.shared.trap_rule import TrapRule
from hybrid_cc.shared.trick_wall_rule import TrickWallRule

DEFAULT_COLOR = "white"


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

    def process(self, elem, base_images, *, default_color=None):
        color = elem.color or default_color
        memo_name = hash(elem)
        if memo_name in self.memoized:
            return self.memoized[memo_name]

        if not isinstance(base_images, list):
            base_images = [base_images]

        processed_images = [
            colorize(img, color) for img
            in base_images] if color else base_images

        color = color or DEFAULT_COLOR

        if elem.id == Id.TRAP and elem.channel is not None:
            label = str(elem.channel)
            self.label_maker.position = 9  # bottom right
            self.label_maker.text_color = color.name.lower()
            processed_images = [
                self.label_maker.apply(img, label)
                for img in processed_images
            ]
        elif (elem.id in (Id.POP_UP_WALL, Id.STEPPING_STONE)
              and elem.count and elem.count > 1):
            label = str(elem.count)
            self.label_maker.position = 9  # bottom right
            self.label_maker.text_color = color
            processed_images = [
                self.label_maker.apply(img, label)
                for img in processed_images
            ]
        elif elem.id in (Id.DOOR, Id.SOCKET) and elem.count and elem.count > 1:
            label = str(elem.count)
            self.label_maker.position = 7  # lower left
            self.label_maker.text_color = color
            processed_images = [
                self.label_maker.apply(img, label)
                for img in processed_images
            ]
        elif elem.id in (Id.KEY, Id.TOOL) and elem.count and elem.count > 1:
            label = str(elem.count)
            self.label_maker.position = 3  # upper right
            self.label_maker.text_color = color
            processed_images = [
                self.label_maker.apply(img, label)
                for img in processed_images
            ]
        elif elem.id in (Id.BUTTON,) and elem.channel:
            label = str(elem.channel)
            self.label_maker.position = 7  # lower left
            self.label_maker.text_color = color
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
        return self.process(elem, self.cc2("FLOOR"), default_color=Color.GREY)

    def wall(self, elem):
        return self.process(elem, self.cc2("WALL"), default_color=Color.GREY)

    def exit(self, elem):
        base = self.cc2_series("EXIT", 4)
        return self.process(elem, base, default_color=Color.BLUE)

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
        return self.process(elem, base, default_color=Color.GREY)

    def dirt(self, elem):
        return self.process(elem, self.custom_tile(10),
                            default_color=Color.GREY)

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
        return self.process(elem, frames, default_color=Color.GREY)

    def teleport(self, elem):
        frames = [self.custom_tile(i) for i in range(6, 10)]
        return self.process(elem, frames, default_color=Color.BLUE)

    def trap(self, elem):
        name = "TRAP_SHUT" if elem.rule == TrapRule.SHUT else "TRAP"
        return self.process(elem, self.cc2(name), default_color=Color.TAN)

    def gravel(self, elem):
        return self.custom_tile(11)

    def pop_up_wall(self, elem):
        return self.process(elem, self.cc2("POP_UP_WALL"),
                            default_color=Color.GREY)

    def stepping_stone(self, elem):
        top = self.custom_tile(12)
        bottom = self.fire(elem) if elem.rule == "fire" else self.water(elem)
        combined = []
        for frame in bottom:
            copy = frame.copy()
            copy.paste(top, (0, 0), top)
            combined.append(copy)
        return self.process(elem, combined)

    def hint(self, elem):
        return self.cc2("HINT")

    def cloner(self, elem):
        cloner = self.cc2("CLONER").copy()
        d = elem.direction
        processed = self.process(elem, cloner, default_color=Color.RED)
        if d:
            arrow = self.cc2(f"CLONER_ARROW_{d.name}")
            processed.paste(arrow, (0, 0), arrow)
        return processed

    def door(self, elem):
        return self.process(elem, self.custom_tile(13),
                            default_color=Color.GREY)

    def thief(self, elem):
        if elem.rule == ThiefRule.KEYS:
            return self.custom_tile(14)
        return self.cc2("THIEF")

    def socket(self, elem):
        return self.process(elem, self.custom_tile(15),
                            default_color=Color.GREY)

    def bomb(self, elem):
        return self.process(elem, self.custom_tile(16),
                            default_color=Color.RED)

    def key(self, elem):
        index = {
            KeyRule.DEFAULT: 17,
            KeyRule.FRAGILE: 18,
            KeyRule.ACTING_DIRT: 19,
        }[elem.rule]
        return self.process(elem, self.custom_tile(index))

    def tool(self, elem):
        name = ["FLIPPERS", "FIRE_BOOTS", "SKATES", "SUCTION_BOOTS"][
            elem.rule.value - 1]
        return self.process(elem, self.cc2(name))

    def button(self, elem):
        if elem.rule == ButtonRule.TOGGLE:
            frames = [self.custom_tile(i) for i in range(20, 22)]
            return self.process(elem, frames, default_color=Color.GREY)
        elif elem.rule == ButtonRule.HOLD_ALL:
            return self.process(elem, self.custom_tile(22),
                                default_color=Color.GREY)
        elif elem.rule == ButtonRule.HOLD_ONE:
            return self.process(elem, self.custom_tile(23),
                                default_color=Color.GREY)
        elif elem.rule == ButtonRule.DPAD:
            return self.process(elem, self.custom_tile(24),
                                default_color=Color.GREY)
