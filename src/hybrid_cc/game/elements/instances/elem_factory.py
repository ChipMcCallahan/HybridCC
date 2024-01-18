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
                _id = Id.from_class_name(attribute_name)
                cls.id_to_class[_id] = element_class

    @classmethod
    def construct_at(cls, pos, _id, **kwargs):
        instance_class = cls.get_class(_id)
        constructor = getattr(instance_class, "construct_at")
        return constructor(pos, **kwargs)

    @classmethod
    def destruct_at(cls, pos, _id):
        instance_class = cls.get_class(_id)
        destructor = getattr(instance_class, "destruct_at")
        return destructor(pos)

    @classmethod
    def get_class(cls, _id):
        if not cls.id_to_class:
            raise TypeError(f"ElemFactory was not initialized!")
        if _id not in cls.id_to_class:
            raise TypeError(f"Id {_id} was not found in Elem class registry.")
        return cls.id_to_class[_id]