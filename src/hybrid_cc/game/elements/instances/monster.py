import logging

from hybrid_cc.game.elements.instances.player import Player
from hybrid_cc.game.elements.mob import Mob
from hybrid_cc.game.request import MoveRequest, DestroyRequest, LoseRequest, \
    CreateRequest
from hybrid_cc.game.rng import RNG
from hybrid_cc.shared import Id, Direction
from hybrid_cc.shared.kwargs import RULE, DIRECTION
from hybrid_cc.shared.monster_rule import MonsterRule
from hybrid_cc.shared.move_result import MoveResult


class Monster(Mob):
    kwarg_filter = (RULE, DIRECTION)  # Retain these kwargs only.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def init_at_level_load(cls):
        logging.info(f"Initializing {cls.__name__}...")

    # --------------------------------------------------------------------------
    # PLANNING PHASE
    # --------------------------------------------------------------------------

    def do_planning(self, tick, **kwargs):
        n = 3 if self.rule in (MonsterRule.TEETH, MonsterRule.BLOB) else 1
        if self.moved_last_n_ticks(tick, n=n):
            return [], []

        d = self.direction
        if self.rule == MonsterRule.FIREBALL:
            directions = [d, d.right(), d.left(), d.reverse()]
        elif self.rule == MonsterRule.GLIDER:
            directions = [d, d.left(), d.right(), d.reverse()]
        elif self.rule == MonsterRule.ANT:
            directions = [d.left(), d, d.right(), d.reverse()]
        elif self.rule == MonsterRule.PARAMECIUM:
            directions = [d.right(), d, d.left(), d.reverse()]
        elif self.rule == MonsterRule.BLOB:
            pool = [Direction[d] for d in "NESW"]
            directions = []
            while len(pool) > 0:
                directions.append(pool.pop(RNG.next() % len(pool)))
        elif self.rule == MonsterRule.TEETH:
            if not Player.instance:
                return [], []
            tx, ty, _ = self.p
            px, py, _ = Player.instance.p
            dx, dy = px - tx, py - ty
            x_dir, y_dir = None, None
            if dx < 0:
                x_dir = Direction.W
            if dx > 0:
                x_dir = Direction.E
            if dy < 0:
                y_dir = Direction.N
            if dy > 0:
                y_dir = Direction.S
            directions = [d for d in [y_dir, x_dir] if d]
            if abs(dx) > abs(dy):
                directions = reversed(directions)
        elif self.rule == MonsterRule.WALKER:
            d = self.direction
            pool = [d.right(), d.left(), d.reverse()]
            directions = [d]
            while len(pool) > 0:
                directions.append(pool.pop(RNG.next() % len(pool)))
        elif self.rule == MonsterRule.BALL:
            directions = [d, d.reverse()]
        else:
            raise ValueError(f"Unexpected monster rule: {self.rule}")
        return MoveRequest.from_directions(self.mob_id, directions), []

    # --------------------------------------------------------------------------
    # ACCESS RULES
    # --------------------------------------------------------------------------

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
                LoseRequest(cause=self, p=p)
            ]

    # --------------------------------------------------------------------------
    # OTHER
    # --------------------------------------------------------------------------

    def on_completed_move(self, old_p, new_p, tick, **kwargs):
        super().on_completed_move(old_p, new_p, tick, **kwargs)
        return [CreateRequest(p=old_p, id=Id.PLACEHOLDER)]
