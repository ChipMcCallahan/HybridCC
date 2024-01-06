"""
Module for the MapCell class, representing a cell in a map with various attributes.
"""


class MapCell:
    """
    Represents a cell in a map as a simple wrapper around a dictionary.
    Allows setting and getting values based on Layer enum.
    """

    def __init__(self):
        """
        Initializes a MapCell with an empty dictionary to store layer values.
        """
        self.attributes = {}

    def set(self, layer, value):
        """
        Sets the value for a given layer.
        """
        self.attributes[layer] = value

    def get(self, layer):
        """
        Gets the value associated with a given layer.
        """
        return self.attributes.get(layer)
