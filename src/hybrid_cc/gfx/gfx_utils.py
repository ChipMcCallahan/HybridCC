from PIL import ImageOps, ImageEnhance

from hybrid_cc.shared.color import Color


def colorize(base_img, color, brightness=1.5):
    if isinstance(color, Color):
        color = color.value
    _, _, _, alpha = base_img.split()
    img_gray = ImageOps.grayscale(base_img)
    # The black argument is for the blackpoint(color to be applied to the
    # darkest point), and the color variable is for the whitepoint (color
    # to be applied to the lightest point).
    img_new = ImageOps.colorize(img_gray, "#00000000", color)
    img_new.putalpha(alpha)
    enhancer = ImageEnhance.Brightness(img_new)
    return enhancer.enhance(brightness)  # 1.5 is 50% brighter
