import logging

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest, CreateRequest
from hybrid_cc.shared import Id
from hybrid_cc.shared.kwargs import COLOR, RULE
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import PUSHABLE
from hybrid_cc.shared.trick_wall_rule import TrickWallRule


class TrickWall(Elem):
    kwarg_filter = (COLOR, RULE)  # Retain these kwargs only.
    show_secrets_positions = dict()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")
        cls.show_secrets_positions = dict()

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------
    @classmethod
    def do_class_planning(cls, **kwargs):
        keys_to_remove = []
        for key in cls.show_secrets_positions:
            if cls.show_secrets_positions[key] is None:
                continue
            cls.show_secrets_positions[key] -= 1
            if cls.show_secrets_positions[key] == 0:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            cls.show_secrets_positions.pop(key)

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

    def start_enter(self, mob, position, direction):
        if self.rule == TrickWallRule.PASS_THRU:
            if not mob.tagged(PUSHABLE):
                return MoveResult.PASS, None
        elif (self.rule == TrickWallRule.BECOMES_WALL or
              self.rule == TrickWallRule.INVISIBLE_BECOMES_WALL):
            return MoveResult.FAIL, [
                DestroyRequest(target=self, pos=position),
                CreateRequest(eid=Id.WALL, pos=position, color=self.color)
            ]
        elif self.rule == TrickWallRule.BECOMES_FLOOR:
            return MoveResult.PASS, [
                DestroyRequest(target=self, pos=position),
                CreateRequest(eid=Id.FLOOR, pos=position, color=self.color)
            ]
        elif self.rule == TrickWallRule.PERMANENTLY_INVISIBLE:
            self.show_secrets_positions[position] = 4
        return MoveResult.FAIL, None

    def finish_enter(self, mob, position, direction):
        if self.rule == TrickWallRule.PASS_THRU:
            self.show_secrets_positions[position] = None

    def finish_exit(self, mob, position, direction):
        if self.rule == TrickWallRule.PASS_THRU:
            self.show_secrets_positions.pop(position)
