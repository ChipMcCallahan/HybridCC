"""
Module for the LevelCell class, representing a cell in a map with various attributes.
"""
from hybrid_cc.shared import Layer


class LevelCell:
    """
    Represents a cell in a map as a simple wrapper around a dictionary.
    Allows setting and getting values based on Layer enum.
    """

    def __init__(self):
        """
        Initializes a LevelCell with an empty dictionary to store layer values.
        """
        self.layers = {}
        self._sides = []

    def set(self, layer, elem):
        """
        Sets the value for a given layer.
        """
        if layer != elem.id.layer():
            raise ValueError(
                f"Layer {layer} mismatch: {elem} had "
                f"layer {elem.id.layer()}.")
        self.layers[layer] = elem

    def get(self, layer):
        """
        Gets the value associated with a given layer.
        """
        return self.layers.get(layer)

    @property
    def terrain(self):
        """Gets the TERRAIN layer."""
        return self.get(Layer.TERRAIN)

    @terrain.setter
    def terrain(self, value):
        """Sets the TERRAIN layer."""
        self.set(Layer.TERRAIN, value)

    @property
    def terrain_mod(self):
        """Gets the TERRAIN_MOD layer."""
        return self.get(Layer.TERRAIN_MOD)

    @terrain_mod.setter
    def terrain_mod(self, value):
        """Sets the TERRAIN_MOD layer."""
        self.set(Layer.TERRAIN_MOD, value)

    @property
    def pickup(self):
        """Gets the PICKUP layer."""
        return self.get(Layer.PICKUP)

    @pickup.setter
    def pickup(self, value):
        """Sets the PICKUP layer."""
        self.set(Layer.PICKUP, value)

    @property
    def sides(self):
        """Gets the sides list."""
        return self._sides

    def add_sides(self, new_sides):
        """Add new sides to the list. new_sides can be a single item or a
        list of items"""
        if isinstance(new_sides, list):
            self._sides.extend(new_sides)
        else:
            self._sides.append(new_sides)
        for elem in self._sides:
            if elem.id.layer() != Layer.SIDES:
                raise ValueError(
                    f"Layer {Layer.SIDES} mismatch: {elem} had "
                    f"layer {elem.id.layer()}.")

    @property
    def mob(self):
        """Gets the MOB layer."""
        return self.get(Layer.MOB)

    @mob.setter
    def mob(self, elem):
        """Sets the MOB layer."""
        self.set(Layer.MOB, elem)

    def get_elem_by_id(self, eid):
        here = self.get(eid.layer)
        return here if here.id == eid else None

    def contains(self, eid):
        return self.get_elem_by_id(eid) is not None

    def contains_any(self, *eids):
        for eid in eids:
            if self.contains(eid):
                return True
        return False
