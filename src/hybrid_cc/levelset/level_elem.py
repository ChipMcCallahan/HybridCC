"""
This module contains the Elem class, which represents a basic element in a game
or application with an associated Id and a set of arguments.
"""
from hybrid_cc.shared.kwargs import SIDES, DIRECTION, RULE, COUNT, COLOR, \
    CHANNEL


class LevelElem:
    """
    An immutable element in a game or application.

    Attributes: id (Id): An enum representing the type of the element.
    direction, rule, count, color, channel, sides: Various attributes of the
    element.
    """

    def __init__(self, _id, direction=None, rule=None, count=None, color=None,
                 channel=None, sides=None):
        """
        Initializes a new instance of the Elem class.
        """
        self._id = _id
        self._direction = direction
        self._rule = rule
        self._count = count
        self._color = color
        self._channel = channel
        self._sides = sides

    def get_kwargs(self):
        return {
            DIRECTION: self.direction,
            RULE: self.rule,
            COUNT: self.count,
            COLOR: self.color,
            CHANNEL: self.channel,
            SIDES: self.sides
        }

    @property
    def id(self):
        """Gets the id of the element."""
        return self._id

    @property
    def direction(self):
        """Gets the direction of the element."""
        return self._direction

    @property
    def rule(self):
        """Gets the rule of the element."""
        return self._rule

    @property
    def count(self):
        """Gets the count of the element."""
        return self._count

    @property
    def color(self):
        """Gets the color of the element."""
        return self._color

    @property
    def channel(self):
        """Gets the channel of the element."""
        return self._channel

    @property
    def sides(self):
        """Gets the sides of the element."""
        return self._sides

    def __hash__(self):
        """
        Generates a hash value based on the attributes of the element.

        Returns:
            int: A hash value representing the element.
        """
        return hash((self._id, self._direction, self._rule, self._count,
                     self._color, self._channel, self._sides))

    def __eq__(self, other):
        """Check equality with another Elem instance."""
        if not isinstance(other, LevelElem):
            return False
        return (self._id, self._direction, self._rule, self._count, self._color,
                self._channel, self._sides) == \
            (other._id, other._direction, other._rule, other._count,
             other._color, other._channel, other._sides)

    def __repr__(self):
        """
        Generates an unambiguous string representation of the element.
        """
        return (
            f"Elem(id={self._id!r}, direction={self._direction!r}, rule={self._rule!r}, "
            f"count={self._count!r}, color={self._color!r}, channel={self._channel!r}, sides={self._sides!r})")

    def __str__(self):
        """
        Generates a readable string representation of the element.
        """
        attributes = [f"direction={self._direction}", f"rule={self._rule}",
                      f"count={self._count}",
                      f"color={self._color}", f"channel={self._channel}",
                      f"sides={self._sides}"]
        attributes_str = ", ".join(
            attr for attr in attributes if attr.split('=')[1] != 'None')
        return f"Elem with ID: {self._id}, Properties: {attributes_str}"
