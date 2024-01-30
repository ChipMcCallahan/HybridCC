import logging

import pygame
from PIL import Image

from hybrid_cc.game.elements.instances.player import Player
from hybrid_cc.game.elements.instances.trick_wall import TrickWall
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.key_rule import KeyRule
from hybrid_cc.gfx.gfx_provider import GfxProvider
from hybrid_cc.shared import Direction, Id
from hybrid_cc.shared.shared_utils import is_iter
from hybrid_cc.shared.tool_rule import ToolRule


# noinspection PyTypeChecker
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
        if id_and_kwargs.id in (Id.DIRT_BLOCK, Id.ICE_BLOCK):
            pyg_result = [pyg_result] * 8
        self.cache[cache_key] = pyg_result
        return pyg_result

    @staticmethod
    def expand_to_8_frames(frames):
        num_frames = len(frames)
        if num_frames == 8:
            return frames  # Return the original array if it already has 8 frames

        # Calculate the number of times each frame should be repeated
        repeat_times = 8 // num_frames

        expanded_frames = []
        for frame in frames:
            expanded_frames.extend([frame] * repeat_times)

        return expanded_frames

    def provide_one(self, elem, logic_tick=0, **kwargs):
        frames = self.provide(elem, **kwargs)
        if not is_iter(frames):
            return frames, None
        move_tick = logic_tick // 4
        if isinstance(elem, Mob) and elem.last_move_tick is not None:
            offset = move_tick - elem.last_move_tick
            if offset < 2:
                index = offset * 4 + logic_tick % 4
                frames = self.expand_to_8_frames(frames)
                frame = self.moving_double(frames[index], index, elem)
                offset = (0, 0)
                if elem.direction == Direction.S:
                    offset = (0, -1)  # render one tile higher than normal
                elif elem.direction == Direction.E:
                    offset = (-1, 0)  # render one tile left of normal
                return frame, offset
            else:
                return frames[0], None
        if len(frames) == 4:
            return frames[(move_tick // 2) % 4], None
        return frames[0], None

    @staticmethod
    def moving_double(frame, index, elem):
        if elem.direction in (Direction.N, Direction.S):
            if frame.get_size() == (32, 64):  # Blobs, Walkers
                return frame
            main_surface = pygame.Surface((32, 64), pygame.SRCALPHA)
            y = index * 4 if elem.direction == Direction.S else 32 - index * 4
            main_surface.blit(frame, (0, y))
            return main_surface
        elif elem.direction in (Direction.E, Direction.W):
            if frame.get_size() == (64, 32):  # Blobs, Walkers
                return frame
            main_surface = pygame.Surface((64, 32), pygame.SRCALPHA)
            x = index * 4 if elem.direction == Direction.E else 32 - index * 4
            main_surface.blit(frame, (x, 0))
            return main_surface
        return frame

    def provide_viewport(self, layers, logic_tick, nw_pos, se_pos, camera):
        w, h = se_pos[0] - nw_pos[0] + 1, se_pos[1] - nw_pos[1] + 1

        raw_surface = pygame.Surface((w * 32,
                                      h * 32))

        for layer in layers:
            for i in range(nw_pos[0], se_pos[0] + 1):
                for j in range(nw_pos[1], se_pos[1] + 1):
                    position = (i, j, 0)
                    here = layer.get(position, None)
                    if not is_iter(here):
                        here = [here]
                    for elem in here:
                        kwargs = {}
                        if not elem:
                            continue
                        if isinstance(elem, Player):
                            for tag in elem.tags:
                                kwargs[tag] = True
                        if isinstance(elem, TrickWall):
                            if position in TrickWall.show_secrets_positions:
                                kwargs["show_secrets"] = True
                        img, offset = self.provide_one(elem, logic_tick, **kwargs)
                        offset = offset or (0, 0)
                        x = i + offset[0] - nw_pos[0]
                        y = j + offset[1] - nw_pos[1]
                        raw_surface.blit(img,
                                         (x * 32,
                                          y * 32))

        if (w, h) == (9, 9):
            return raw_surface

        crop_x, crop_y = tuple(
            i * 32 for i in camera.get_tile_offset(logic_tick))
        if crop_x < 0:
            crop_x = 32 + crop_x
        if crop_y < 0:
            crop_y = 32 + crop_y
        crop_width, crop_height = 9 * 32, 9 * 32
        return raw_surface.subsurface((crop_x, crop_y, crop_width, crop_height))

    class HashableObject:
        def __init__(self, **attributes):
            self.__dict__.update(attributes)

        def __hash__(self):
            return hash(tuple(sorted(self.__dict__.items())))

        def __eq__(self, other):
            return (isinstance(other, self.__class__) and
                    self.__dict__ == other.__dict__)

    floor_elem = HashableObject(id=Id.FLOOR, color=Color.GREY)
    inventory_elems = {}

    def provide_keys(self):
        key_counts = getattr(Player.instance, "keys", None)
        if not key_counts:
            return
        keys = []
        for color in Color:
            if color in key_counts:
                keys.append((color, key_counts[color]))
        raw_surface = pygame.Surface((len(keys) * 32, 32))
        for index, pair in enumerate(keys):
            color, count = pair
            if pair not in self.inventory_elems:
                elem = self.HashableObject(id=Id.KEY, color=color, count=count,
                                           rule=KeyRule.DEFAULT)
                self.inventory_elems[pair] = elem
            floor_img, _ = self.provide_one(self.floor_elem)
            key_img, _ = self.provide_one(self.inventory_elems[pair])
            raw_surface.blit(floor_img, (index * 32, 0))
            raw_surface.blit(key_img, (index * 32, 0))
        return raw_surface

    # noinspection PyTypeChecker
    def provide_tools(self):
        tool_counts = getattr(Player.instance, "tools", None)
        if not tool_counts:
            return
        tools = []
        for id in (Id.FLIPPERS, Id.FIRE_BOOTS, Id.SKATES, Id.SUCTION_BOOTS):
            if id in tool_counts:
                tools.append((id, tool_counts[id]))
        raw_surface = pygame.Surface((len(tools) * 32, 32))
        for index, pair in enumerate(tools):
            id, count = pair
            if pair not in self.inventory_elems:
                elem = self.HashableObject(id=id, count=count,
                                           rule=ToolRule.DEFAULT)
                self.inventory_elems[pair] = elem
            floor_img, _ = self.provide_one(self.floor_elem)
            tool_img, _ = self.provide_one(self.inventory_elems[pair])
            raw_surface.blit(floor_img, (index * 32, 0))
            raw_surface.blit(tool_img, (index * 32, 0))
        return raw_surface

    @staticmethod
    def to_pygame_surface(pil_image: Image):
        # Convert a PIL image to a Pygame surface
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        return pygame.image.fromstring(data, size, mode)
