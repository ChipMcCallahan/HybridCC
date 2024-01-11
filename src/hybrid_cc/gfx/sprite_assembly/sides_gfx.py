from hybrid_cc.gfx.sprite_assembly.gfx_assembler import GfxAssembler


class SidesGfx:
    def __init__(self):
        self.assembler = GfxAssembler()

    def panel(self, elem, **kwargs):
        sides = elem.get("sides")  # expect "NESW"
        base = self.assembler.stack(
            *[self.assembler.custom("NESW".index(d.upper()) + 30) for d in
              sides])
        return self.assembler.colorize(base, elem.color)

    def corner(self, elem, **kwargs):
        sides = elem.get("sides")  # expect "NW", "NE", "SW", "SE"
        base = self.assembler.custom(
            ("SE", "SW", "NW", "NE").index(sides.upper()) + 34)
        return self.assembler.colorize(base, elem.color)
