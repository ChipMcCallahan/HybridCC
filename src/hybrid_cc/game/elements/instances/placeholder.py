import logging
from collections import defaultdict

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest, LoseRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.move_result import MoveResult


class Placeholder(Elem):
    positions = set()
    instance = None
    trying_to_enter = defaultdict(set)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.positions.clear()
        cls.instance = None
        cls.trying_to_enter.clear()

    @classmethod
    def construct_at(cls, p, **kwargs):
        elem = super().construct_at(p, **kwargs)
        cls.instance = elem
        cls.positions.add(p)
        return elem

    @classmethod
    def do_class_planning(cls, **kwargs):
        requests = [DestroyRequest(src=cls.instance, tgt=cls.instance, p=p) for
                    p in cls.positions]
        cls.positions.clear()
        cls.trying_to_enter.clear()
        return [], requests

    def start_enter(self, mob, p, d):
        move_result = MoveResult.PASS
        if mob.id != Id.PLAYER:
            previously_tried = mob.mob_id in self.trying_to_enter[p]
            if not previously_tried:
                move_result = MoveResult.DEFER
                self.trying_to_enter[p].add(mob.mob_id)
        return move_result, []

    def finish_enter(self, mob, p, d):
        return [
            DestroyRequest(tgt=self, src=mob, p=p)
        ]
