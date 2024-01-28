from math import floor, ceil

from hybrid_cc.shared import Direction

VIEWPORT_SIZE = 9
TILE_SIZE = 32


class Camera:
    def __init__(self, target, gameboard):
        self.target = target
        self.target_position = None
        self.position = None
        self.direction = None
        self.last_move_tick = None
        self.gameboard = gameboard
        self.margin = VIEWPORT_SIZE // 2  # 4
        self.update()

    def update(self):
        self.target_position = getattr(self.target, "position", (0, 0, 0))
        self.direction = getattr(self.target, "direction", Direction.S)
        self.last_move_tick = getattr(self.target, "last_move_tick", None)

        x, y, z = self.target_position
        x, y = max(x, self.margin), max(y, self.margin)
        x = min(x, self.gameboard.size[0] - self.margin)
        y = min(y, self.gameboard.size[1] - self.margin)
        self.position = x, y, z

    def get_tile_offset(self, logic_tick):
        """Get the camera offset in terms of fractions of a tile."""
        move_tick, tick_modulo = logic_tick // 4, logic_tick % 4
        target_offset = (0, 0)
        if self.last_move_tick is not None:
            stale_time = move_tick - self.last_move_tick
            if stale_time < 2:
                fraction = 1 - ((stale_time * 4 + tick_modulo) / 8)
                offset_x, offset_y, _ = self.direction.reverse().value
                offset_x *= fraction
                offset_y *= fraction
                target_offset = offset_x, offset_y
        return target_offset

    def get_target_render_position(self, logic_tick):
        return tuple(a + b for a, b in zip(self.target_position,
                                           self.get_tile_offset(logic_tick)))

    def get_tile_bounds(self, logic_tick):
        # Clamp camera position to moving target position, not to exceed
        # *margin* tiles from level edge.
        tx, ty = self.get_target_render_position(logic_tick)
        cx, cy = max(self.margin, tx), max(self.margin, ty)
        cx = min(self.gameboard.size[0] - self.margin - 1, cx)
        cy = min(self.gameboard.size[1] - self.margin - 1, cy)

        top_left = floor(cx - self.margin), floor(cy - self.margin)
        bottom_right = ceil(cx + self.margin), ceil(cy + self.margin)
        return top_left, bottom_right
