from hybrid_cc.shared import Id
from hybrid_cc.shared.move_result import MoveResult


class MoveHandler:
    def __init__(self, map):
        self.map = map

    def move(self, mob, d, tick):
        requests = []

        result, new_requests = self.test_move(mob, d)
        requests += new_requests or []
        if result != MoveResult.PASS:
            result, new_requests = self.fail_move(mob, result, d)
            requests += new_requests or []
            return result, requests

        result, new_requests = self.start_move(mob, d)
        requests += new_requests or []
        if result != MoveResult.PASS:
            result, new_requests = self.fail_move(mob, result, d)
            requests += new_requests or []
            return result, requests

        requests += self.finish_move(mob, d, tick) or []

        return result, requests

    @staticmethod
    def fail_move(mob, move_result, d):
        method = getattr(mob, "on_failed_move", None)
        requests = None
        if method:
            requests = method(move_result, d)
        return move_result, requests

    def test_move(self, mob, d):
        return self._do_trial_move(mob, d, 'test')

    def start_move(self, mob, d):
        return self._do_trial_move(mob, d, 'start')

    def _do_trial_move(self, mob, d, phase):
        here_p, offset = mob.position, d.value
        there_p = tuple(a + b for a, b in zip(here_p, offset))

        here = self.map.get(here_p)
        there = None if self.map.is_oob(there_p) else self.map.get(there_p)

        result, requests = MoveResult.PASS, []

        # Process exit
        for elem in here.all():
            if elem is mob:
                continue
            method = getattr(elem, f"{phase}_exit", None)
            if method:
                result, new_requests = method(mob, here_p, d)
                requests += new_requests or []
                if result != MoveResult.PASS:
                    return result, requests

        if not there:
            return MoveResult.FAIL, requests

        # Process enter
        for elem in there.all():
            method = getattr(elem, f"{phase}_enter", None)
            if method:
                result, new_requests = method(mob, there_p, d)
                requests += new_requests or []
                if result != MoveResult.PASS:
                    return result, requests
        return result, requests

    def finish_move(self, mob, d, tick):
        here_p, offset = mob.position, d.value
        there_p = tuple(a + b for a, b in zip(here_p, offset))

        if self.map.is_oob(there_p):
            raise AttributeError(f"Position {there_p} is oob, can't finalize a "
                                 f"move there")

        here, there = self.map.get(here_p), self.map.get(there_p)

        requests = []

        # Process exit
        for elem in here.all():
            if elem is mob:
                continue
            method = getattr(elem, "finish_exit", None)
            if method:
                requests += method(mob, here_p, d) or []

        # Process enter
        for elem in there.all():
            method = getattr(elem, f"finish_enter", None)
            if method:
                requests += method(mob, there_p, d) or []

        here.remove(mob)
        there.add(mob)
        mob.on_completed_move(here_p, there_p, tick)
        return requests