"""This module provides image colorization functionality using the PIL
library."""
from PIL import ImageOps, ImageEnhance, Image, ImageColor

# How much brightness increase to apply to various colors so they look right.
BRIGHTNESS_ADJUSTMENTS = {
    "grey": 2.0,
    "green": 1.7,
}
DEFAULT_BRIGHTNESS = 1.5


class Colorizer:
    """A class for colorizing images with specified color and brightness."""

    @staticmethod
    def colorize(base_img, color, brightness=None):
        """Apply a color and brightness to a grayscale image."""
        color = color or "grey"

        if hasattr(color, "name"):
            color = color.name.lower()

        brightness = (brightness or
                      BRIGHTNESS_ADJUSTMENTS.get(color, DEFAULT_BRIGHTNESS))

        if not isinstance(base_img, Image.Image):
            raise TypeError("base_img must be a PIL Image instance")

        try:
            color = ImageColor.getcolor(color, "RGBA")
        except ValueError:
            raise ValueError(f"{color} is not a valid PIL color")

        # Convert the base image to grayscale
        img_gray = ImageOps.grayscale(base_img)

        # Apply the color to the grayscale image
        img_colored = ImageOps.colorize(img_gray, black="#00000000",
                                        white=color)

        # Apply the original alpha channel to the colored image
        img_colored.putalpha(base_img.split()[3])

        # Enhance the brightness of the colored image
        img_brightened = ImageEnhance.Brightness(img_colored).enhance(
            brightness)

        return img_brightened
