import importlib.resources

from cc_tools import CC2SpriteSet
from PIL import ImageOps, ImageEnhance, Image

from hybrid_cc.shared import Id
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.trick_wall_rule import TrickWallRule


class GfxProvider:
    def __init__(self):
        self.sprite_set = CC2SpriteSet.factory("flat.bmp")
        self.memoized = {}
        with importlib.resources.path("hybrid_cc.art", "custom.png") as path:
            image = Image.open(path)
            self.custom = image.convert('RGBA')

    def custom_tile(self, index):
        image = self.custom
        tiles_wide = image.width // 32
        x = (index % tiles_wide) * 32
        y = (index // tiles_wide) * 32
        return image.crop((x, y, x + 32, y + 32))

    def demo(self, elem):
        if elem.id == Id.FLOOR:
            return self.floor(elem)

    def cc2(self, name):
        return self.sprite_set.sprites[name]

    def cc2_series(self, base, n):
        return [self.cc2(name) for name in
                [f"{base}_{i}" if i > 0 else base for i in range(n)]]

    def colorize(self, base_img, color, brightness=1.5):
        _, _, _, alpha = base_img.split()
        img_gray = ImageOps.grayscale(base_img)
        # The black argument is for the blackpoint(color to be applied to the
        # darkest point), and the color variable is for the whitepoint (color
        # to be applied to the lightest point).
        img_new = ImageOps.colorize(img_gray, "#00000000",
                                    color.value)
        img_new.putalpha(alpha)
        enhancer = ImageEnhance.Brightness(img_new)
        return enhancer.enhance(brightness)  # 1.5 is 50% brighter

    def process_element(self, elem, default_color, base_images):
        color = elem.get("color", default_color)
        memo_name = hash(elem)
        if memo_name in self.memoized:
            return self.memoized[memo_name]

        if not isinstance(base_images, list):
            base_images = [base_images]

        processed_images = [
            self.colorize(img, color) if color != default_color else img for img
            in base_images]

        # If there's only one image, don't store it as a list
        result = processed_images if len(processed_images) > 1 else \
            processed_images[0]

        self.memoized[memo_name] = result
        return result

    def floor(self, elem):
        return self.process_element(elem, Color.GREY, self.cc2("FLOOR"))

    def wall(self, elem):
        return self.process_element(elem, Color.GREY, self.cc2("WALL"))

    def exit(self, elem):
        base = self.cc2_series("EXIT", 4)
        return self.process_element(elem, Color.BLUE, base)

    def water(self):
        return self.cc2_series("WATER", 4)

    def fire(self):
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
        return self.process_element(elem, Color.GREY, base)
