import logging

from hybrid_cc.gfx.sprite_assembly.mob_gfx import MobGfx
from hybrid_cc.gfx.sprite_assembly.pickup_gfx import PickupGfx
from hybrid_cc.gfx.sprite_assembly.sides_gfx import SidesGfx
from hybrid_cc.gfx.sprite_assembly.terrain_gfx import TerrainGfx
from hybrid_cc.gfx.sprite_assembly.terrain_mod_gfx import TerrainModGfx
from hybrid_cc.shared import Layer
from hybrid_cc.shared.shared_utils import is_iter


class GfxProvider:
    def __init__(self):
        self.cache = {}
        self.cache_misses = 0
        self.terrain_gfx = TerrainGfx()
        self.terrain_mod_gfx = TerrainModGfx()
        self.pickup_gfx = PickupGfx()
        self.sides_gfx = SidesGfx()
        self.mob_gfx = MobGfx()

    def provide(self, id_and_kwargs, **extra_kwargs):
        """
        Provide a graphic based on an object and optional additional parameters.

        Parameters:
            id_and_kwargs (hashable): The object to provide graphics for.
            **extra_kwargs: Additional keyword arguments to be considered for
            the graphics provision.

        Returns:
            A PIL Image or a list of PIL Images associated with the object and
            keyword arguments.
        """
        # Combine key and kwargs into a single hashable object for caching
        cache_key = (id_and_kwargs, frozenset(extra_kwargs.items()))

        # Check if the item is in the cache
        if cache_key in self.cache:
            return self.cache[cache_key]

        self.cache_misses += 1
        if self.cache_misses % 10000 == 0:
            logging.warning(f"{self.cache_misses} cache misses so far")

        id = id_and_kwargs.id if hasattr(id_and_kwargs, "id") else None
        layer = id.layer() if hasattr(id, "layer") else None

        if id and layer:
            gfx_obj = {
                Layer.TERRAIN: self.terrain_gfx,
                Layer.PICKUP: self.pickup_gfx,
                Layer.TERRAIN_MOD: self.terrain_mod_gfx,
                Layer.SIDES: self.sides_gfx,
                Layer.MOB: self.mob_gfx
            }
            method = getattr(gfx_obj[layer], id.name.lower(), None)
            result = method(id_and_kwargs, **extra_kwargs)
            self.cache[cache_key] = result
            return result

        raise ValueError("No Gfx Could be provided.")

    def provide_one(self, id_and_kwargs, **extra_kwargs):
        frames = self.provide(id_and_kwargs, **extra_kwargs)
        if is_iter(frames):
            return frames[0]
        return frames
