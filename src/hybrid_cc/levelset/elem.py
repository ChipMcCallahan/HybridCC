"""
This module contains the Elem class, which represents a basic element in a game
or application with an associated Id and a set of arguments.
"""


class Elem:
    """
    A basic element in a game or application.

    Attributes:
        id (Id): An enum representing the type of the element.
        kwargs (dict): A dictionary of arguments associated with the element.
    """

    def __init__(self, _id, **kwargs):
        """
        Initializes a new instance of the Elem class.
        """
        self.id = _id
        self.kwargs = kwargs

    def __hash__(self):
        """
        Generates a hash value based on the id and kwargs of the element.

        Returns:
            int: A hash value representing the element.
        """
        # Create a tuple of all the key-value pairs in kwargs, plus the id
        # Sort the items to ensure consistent ordering
        items = tuple(sorted(self.kwargs.items())) + (self.id,)
        return hash(items)

    def get(self, arg, default=None):
        """
        Retrieves the value associated with the specified argument.
        Returns None if the argument does not exist in args.
        """
        return self.kwargs.get(arg, default)

    @property
    def color(self):
        """
        Retrieves the color associated with the element.
        Returns None if the color is not specified.
        """
        return self.get('color')

    @property
    def rule(self):
        """
        Retrieves the rule associated with the element.
        Returns None if the rule is not specified.
        """
        return self.get('rule')

    @property
    def count(self):
        """
        Retrieves the count associated with the element.
        Returns None if the count is not specified.
        """
        return self.get('count')

    @property
    def channel(self):
        """
        Retrieves the channel associated with the element.
        Returns None if the channel is not specified.
        """
        return self.get('channel')

    @property
    def direction(self):
        """
        Retrieves the direction associated with the element.
        Returns None if the direction is not specified.
        """
        return self.get('direction')
