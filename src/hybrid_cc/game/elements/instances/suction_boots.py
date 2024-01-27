import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COUNT, RULE


class SuctionBoots(Elem):
    kwarg_filter = (RULE, COUNT)  # Retain these kwargs only.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------
    @classmethod
    def do_class_planning(cls, **kwargs):
        pass
    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------
    def test_enter(self, mob, position, direction):
        raise NotImplementedError("Implement or remove.")

    def test_exit(self, mob, position, direction):
        raise NotImplementedError("Implement or remove.")

    def start_enter(self, mob, position, direction):
        raise NotImplementedError("Implement or remove.")

    def start_exit(self, mob, position, direction):
        raise NotImplementedError("Implement or remove.")

    def finish_exit(self, mob, position, direction):
        raise NotImplementedError("Implement or remove.")

    def finish_enter(self, mob, position, direction):
        raise NotImplementedError("Implement or remove.")
