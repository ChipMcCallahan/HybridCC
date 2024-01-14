"""Class for adding transparency to images."""
from PIL import Image


class Transparencizer:
    """Class for adding transparency to images."""
    def __init__(self):
        # Create a new image for the alpha mask
        self.alpha_mask = Image.new("L", (32, 32), 0)

        # Center for the square
        center = (32 / 2 - 0.5, 32 / 2 - 0.5)
        max_distance = min(center)  # Maximum distance from center to corner

        for y in range(32):
            for x in range(32):
                distance = max(abs(x - center[0]), abs(y - center[1]))

                # Calculate the alpha value based on the distance, making it
                # exponentially transparent as it gets closer to the center
                alpha = int(255 * (
                        distance / max_distance) ** 2)  # Exponential decrease

                # Set the pixel in the alpha mask
                self.alpha_mask.putpixel((x, y), alpha)

    def transparencize(self, base_image):
        """
            Applies a transparent square to an existing image. The transparency
            increases exponentially as one moves closer to the center.
            """
        if base_image.mode != 'RGBA':
            raise ValueError("Base image must be in RGBA mode")
        base_image.putalpha(self.alpha_mask)
        return base_image
