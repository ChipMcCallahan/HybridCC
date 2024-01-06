"""
This module contains the Elem class, which represents a basic element in a game
or application with an associated Id and a set of arguments.
"""


class Elem:
    """
    A basic element in a game or application.

    Attributes:
        id (Id): An enum representing the type of the element.
        args (dict): A dictionary of arguments associated with the element.
    """

    def __init__(self, id, **kwargs):
        """
        Initializes a new instance of the Elem class.
        """
        self.id = id
        self.args = kwargs

    def get(self, arg):
        """
        Retrieves the value associated with the specified argument.
        Returns None if the argument does not exist in args.
        """
        return self.args.get(arg)