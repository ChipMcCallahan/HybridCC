"""
Module for the MapCell class, representing a cell in a map with various attributes.
"""
from hybrid_cc.shared import Layer


class MapCell:
    """
    Represents a cell in a map as a simple wrapper around a dictionary.
    Allows setting and getting values based on Layer enum.
    """

    def __init__(self):
        """
        Initializes a MapCell with an empty dictionary to store layer values.
        """
        self.layers = {}

    def set(self, layer, value):
        """
        Sets the value for a given layer.
        """
        self.layers[layer] = value

    def get(self, layer):
        """
        Gets the value associated with a given layer.
        """
        return self.layers.get(layer)

    @property
    def terrain(self):
        """Gets the TERRAIN layer for this MapCell."""
        return self.get(Layer.TERRAIN)

    @terrain.setter
    def terrain(self, value):
        """Sets the TERRAIN layer for this MapCell."""
        self.set(Layer.TERRAIN, value)

    @property
    def terrain_mod(self):
        """Gets the TERRAIN_MOD layer for this MapCell."""
        return self.get(Layer.TERRAIN_MOD)

    @terrain_mod.setter
    def terrain_mod(self, value):
        """Sets the TERRAIN_MOD layer for this MapCell."""
        self.set(Layer.TERRAIN_MOD, value)

    @property
    def pickup(self):
        """Gets the PICKUP layer for this MapCell."""
        return self.get(Layer.PICKUP)

    @pickup.setter
    def pickup(self, value):
        """Sets the PICKUP layer for this MapCell."""
        self.set(Layer.PICKUP, value)

    @property
    def sides(self):
        """Gets the SIDES layer for this MapCell."""
        return self.get(Layer.SIDES)

    @sides.setter
    def sides(self, value):
        """Sets the SIDES layer for this MapCell."""
        self.set(Layer.SIDES, value)

    @property
    def mob(self):
        """Gets the MOB layer for this MapCell."""
        return self.get(Layer.MOB)

    @mob.setter
    def mob(self, value):
        """Sets the MOB layer for this MapCell."""
        self.set(Layer.MOB, value)
