"""Module for stacking multiple images with transparency into one."""
from PIL import Image


class Stacker:
    """Class for stacking multiple images into one, respecting transparency."""

    @staticmethod
    def stack(*images):
        """
        Stack multiple images into a single new image using the alpha
        channel of each image as a mask.

        Parameters:
            *images: A variable number of Image.Image objects to be stacked.

        Returns: Image.Image: A new image consisting of all the stacked
        images, with transparency preserved.

        Raises:
            ValueError: If the images are not all the same size.
        """
        if not images:
            raise ValueError("At least one image is required to stack.")

        images = [image for image in images if image]

        # Verify all images are the same size
        image_size = images[0].size
        if not all(img.size == image_size for img in images):
            raise ValueError("All images must be the same size to combine.")

        # Create a new image with the width and height of the first image
        combined_image = Image.new('RGBA', image_size)

        # Paste images into the combined image using each image as its own mask
        for index, img in enumerate(images):
            combined_image.paste(img, (0, 0), img)

        return combined_image
