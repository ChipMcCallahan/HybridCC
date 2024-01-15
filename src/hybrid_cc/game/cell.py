

class Cell:
    def __init__(self):
        self.terrain = None
        self.terrain_mod = None
        self.pickup = None
        self.mob = None
        self.sides = {}

    # -----------
    # BOOKKEEPING
    # -----------
    def add(self, _id, **kwargs):
        layer = _id.layer()
        method = getattr(self, f"set_{layer.name.lower()}")
        method(_id, **kwargs)

    def remove(self, _id):
        layer = _id.layer()
        remove_method_name = f"remove_{layer.name.lower()}"
        if hasattr(self, remove_method_name):
            method = getattr(self, remove_method_name)
            return method(_id)
        else:
            raise AttributeError(f"Remove method for '{layer.name}' not "
                                 f"implemented")

    # -----------
    # TERRAIN
    # -----------
    def set_terrain(self, _id, **kwargs):
        self.terrain = (_id, kwargs)

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
    def set_terrain_mod(self, _id, **kwargs):
        self.terrain_mod = (_id, kwargs)

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
    def set_pickup(self, _id, **kwargs):
        self.pickup = (_id, kwargs)

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
    def set_mob(self, _id, **kwargs):
        self.mob = (_id, kwargs)

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
    def set_sides(self, _id, **kwargs):
        self.sides[_id] = (_id, kwargs)

    def get_sides(self):
        return self.sides

    def remove_sides(self, _id):
        self.sides.pop(_id)
