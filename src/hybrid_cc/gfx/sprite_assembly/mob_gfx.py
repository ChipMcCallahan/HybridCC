from hybrid_cc.gfx.sprite_assembly.gfx_assembler import GfxAssembler
from hybrid_cc.shared.color import Color


class MobGfx:
    def __init__(self):
        self.assembler = GfxAssembler()

    def label(self, label, color, **kwargs):
        # Always place label in center for Mob layer
        return self.assembler.label_ne(label, color)

    def dirt_block(self, elem, **kwargs):
        base = self.assembler.custom(38)
        if kwargs.get("transparent"):
            base = self.assembler.transparencize(base)
        return self.assembler.colorize(base, elem.color)

    def ice_block(self, elem, **kwargs):
        base = self.assembler.custom(39)
        if kwargs.get("transparent"):
            base = self.assembler.transparencize(base)
        return self.assembler.colorize(base, Color.CYAN)

    def monster(self, elem, **kwargs):
        method = getattr(self, elem.rule.name.lower(), None)
        return method(elem, **kwargs)

    def teeth(self, elem, **kwargs):
        d = "S" if elem.direction.name == "N" else elem.direction.name
        series = self.assembler.cc2_series(f"TEETH_{d}", 3)
        series.append(series[1])
        return series

    def blob(self, elem, **kwargs):
        return self.assembler.cc2("BLOB") #TODO: handle animation

    def fireball(self, elem, **kwargs):
        frames = self.assembler.cc2_series("FIREBALL", 4)
        return [frames[0]] + [frames[i] for i in (3, 2, 1)]

    def glider(self, elem, **kwargs):
        d = elem.direction.name
        return self.assembler.cc2_series(f"GLIDER_{d}", 2)

    def ant(self, elem, **kwargs):
        d = elem.direction.name
        return self.assembler.cc2_series(f"ANT_{d}", 4)

    def paramecium(self, elem, **kwargs):
        d = elem.direction.name
        frames = self.assembler.cc2_series(f"PARAMECIUM_{d}", 3)
        return frames + [frames[1]]

    def ball(self, elem, **kwargs):
        frames = self.assembler.cc2_series(f"BALL", 5)
        return frames + [frames[i] for i in (3, 2, 1)]

    def walker(self, elem, **kwargs):
        return self.assembler.cc2("WALKER") #TODO: handle animation

    def tank(self, elem, **kwargs):
        d = elem.direction.name
        return self.assembler.cc2_series(f"TANK_{d}", 2)

    def player(self, elem, **kwargs):
        d = elem.direction.name
        push = kwargs.get("pushing")
        swim = kwargs.get("swimming")
        if push:
            return self.assembler.cc2(f"PLAYER_PUSHING_{d}")
        if swim:
            return self.assembler.cc2_series(f"PLAYER_SWIMMING_{d}", 2)
        return self.assembler.cc2_series(f"PLAYER_{d}", 8)
