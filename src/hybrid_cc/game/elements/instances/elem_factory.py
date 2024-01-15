import logging
import re
from hybrid_cc.game.elements import instances
from hybrid_cc.shared import Id


class ElemFactory:
    id_to_class = {}

    def __init__(self):
        raise TypeError("Cannot instantiate ElemFactory class.")

    @classmethod
    def initialize(cls):
        logging.info("Initializing ElemFactory...")
        for attribute_name in dir(instances):
            element_class = getattr(instances, attribute_name)

            # Check if it's a class but not this class.
            if element_class is not cls and isinstance(element_class, type):
                # Convert from CamelCase to SNAKE_CASE to match Id.
                name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', attribute_name)
                name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).upper()
                try:
                    _id = Id[name]
                    cls.id_to_class[_id] = element_class
                except KeyError:
                    raise TypeError(f"Instance class was {element_class}, but "
                                    f"'{name}' was not found in Id enum")

    @classmethod
    def construct_at(cls, pos, _id, **kwargs):
        if not cls.id_to_class:
            raise TypeError(f"ElemFactory was not initialized!")
        if _id not in cls.id_to_class:
            raise TypeError(f"Id {_id} was not found in Elem class registry.")
        instance_class = cls.id_to_class[_id]
        factory = getattr(instance_class, "construct_at")
        return factory(pos, **kwargs)
