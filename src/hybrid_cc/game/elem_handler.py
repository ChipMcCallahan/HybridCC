import logging
from hybrid_cc.game.elements import instances
from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.shared import Id, Direction
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.kwargs import DIRECTION, SIDES, COLOR, RULE, COUNT, \
    CHANNEL

DEFAULT_KWARGS = {
    COLOR: Color.GREY,
    RULE: None,
    COUNT: 1,
    CHANNEL: 0,
    SIDES: "",
    DIRECTION: Direction.S
}


class ElemHandler:
    def __init__(self):
        self.id_to_class = {}
        for attribute_name in dir(instances):
            element_class = getattr(instances, attribute_name)

            if isinstance(element_class, type):
                _id = Id.from_class_name(attribute_name)
                self.id_to_class[_id] = element_class

    def init_at_game_load(self):
        logging.info(f"Initializing {self.__name__} at game load...")

    def init_at_level_load(self):
        logging.info(f"Initializing {self.__name__}...")
        Elem.init_at_level_load()
        Mob.init_at_level_load()
        for attribute_name in dir(instances):
            element_class = getattr(instances, attribute_name)

            # Check if it's a class but not this class.
            if element_class is not self and isinstance(element_class, type):
                if hasattr(element_class, "init_at_level_load"):
                    init_elem_cls = getattr(element_class, "init_at_level_load")
                    init_elem_cls()

    def construct_at(self, pos, _id, **kwargs):
        kwargs = self.assign_kwarg_defaults(**kwargs)
        instance_class = self.get_class(_id)
        constructor = getattr(instance_class, "construct_at")
        return constructor(pos, **kwargs)

    @staticmethod
    def destruct_at(pos, elem):
        instance_class = elem.__class__
        destructor = getattr(instance_class, "destruct_at")
        destructor(pos)

    def get_class(self, _id):
        if not self.id_to_class:
            raise TypeError(f"{self.__name__} was not initialized!")
        if _id not in self.id_to_class:
            raise TypeError(f"Id {_id} was not found in Elem class registry.")
        return self.id_to_class[_id]

    @staticmethod
    def assign_kwarg_defaults(**kwargs):
        new_kwargs = kwargs.copy()
        for kwarg in (COLOR, RULE, COUNT, CHANNEL, SIDES, DIRECTION):
            new_kwargs[kwarg] = kwargs.get(kwarg) or DEFAULT_KWARGS[kwarg]
        return new_kwargs

    def collect_move_plans(self, inputs, tick):
        all_move_plans = []

        # Class level plans (e.g. ice, force floor, dpad buttons)
        for elem_class in self.id_to_class.values():
            method = getattr(elem_class, "do_class_planning", None)
            if method:
                move_plan = method(inputs=inputs, tick=tick)
                if move_plan:
                    all_move_plans.append(move_plan)

        # Instance level plans (mobs)
        for mob_id, mob in Mob.instances.items():
            method = getattr(mob, "do_planning", None)
            if method:
                move_plan = method(inputs=inputs, tick=tick)
                if move_plan:
                    all_move_plans.append(move_plan)

        return all_move_plans

    @staticmethod
    def get_mob(mob_id):
        return Mob.get_mob(mob_id)

    @staticmethod
    def exists(mob_id):
        return Mob.exists(mob_id)
