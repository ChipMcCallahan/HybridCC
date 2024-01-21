from hybrid_cc.shared.move_result import MoveResult


class MoveHandler:
    def __init__(self, map):
        self.map = map

    def move(self, mob, d, tick):
        result = self.test_move(mob, d)
        if result != MoveResult.PASS:
            return result
        result = self.start_move(mob, d)
        if result != MoveResult.PASS:
            return result
        self.finish_move(mob, d, tick)
        return result

    def test_move(self, mob, d):
        return self._do_trial_move(mob, d, 'test')

    def start_move(self, mob, d):
        return self._do_trial_move(mob, d, 'start')

    def _do_trial_move(self, mob, d, phase):
        here_p, offset = mob.position, d.value
        there_p = tuple(a + b for a, b in zip(here_p, offset))

        if self.map.is_oob(there_p):
            return MoveResult.FAIL

        here, there = self.map.get(here_p), self.map.get(there_p)

        result = MoveResult.PASS

        # Process exit
        for elem in here.all():
            if elem is mob:
                continue
            method = getattr(elem, f"{phase}_exit", None)
            if method:
                result = method(mob, here_p, d)
                if result != MoveResult.PASS:
                    return result

        # Process enter
        for elem in there.all():
            method = getattr(elem, f"{phase}_enter", None)
            if method:
                result = method(mob, there_p, d)
                if result != MoveResult.PASS:
                    return result
        return result

    def finish_move(self, mob, d, tick):
        here_p, offset = mob.position, d.value
        there_p = tuple(a + b for a, b in zip(here_p, offset))

        if self.map.is_oob(there_p):
            raise AttributeError(f"Position {there_p} is oob, can't finalize a "
                                 f"move there")

        here, there = self.map.get(here_p), self.map.get(there_p)

        # Process exit
        for elem in here.all():
            if elem is mob:
                continue
            method = getattr(elem, "finish_exit", None)
            if method:
                method(mob, here_p, d)

        # Process enter
        for elem in there.all():
            method = getattr(elem, f"finish_enter", None)
            if method:
                method(mob, there_p, d)

        here.remove(mob)
        there.add(mob)
        mob.finalize_move(here_p, there_p, tick)
