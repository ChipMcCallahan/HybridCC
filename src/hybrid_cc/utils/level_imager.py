"""Class that creates level images"""

from PIL import Image

from hybrid_cc.gfx.gfx_provider import GfxProvider
from hybrid_cc.gfx.sprite_assembly.utils.labeler import Labeler
from hybrid_cc.gfx.sprite_assembly.utils.stacker import Stacker


class LevelImager:
    """Class that creates level images"""

    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.show_secrets = None
        self.set_show_secrets(True)
        self.show_monster_order = None
        self.set_show_monster_order(True)
        self.gfx_provider = GfxProvider()
        self.labeler = Labeler()
        self.stacker = Stacker()
        # TODO: draw arrows on cloner blocks

    def set_show_secrets(self, show_secrets):
        """Set the show_secrets boolean on self and CC1SpriteSet."""
        self.show_secrets = show_secrets

    def set_show_monster_order(self, show_monster_order):
        """Set the show_monster_order boolean."""
        self.show_monster_order = show_monster_order

    def level_image(self, level):
        """Create a PNG image from a Level."""
        images = []
        x, y, z = level.size
        for k in range(z):
            images.append(Image.new("RGBA", (32 * x, 32 * y)))

            for j in range(y):
                for i in range(x):
                    p = (i, j, k)
                    cell = level.get(p)

                    elems = [e for e in [
                        cell.terrain, cell.terrain_mod, cell.pickup,
                        cell.mob] + cell.sides if e is not None]
                    kwargs = {"show_secrets": self.show_secrets}
                    tile_images = [self.gfx_provider.provide_one(elem, **kwargs)
                                   for elem in elems]
                    tile_img = self.stacker.stack(*tile_images)

                    if self.show_monster_order and p in level.movement:
                        index = str(level.movement.index(p))
                        tile_img = self.stacker.stack(tile_img,
                                                      self.labeler.label(index,
                                                                         1))

                    images[k].paste(tile_img, (i * 32, j * 32), tile_img)
        return images
