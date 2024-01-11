"""Class for adding transparency to images."""
from PIL import Image


class Transparencizer:
    """Class for adding transparency to images."""
    def transparencize(self, base_image):
        """
            Applies a transparent square to an existing image. The transparency
            increases exponentially as one moves closer to the center.

            Args:
                base_image (PIL.Image.Image): The existing image to which the
                transparent square will be applied.

            Returns:
                PIL.Image.Image: The image with the applied transparent square.
            """
        # Ensure base image is in RGBA mode
        base_image = base_image.convert("RGBA")
        image_size = base_image.size[0]  # Assuming the image is square

        # Create a new image for the alpha mask
        alpha_mask = Image.new("L", (image_size, image_size), 0)

        # Center for the square
        center = (image_size / 2 - 0.5, image_size / 2 - 0.5)
        max_distance = min(center)  # Maximum distance from center to corner

        for y in range(image_size):
            for x in range(image_size):
                distance = max(abs(x - center[0]), abs(y - center[1]))

                # Calculate the alpha value based on the distance, making it
                # exponentially transparent as it gets closer to the center
                alpha = int(255 * (
                        distance / max_distance) ** 2)  # Exponential decrease

                # Set the pixel in the alpha mask
                alpha_mask.putpixel((x, y), alpha)

        # Combine the base image with the alpha mask
        base_image.putalpha(alpha_mask)

        return base_image
