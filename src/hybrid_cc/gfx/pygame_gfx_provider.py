import logging
import math

import pygame
from PIL import Image

from hybrid_cc.game.elements.instances.exit import Exit
from hybrid_cc.game.elements.instances.player import Player
from hybrid_cc.gfx.gfx_provider import GfxProvider
from hybrid_cc.shared import Direction
from hybrid_cc.shared.shared_utils import is_iter


class PygameGfxProvider:
    def __init__(self):
        self.cache = {}
        self.cache_misses = 0
        self.gfx_provider = GfxProvider()
        self.viewport = pygame.Surface((320, 320))

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

    def provide_one(self, elem, logic_tick):
        frames = self.provide(elem)
        if not is_iter(frames):
            return frames, None
        move_tick = logic_tick // 4
        if isinstance(elem, Player) and elem.last_move_tick is not None:
            offset = move_tick - elem.last_move_tick
            if offset < 2:
                index = offset * 4 + logic_tick % 4
                frame = self.moving_double(frames[index], index, elem)
                offset = (0, 0)
                if elem.direction == Direction.S:
                    offset = (0, -1)  # render one tile higher than normal
                elif elem.direction == Direction.E:
                    offset = (-1, 0)  # render one tile left of normal
                return frame, offset
            else:
                return frames[0], None
        if isinstance(elem, Exit):
            return frames[move_tick % 4], None
        return frames[0], None

    @staticmethod
    def moving_double(frame, index, elem):
        if elem.direction in (Direction.N, Direction.S):
            main_surface = pygame.Surface((32, 64), pygame.SRCALPHA)
            y = index * 4 if elem.direction == Direction.S else 32 - index * 4
            main_surface.blit(frame, (0, y))
            return main_surface
        elif elem.direction in (Direction.E, Direction.W):
            main_surface = pygame.Surface((64, 32), pygame.SRCALPHA)
            x = index * 4 if elem.direction == Direction.E else 32 - index * 4
            main_surface.blit(frame, (x, 0))
            return main_surface
        return frame

    def provide_viewport(self, size, layers, logic_tick):
        move_tick = logic_tick // 4
        tick_modulo = logic_tick % 4
        tile_size = 32
        raw_surface = pygame.Surface((size * tile_size, size * tile_size))

        player_offset = (0, 0)
        player_tile = (0, 0)

        def get_player_offset(player):
            stale_time = math.inf
            if player.last_move_tick is not None:
                stale_time = move_tick - player.last_move_tick
            if stale_time >= 2:
                return 0, 0
            scale = tile_size - (stale_time * 4 + tick_modulo) * 4
            offset_x, offset_y, _ = player.direction.reverse().value
            return offset_x * scale, offset_y * scale

        for layer in layers:
            for i in range(0, size):
                for j in range(0, size):
                    elem = layer.get((i, j), None)
                    if not elem:
                        continue
                    if isinstance(elem, Player):
                        player_offset = get_player_offset(elem)
                        player_tile = (i, j)
                    img, offset = self.provide_one(elem, logic_tick)
                    offset = offset or (0, 0)
                    x = i + offset[0]
                    y = j + offset[1]
                    raw_surface.blit(img,
                                     (x * tile_size,
                                      y * tile_size))

        crop_width, crop_height = 9 * tile_size, 9 * tile_size

        # Calculate player's absolute position on the raw_surface
        player_abs_x = (player_tile[0] * tile_size) + player_offset[0]
        player_abs_y = (player_tile[1] * tile_size) + player_offset[1]

        # Calculate the top-left corner for cropping, centered on the player
        crop_x = player_abs_x - crop_width // 2 + tile_size // 2
        crop_y = player_abs_y - crop_height // 2 + tile_size // 2

        # Clamp the crop area so it doesn't go out of the raw_surface's bounds
        crop_x = max(min(crop_x, size * tile_size - crop_width), 0)
        crop_y = max(min(crop_y, size * tile_size - crop_height), 0)

        # Create a new surface for the cropped area
        return raw_surface.subsurface((crop_x, crop_y, crop_width, crop_height))

    @staticmethod
    def to_pygame_surface(pil_image: Image):
        # Convert a PIL image to a Pygame surface
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        return pygame.image.fromstring(data, size, mode)
