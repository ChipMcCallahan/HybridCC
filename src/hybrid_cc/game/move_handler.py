from hybrid_cc.shared import Id
from hybrid_cc.shared.move_result import MoveResult


class MoveHandler:
    def __init__(self, map):
        self.map = map

    def move(self, mob, d, tick, slap=None, sim_pos=None):
        requests = []
        result, new_requests = self.test_move(mob, d, sim_pos)
        requests += new_requests or []
        if result != MoveResult.PASS:
            result, new_requests = self.fail_move(mob, result, d)
            requests += new_requests or []
            return result, requests

        result, new_requests = self.start_move(mob, d, sim_pos)
        requests += new_requests or []
        if result != MoveResult.PASS:
            result, new_requests = self.fail_move(mob, result, d)
            requests += new_requests or []
            return result, requests

        if slap:
            slap_result, new_requests = self.test_move(mob, slap, sim_pos)
            requests += new_requests or []
            if slap_result == MoveResult.PASS:
                _, new_requests = self.start_move(mob, slap, sim_pos)
                requests += new_requests or []

        requests += self.finish_move(mob, d, tick, sim_pos) or []

        return result, requests

    @staticmethod
    def fail_move(mob, move_result, d):
        method = getattr(mob, "on_failed_move", None)
        requests = None
        if method:
            requests = method(move_result, d)
        return move_result, requests

    def test_move(self, mob, d, sim_pos=None):
        return self._do_trial_move(mob, d, 'test', sim_pos)

    def start_move(self, mob, d, sim_pos=None):
        return self._do_trial_move(mob, d, 'start', sim_pos)

    def _do_trial_move(self, mob, d, phase, sim_pos=None):
        here_p, offset = sim_pos or mob.position, d.value
        there_p = tuple(a + b for a, b in zip(sim_pos or here_p, offset))

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

    def finish_move(self, mob, d, tick, sim_pos=None):
        here_p, offset = mob.position, d.value
        there_p = tuple(a + b for a, b in zip(sim_pos or here_p, offset))

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
        new_requests = mob.on_completed_move(here_p, there_p, tick,
                                             simulated_position=sim_pos)
        if new_requests:
            requests.extend(new_requests)
        return requests
