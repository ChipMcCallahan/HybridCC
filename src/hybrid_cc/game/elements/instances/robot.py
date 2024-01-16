from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import CHANNEL, COLOR


class Robot(Mob):
    kwarg_filter = (COLOR, CHANNEL)  # Retain these kwargs only.
    class_id = Id.ROBOT
    instances = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def construct_at(cls, pos, **kwargs):
        lookup_key = cls.class_lookup_key(**kwargs)
        if lookup_key not in cls.instances:
            cls.instances[lookup_key] = cls(**kwargs)
        return cls.instances[lookup_key]

    @classmethod
    def destruct_at(cls, pos, **kwargs):
        pass

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    def do_planning(self):
        raise NotImplementedError("Implement or remove.")

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    def test_enter(self, position, other, direction):
        raise NotImplementedError("Implement or remove.")

    def test_exit(self, position, other, direction):
        raise NotImplementedError("Implement or remove.")

    def start_enter(self, position, other, direction):
        raise NotImplementedError("Implement or remove.")

    def start_exit(self, position, other, direction):
        raise NotImplementedError("Implement or remove.")

    def finish_exit(self, position, other, direction):
        raise NotImplementedError("Implement or remove.")

    def finish_enter(self, position, other, direction):
        raise NotImplementedError("Implement or remove.")
