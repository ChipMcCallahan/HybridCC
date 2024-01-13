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
        """Get the value for arg, or default if not exists."""
        return self.kwargs.get(arg, default)

    def set(self, arg, val):
        """Set the value for arg."""
        self.kwargs[arg] = val

    @property
    def color(self):
        """Gets the color of the element."""
        return self.get('color')

    @color.setter
    def color(self, value):
        """Sets the color of the element."""
        self.set('color', value)

    @property
    def rule(self):
        """Gets the rule of the element."""
        return self.get('rule')

    @rule.setter
    def rule(self, value):
        """Sets the rule of the element."""
        self.set('rule', value)

    @property
    def count(self):
        """Gets the count of the element."""
        return self.get('count')

    @count.setter
    def count(self, value):
        """Sets the count of the element."""
        self.set('count', value)

    @property
    def channel(self):
        """Gets the channel of the element."""
        return self.get('channel')

    @channel.setter
    def channel(self, value):
        """Sets the channel of the element."""
        self.set('channel', value)

    @property
    def direction(self):
        """Gets the direction of the element."""
        return self.get('direction')

    @direction.setter
    def direction(self, value):
        """Sets the direction of the element."""
        self.set('direction', value)

    def __repr__(self):
        """
        Generates an unambiguous string representation of the element.
        """
        return f"Elem(id={self.id!r}, kwargs={self.kwargs!r})"

    def __str__(self):
        """
        Generates a readable string representation of the element.
        """
        kwargs_str = ", ".join(f"{key}={value}" for key, value in self.kwargs.items())
        return f"Elem with ID: {self.id}, Properties: {kwargs_str}"
