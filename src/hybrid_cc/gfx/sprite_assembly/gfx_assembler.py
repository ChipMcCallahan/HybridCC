import importlib.resources

from PIL import Image
from cc_tools import CC2SpriteSet

from hybrid_cc.gfx.sprite_assembly.utils.labeler import Labeler
from hybrid_cc.gfx.sprite_assembly.utils.stacker import Stacker
from hybrid_cc.gfx.sprite_assembly.utils.colorizer import Colorizer


class GfxAssembler:
    def __init__(self):
        self.sprite_set = CC2SpriteSet.factory("flat.bmp")
        self.labeler = Labeler()
        with importlib.resources.path("hybrid_cc.art", "custom.png") as path:
            image = Image.open(path)
            self.custom_tiles = image.convert('RGBA')

    def custom(self, index):
        image = self.custom_tiles
        tiles_wide = image.width // 32
        x = (index % tiles_wide) * 32
        y = (index // tiles_wide) * 32
        return image.crop((x, y, x + 32, y + 32))

    def cc2(self, name):
        return self.sprite_set.sprites[name].copy()

    def cc2_series(self, base, n):
        return [self.cc2(name) for name in
                [f"{base}_{i}" if i > 0 else base for i in range(n)]]

    def stack(self, *images):
        """Pass-through method to stack images."""
        return Stacker.stack(*images)

    def colorize(self, base_img, color, brightness=1.5):
        """Pass-through method to colorize an image."""
        return Colorizer.colorize(base_img, color, brightness)

    def label_ne(self, label, color="white"):
        """Label the image at the top right."""
        return self.labeler.label(label, 3, color)

    def label_se(self, label, color="white"):
        """Label the image at the bottom right."""
        return self.labeler.label(label, 9, color)

    def label_sw(self, label, color="white"):
        """Label the image at the bottom left."""
        return self.labeler.label(label, 7, color)
