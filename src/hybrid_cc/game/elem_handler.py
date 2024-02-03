from hybrid_cc.game.elements import instances
from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.elements.instances.socket import Socket
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.shared import Id, Direction
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.kwargs import DIRECTION, SIDES, COLOR, RULE, COUNT, \
    CHANNEL
from hybrid_cc.shared.tag import OVERRIDDEN

DEFAULT_KWARGS = {
    COLOR: Color.GREY,
    RULE: None,
    COUNT: 1,
    CHANNEL: 0,
    SIDES: "",
    DIRECTION: Direction.S
}


class ElemHandler:
    def __init__(self, level):
        self.id_to_class = {}
        for attribute_name in dir(instances):
            element_class = getattr(instances, attribute_name)

            if isinstance(element_class, type):
                _id = Id.from_class_name(attribute_name)
                self.id_to_class[_id] = element_class

        Elem.init_at_level_load()
        Mob.init_at_level_load()
        for attribute_name in dir(instances):
            element_class = getattr(instances, attribute_name)

            # Check if it's a class but not this class.
            if element_class is not self and isinstance(element_class, type):
                if hasattr(element_class, "init_at_level_load"):
                    init_elem_cls = getattr(element_class, "init_at_level_load")
                    init_elem_cls()

        # Element specific initializations.
        Socket.set_chips_required(level.chips.copy())

    def construct_at(self, p, _id, **kwargs):
        kwargs = self.assign_kwarg_defaults(**kwargs)
        instance_class = self.get_class(_id)
        constructor = getattr(instance_class, "construct_at")
        return constructor(p, **kwargs)

    @staticmethod
    def destruct_at(p, elem):
        instance_class = elem.__class__
        destructor = getattr(instance_class, "destruct_at")
        destructor(elem, p)

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
        moves, requests = [], []

        # Class level plans (e.g. ice, force floor, dpad buttons)
        for elem_class in self.id_to_class.values():
            method = getattr(elem_class, "do_class_planning", None)
            if method:
                new_moves, new_requests = method(inputs=inputs, tick=tick)
                if new_moves:
                    moves.extend(new_moves)
                if new_requests:
                    requests.extend(new_requests)

        # Instance level plans (mobs)
        for mob_id, mob in Mob.instances.items():
            method = getattr(mob, "do_planning", None)
            if method:
                new_moves, new_requests = method(tick, inputs=inputs)

                # Don't do anything with the requests if overridden.
                if mob.tagged(OVERRIDDEN):
                    continue

                if new_moves:
                    if mob.id == Id.PLAYER:  # Player always moves first
                        moves = new_moves + moves
                    else:
                        moves += new_moves
                if new_requests:
                    requests.extend(new_requests)

        return moves, requests

    @staticmethod
    def get_mob(mob_id):
        return Mob.get_mob(mob_id)
