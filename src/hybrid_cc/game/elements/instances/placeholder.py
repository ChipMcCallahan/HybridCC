import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest, LoseRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.move_result import MoveResult


class Placeholder(Elem):
    positions = set()
    instance = None

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.positions.clear()
        cls.instance = None

    @classmethod
    def construct_at(cls, p, **kwargs):
        elem = super().construct_at(p, **kwargs)
        cls.instance = elem
        cls.positions.add(p)
        return elem

    @classmethod
    def do_class_planning(cls, **kwargs):
        requests = [DestroyRequest(target=cls.instance, p=p) for p in
                    cls.positions]
        cls.positions.clear()
        return [], requests

    @staticmethod
    def test_enter(mob, p, direction):
        if mob.id == Id.PLAYER:
            return MoveResult.PASS, []
        return MoveResult.FAIL, []

    def finish_enter(self, mob, p, direction):
        if mob.id == Id.PLAYER:
            return [
                DestroyRequest(target=mob, p=p),
                DestroyRequest(target=self, p=p),
                # TODO: pass (id, rule) into placeholder creation. Not sure
                # this is even possible since player moves first?
                LoseRequest(cause=self, p=p)
            ]
