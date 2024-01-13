import logging

from hybrid_cc.gfx.sprite_assembly.mob_gfx import MobGfx
from hybrid_cc.gfx.sprite_assembly.pickup_gfx import PickupGfx
from hybrid_cc.gfx.sprite_assembly.sides_gfx import SidesGfx
from hybrid_cc.gfx.sprite_assembly.terrain_gfx import TerrainGfx
from hybrid_cc.gfx.sprite_assembly.terrain_mod_gfx import TerrainModGfx
from hybrid_cc.shared import Layer


class GfxProvider:
    def __init__(self):
        self.cache = {}
        self.terrain_gfx = TerrainGfx()
        self.terrain_mod_gfx = TerrainModGfx()
        self.pickup_gfx = PickupGfx()
        self.sides_gfx = SidesGfx()
        self.mob_gfx = MobGfx()

    def provide(self, obj, **kwargs):
        """
        Provide a graphic based on an object and optional additional parameters.

        Parameters:
            obj (hashable): The object to provide graphics for.
            **kwargs: Additional keyword arguments to be considered for the
            graphics provision.

        Returns:
            A PIL Image or a list of PIL Images associated with the object and
            keyword arguments.
        """
        # Combine key and kwargs into a single hashable object for caching
        cache_key = (obj, frozenset(kwargs.items()))

        # Check if the item is in the cache
        if cache_key in self.cache:
            return self.cache[cache_key]

        eid = obj.id if hasattr(obj, "id") else None
        layer = eid.layer() if hasattr(eid, "layer") else None

        if eid and layer:
            gfx_obj = {
                Layer.TERRAIN: self.terrain_gfx,
                Layer.PICKUP: self.pickup_gfx,
                Layer.TERRAIN_MOD: self.terrain_mod_gfx,
                Layer.SIDES: self.sides_gfx,
                Layer.MOB: self.mob_gfx
            }
            method = getattr(gfx_obj[layer], eid.name.lower(), None)
            result = method(obj, **kwargs)
            self.cache[cache_key] = result
            return result

        raise ValueError("No Gfx Could be provided.")

    def provide_one(self, obj, **kwargs):
        frames = self.provide(obj, **kwargs)
        if isinstance(frames, list):
            return frames[0]
        return frames
