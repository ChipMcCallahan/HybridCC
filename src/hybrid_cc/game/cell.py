from hybrid_cc.game.elements.instances.elem_factory import ElemFactory
from hybrid_cc.shared import Id


class Cell:
    def __init__(self, position):
        self.position = position
        self.terrain = None
        self.terrain_mod = None
        self.pickup = None
        self.mob = None
        self._sides = {}

    # -----------
    # BOOKKEEPING
    # -----------
    def construct(self, _id, **kwargs):
        elem = ElemFactory.construct_at(self.position, _id, **kwargs)
        self.simple_add(elem)
        return elem

    def destruct(self, elem_or_id):
        _id = elem_or_id if isinstance(elem_or_id, Id) else elem_or_id.id
        self.simple_remove(_id)
        return ElemFactory.destruct_at(self.position, _id)

    def simple_add(self, elem):
        layer = elem.id.layer()
        set_layer = getattr(self, f"set_{layer.name.lower()}")
        return set_layer(elem)

    def simple_remove(self, elem_or_id):
        _id = elem_or_id if isinstance(elem_or_id, Id) else elem_or_id.id
        layer = _id.layer()
        remove_method_name = f"remove_{layer.name.lower()}"
        method = getattr(self, remove_method_name)
        return method(_id)

    def get_elems(self):
        return [e for e in (self.terrain, self.terrain_mod,
                            self.pickup, self.mob)
                + tuple(self._sides.values()) if e]

    # -----------
    # TERRAIN
    # -----------
    def set_terrain(self, elem):
        self.terrain = elem

    def get_terrain(self):
        return self.terrain

    def remove_terrain(self, _id):
        if self.terrain and self.terrain.id == _id:
            self.terrain = None
            return True
        return False

    # -----------
    # TERRAIN MOD
    # -----------
    def set_terrain_mod(self, elem):
        self.terrain_mod = elem

    def get_terrain_mod(self):
        return self.terrain_mod

    def remove_terrain_mod(self, _id):
        if self.terrain_mod and self.terrain_mod.id == _id:
            self.terrain_mod = None
            return True
        return False

    # -----------
    # PICKUP
    # -----------
    def set_pickup(self, elem):
        self.pickup = elem

    def get_pickup(self):
        return self.pickup

    def remove_pickup(self, _id):
        if self.pickup and self.pickup.id == _id:
            self.pickup = None
            return True
        return False

    # -----------
    # MOB
    # -----------
    def set_mob(self, elem):
        self.mob = elem

    def get_mob(self):
        return self.mob

    def remove_mob(self, _id):
        if self.mob and self.mob.id == _id:
            self.mob = None
            return True
        return False

    # -----------
    # SIDES
    # -----------
    def set_sides(self, elem):
        self._sides[elem.id] = elem

    def get_sides(self):
        return list(self._sides.values())

    def remove_sides(self, _id):
        self._sides.pop(_id)
