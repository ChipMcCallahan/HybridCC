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
    def construct_at(cls, pos, **kwargs):
        elem = super().construct_at(pos, **kwargs)
        cls.instance = elem
        cls.positions.add(pos)
        return elem

    @classmethod
    def do_class_planning(cls, **kwargs):
        requests = [DestroyRequest(target=cls.instance, pos=p) for p in
                    cls.positions]
        cls.positions.clear()
        return [], requests

    @staticmethod
    def test_enter(mob, position, direction):
        if mob.id == Id.PLAYER:
            return MoveResult.PASS, []
        return MoveResult.FAIL, []

    def finish_enter(self, mob, position, direction):
        if mob.id == Id.PLAYER:
            return [
                DestroyRequest(target=mob, pos=position),
                DestroyRequest(target=self, pos=position),
                # TODO: pass (id, rule) into placeholder creation. Not sure
                # this is even possible since player moves first?
                LoseRequest(cause=self)
            ]
