from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.request import DestroyRequest, CreateRequest
from hybrid_cc.shared.kwargs import COUNT, RULE
from hybrid_cc.shared.move_result import MoveResult
from hybrid_cc.shared.tag import COLLECTS_ITEMS, ENTERS_DIRT
from hybrid_cc.shared.tool_rule import ToolRule


class Tool(Elem):
    kwarg_filter = (RULE, COUNT)  # Retain these kwargs only.

    def test_enter(self, mob, p, d):
        if self.rule == ToolRule.DEFAULT:
            if mob.tagged(ENTERS_DIRT):
                return MoveResult.PASS, []
            return MoveResult.FAIL, []
        elif self.rule == ToolRule.ITEM_BARRIER:
            if mob.tools[self.id] > 0:
                return MoveResult.FAIL, []
            return MoveResult.PASS, []
        else:
            raise ValueError(f"invalid rule {self.rule}")

    def finish_enter(self, mob, p, d):
        if self.rule == ToolRule.DEFAULT and mob.tagged(COLLECTS_ITEMS):
            mob.tools[self.id] += 1
            requests = [DestroyRequest(target=self, p=p)]
            if self.count > 1:
                kwargs = {COUNT: self.count - 1, RULE: ToolRule.DEFAULT}
                requests.append(
                    CreateRequest(p=p, id=self.id, **kwargs))
            return requests
