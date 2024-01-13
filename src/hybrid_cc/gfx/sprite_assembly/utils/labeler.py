import importlib.resources

from PIL import Image, ImageDraw

from hybrid_cc.gfx.sprite_assembly.utils.colorizer import Colorizer

PADDING = 1
BG_COLOR = "black"
TILES_WIDE = 13
LETTER_WIDTH = {
    "M": 5,
    "W": 5,
    "N": 5,
    "+": 5,
    "Q": 4
}


class Labeler:
    def __init__(self):
        with importlib.resources.path("hybrid_cc.art",
                                      "letters5x5.png") as path:
            self.letters = Image.open(path)

    @staticmethod
    def _calculate_position(text_width, p):
        x, y = 0, 0

        # Horizontal position
        if p in [1, 4, 7]:  # Left
            x = 2
        elif p in [2, 5, 8]:  # Center
            x = (32 - text_width) // 2 - 1
        elif p in [3, 6, 9]:  # Right
            x = 32 - text_width - 4

        # Vertical position
        if p in [1, 2, 3]:  # Top
            y = 2
        elif p in [4, 5, 6]:  # Middle
            y = (32 - 5) // 2 - 1
        elif p in [7, 8, 9]:  # Bottom
            y = 32 - 5 - 4

        return x, y

    def label(self, label, p=5, color="white"):
        label = str(label) if isinstance(label, int) else label
        color = color or "white"
        label_image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        label_draw = ImageDraw.Draw(label_image)

        # Calculate text size. Chars in "MNW" are 5px wide, others are 3.
        text_width = (sum(LETTER_WIDTH.get(c, 3) for c in label)
                      + max(0, len(label) - 1))

        # Calculate label position
        x, y = self._calculate_position(text_width, p)

        # Calculate rectangle size
        rect_x0 = x - 1
        rect_y0 = y - 1
        rect_x1 = x + text_width + 2
        rect_y1 = y + 5 + 2

        # Draw rounded rectangle
        label_draw.rounded_rectangle((rect_x0, rect_y0, rect_x1, rect_y1),
                                     radius=1, fill=BG_COLOR)

        # Draw the label text
        letter_images = (self.char(c) for c in label)
        combined_img = Image.new("RGBA", (text_width, 5),
                                   (0, 0, 0, 0))  # Transparent background
        # Paste each image into the combined image
        x_offset = 0
        for img in letter_images:
            combined_img.paste(img, (x_offset, 0), img)
            x_offset += img.width + 1  # 1 pixel space between letters

        colored_img = Colorizer.colorize(combined_img, color)

        # Paste text_image onto label_image
        label_image.paste(colored_img,(x + 1, y + 1), colored_img)

        return label_image

    def char(self, c):
        c = str(c) if isinstance(c, int) else c
        assert len(c) == 1 and (c.isdigit() or c.isupper() or c in "+")
        if c.isupper():
            i = ord(c) - ord('A')
        elif c == "+":
            i = 36
        else:
            i = 26 + int(c)

        x = (i % TILES_WIDE) * 5
        y = (i // TILES_WIDE) * 5

        tile = self.letters.crop((x, y, x + 5, y + 5))
        if c == "Q":
            return tile.crop((0+1, 0, 5, 5))
        if c not in "MNW+":
            return tile.crop((0+1, 0, 5-1, 5))
        return tile
