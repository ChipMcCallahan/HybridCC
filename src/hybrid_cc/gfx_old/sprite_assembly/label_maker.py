import importlib.resources

from PIL import Image, ImageDraw

class LabelMaker:
    def __init__(self, *, text_color, bg_color, position):
        with importlib.resources.path("hybrid_cc.art",
                                      "letters5x5.png") as path:
            self.letters = Image.open(path)
        self.text_color = text_color
        self.bg_color = bg_color
        self.text_height = 5
        self.padding = 1
        self.position = position
        if position in (3, 6, 9):
            self.justify = "right"
        elif position in (2, 5, 8):
            self.justify = "center"
        elif position in (1, 4, 7):
            self.justify = "left"

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, value):
        self._text_color = value

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, value):
        self._bg_color = value

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, value):
        self._padding = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def custom_tile(self, index):
        image = self.letters
        tiles_wide = image.width // 5
        x = (index % tiles_wide) * 5
        y = (index // tiles_wide) * 5
        return image.crop((x, y, x + 5, y + 5))

    def char(self, c):
        c = str(c) if isinstance(c, int) else c
        assert len(c) == 1 and (c.isdigit() or c.isupper())
        if c.isupper():
            i = ord(c) - ord('A')
        else:
            i = 26 + int(c)
        tile = self.custom_tile(i)
        if c not in "MNW":
            return tile.crop((1, 0, 4, 5))
        return tile

    def apply(self, image, label):
        label_image = self.make(label)
        image_copy = image.copy()
        image_copy.paste(label_image, (0, 0), label_image)
        return image_copy

    def make(self, label):
        label_image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        label_draw = ImageDraw.Draw(label_image)

        # Calculate text size. Chars in "MNW" are 5px wide, others are 3.
        text_width = (sum(5 if c in "MNW" else 3 for c in label)
                      + max(0, len(label) - 1))
        text_height = self.text_height

        # Calculate label position
        x, y = self._calculate_position(text_width, text_height)

        # Offset from border
        offset_x = 2
        offset_y = 1

        # Adjust x and y based on position
        if self.position in [1, 4, 7]:  # Left
            x += offset_x
        elif self.position in [3, 6, 9]:  # Right
            x -= offset_x

        if self.position in [1, 2, 3]:  # Top
            y += offset_y
        elif self.position in [7, 8, 9]:  # Bottom
            y -= offset_y

        # Calculate rectangle size
        rect_x0 = x - self.padding
        rect_y0 = y - self.padding
        rect_x1 = x + text_width + self.padding + 1
        rect_y1 = y + text_height + self.padding + 1

        text_image = Image.new("RGBA", (32, 32), (255, 255, 255, 255))

        # Draw rounded rectangle
        label_draw.rounded_rectangle((rect_x0, rect_y0, rect_x1, rect_y1),
                                     radius=self.padding, fill=self.bg_color)

        # Draw the label text
        letter_images = (self.char(c) for c in label)
        combined_image = Image.new("RGBA", (text_width, text_height),
                                   (0, 0, 0, 0))  # Transparent background
        # Paste each image into the combined image
        x_offset = 0
        for img in letter_images:
            combined_image.paste(img, (x_offset, 0))
            x_offset += img.width + 1  # 1 pixel space between letters

        text_image = colorize(combined_image, self._text_color)

        # Paste text_image onto label_image
        label_image.paste(text_image,
                          (x + 1, y + 1),
                          text_image)

        return label_image

    def _calculate_position(self, text_width, text_height):
        x, y = 0, 0
        tile_width, tile_height = 32, 32

        # Horizontal position
        if self.position in [1, 4, 7]:  # Left
            x = 0
        elif self.position in [2, 5, 8]:  # Center
            x = (tile_width - text_width) // 2
        elif self.position in [3, 6, 9]:  # Right
            x = tile_width - text_width - 2

        # Vertical position
        if self.position in [1, 2, 3]:  # Top
            y = self.padding
        elif self.position in [4, 5, 6]:  # Middle
            y = (tile_height - text_height) // 2 - 1
        elif self.position in [7, 8, 9]:  # Bottom
            y = tile_height - text_height - self.padding - 2

        return x, y

    @staticmethod
    def new():
        return LabelMaker(
            text_color="red",
            bg_color="black",
            position=5,  # Center
        )
