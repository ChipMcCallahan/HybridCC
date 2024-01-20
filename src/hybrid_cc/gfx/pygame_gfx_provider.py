import logging

import pygame
from PIL import Image

from hybrid_cc.gfx.gfx_provider import GfxProvider
from hybrid_cc.shared.shared_utils import is_iter


class PygameGfxProvider:
    def __init__(self):
        self.cache = {}
        self.cache_misses = 0
        self.gfx_provider = GfxProvider()

    def provide(self, id_and_kwargs, **extra_kwargs):
        cache_key = (id_and_kwargs, frozenset(extra_kwargs.items()))

        # Check if the item is in the cache
        if cache_key in self.cache:
            return self.cache[cache_key]

        self.cache_misses += 1
        if self.cache_misses % 100 == 0:
            logging.debug(f"{self.cache_misses} Pygame cache misses so far")
        if self.cache_misses % 10000 == 0:
            logging.warning(f"{self.cache_misses} Pygame cache misses so far")

        pil_result = self.gfx_provider.provide(id_and_kwargs, **extra_kwargs)
        if is_iter(pil_result):
            pyg_result = [self.to_pygame_surface(i) for i in pil_result]
        else:
            pyg_result = self.to_pygame_surface(pil_result)
        self.cache[cache_key] = pyg_result
        return pyg_result

    def provide_one(self, id_and_kwargs, **extra_kwargs):
        frames = self.provide(id_and_kwargs, **extra_kwargs)
        if is_iter(frames):
            return frames[0]
        return frames

    @staticmethod
    def to_pygame_surface(pil_image: Image):
        # Convert a PIL image to a Pygame surface
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        return pygame.image.fromstring(data, size, mode)
