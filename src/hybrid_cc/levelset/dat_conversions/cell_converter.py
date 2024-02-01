import logging
from typing import Dict

from cc_tools import CC1

from hybrid_cc.levelset import LevelElem, LevelCell
from hybrid_cc.shared import Id, Direction
from hybrid_cc.shared.button_rule import ButtonRule
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.force_rule import ForceRule
from hybrid_cc.shared.key_rule import KeyRule
from hybrid_cc.shared.kwargs import RULE, COUNT, COLOR, DIRECTION, CHANNEL, \
    SIDES
from hybrid_cc.shared.monster_rule import MonsterRule
from hybrid_cc.shared.stepping_stone_rule import SteppingStoneRule
from hybrid_cc.shared.thief_rule import ThiefRule
from hybrid_cc.shared.toggle_wall_rule import ToggleWallRule
from hybrid_cc.shared.tool_rule import ToolRule
from hybrid_cc.shared.trap_rule import TrapRule
from hybrid_cc.shared.trick_wall_rule import TrickWallRule

COLOR_CODE = {
    CC1.BALL_N: Color.RED,
    CC1.BALL_E: Color.GREEN,
    CC1.BALL_S: Color.BLUE,
    CC1.BALL_W: Color.YELLOW,
    CC1.WALKER_N: Color.MAGENTA,
    CC1.WALKER_E: Color.CYAN,
    CC1.WALKER_S: Color.ORANGE,
    CC1.WALKER_W: Color.TAN,
}

NUMBER_CODE = {
    CC1.ANT_N: 2,
    CC1.ANT_E: 3,
    CC1.ANT_S: 4,
    CC1.ANT_W: 5,
    CC1.PARAMECIUM_N: 6,
    CC1.PARAMECIUM_E: 7,
    CC1.PARAMECIUM_S: 8,
    CC1.PARAMECIUM_W: 9,
    CC1.FIREBALL_N: 10,
    CC1.FIREBALL_E: 20,
    CC1.FIREBALL_S: 30,
    CC1.FIREBALL_W: 40,
    CC1.GLIDER_N: 50,
    CC1.GLIDER_E: 60,
    CC1.GLIDER_S: 70,
    CC1.GLIDER_W: 80,
}


class CellConverter:
    @staticmethod
    def colorize(bottom: CC1) -> Dict[str, any]:
        if bottom in COLOR_CODE:
            return {COLOR: COLOR_CODE[bottom]}
        return dict()

    @staticmethod
    def channelize(bottom: CC1) -> Dict[str, any]:
        if bottom in NUMBER_CODE:
            return {CHANNEL: NUMBER_CODE[bottom]}
        return dict()

    @staticmethod
    def count(bottom: CC1) -> Dict[str, any]:
        if bottom in NUMBER_CODE:
            return {COUNT: NUMBER_CODE[bottom]}
        return dict()

    @staticmethod
    def convert(cc1_cell, channel=None, conversion_rules=()):
        cell = LevelCell()

        def populate(top, bottom=CC1.FLOOR):

            if top == CC1.FLOOR:
                kwargs = CellConverter.colorize(bottom)
                cell.terrain = LevelElem(Id.FLOOR, **kwargs)

            elif top == CC1.WALL:
                kwargs = CellConverter.colorize(bottom)
                cell.terrain = LevelElem(Id.WALL, **kwargs)

            elif top == CC1.CHIP:
                kwargs = CellConverter.colorize(bottom) or CellConverter.count(
                    bottom)
                cell.pickup = LevelElem(Id.CHIP, **kwargs)
                if kwargs:
                    if "extend-color" in conversion_rules:
                        populate(CC1.FLOOR, bottom)
                    return

                if bottom in CC1.valid().difference(CC1.pickups()).difference(
                        CC1.mobs()):
                    populate(bottom)

            elif top == CC1.WATER:
                cell.terrain = LevelElem(Id.WATER)

            elif top == CC1.FIRE:
                cell.terrain = LevelElem(Id.FIRE)

            elif top == CC1.INV_WALL_PERM:
                kwargs = CellConverter.colorize(bottom)
                kwargs[RULE] = TrickWallRule.PERMANENTLY_INVISIBLE
                cell.terrain = LevelElem(Id.TRICK_WALL, **kwargs)

            elif top in CC1.panels():
                kwargs = CellConverter.colorize(bottom)
                sides = CC1.dirs(top)
                if bottom in CC1.panels():
                    sides += CC1.dirs(bottom)
                    sides = ''.join(set(sides))
                kwargs[SIDES] = sides
                cell.add_sides(LevelElem(Id.PANEL, **kwargs))
                if bottom in CC1.valid().difference(CC1.mobs()).difference(
                        CC1.panels()):
                    populate(bottom)

            elif top in CC1.blocks():
                kwargs = CellConverter.colorize(bottom)
                if top in CC1.clone_blocks():
                    kwargs[DIRECTION] = Direction[CC1.dirs(top)]
                if bottom == CC1.BLUE_WALL_REAL:
                    populate(CC1.POP_UP_WALL)
                cell.mob = LevelElem(Id.DIRT_BLOCK, **kwargs)
                if bottom in CC1.valid().difference(
                        CC1.mobs()) and bottom != CC1.BLUE_WALL_REAL:
                    populate(bottom)

            elif top == CC1.DIRT:
                kwargs = CellConverter.colorize(bottom)
                cell.terrain = LevelElem(Id.DIRT, **kwargs)

            elif top in CC1.ice():
                if top != CC1.ICE:
                    cell.add_sides(
                        LevelElem(Id.CORNER, sides=CC1.dirs(top.reverse())))
                # doubled corners yield just the corner
                if top != bottom or top == CC1.ICE:
                    cell.terrain = LevelElem(Id.ICE)

            elif top in CC1.forces():
                kwargs = CellConverter.colorize(bottom)
                if COLOR not in kwargs:
                    kwargs[COLOR] = Color.GREEN
                if top == CC1.FORCE_RANDOM:
                    kwargs[RULE] = ForceRule.RANDOM
                else:
                    kwargs[DIRECTION] = Direction[CC1.dirs(top)]
                cell.terrain = LevelElem(Id.FORCE, **kwargs)

            elif top == CC1.EXIT:
                kwargs = CellConverter.colorize(bottom)
                if COLOR not in kwargs:
                    kwargs[COLOR] = Color.BLUE
                cell.terrain = LevelElem(Id.EXIT, **kwargs)

            elif top in CC1.doors():
                kwargs = CellConverter.colorize(bottom) or CellConverter.count(
                    bottom)
                if COLOR not in kwargs:
                    kwargs[COLOR] = Color[top.name.split("_")[0]]
                cell.terrain_mod = LevelElem(Id.DOOR, **kwargs)
                if bottom in CC1.valid().difference(CC1.pickups()).difference(
                        CC1.mobs()):
                    populate(bottom)

            elif top in (CC1.BLUE_WALL_FAKE, CC1.BLUE_WALL_REAL):
                kwargs = CellConverter.colorize(bottom)
                kwargs[RULE] = (TrickWallRule.BECOMES_FLOOR
                                if top == CC1.BLUE_WALL_FAKE
                                else TrickWallRule.BECOMES_WALL)
                if bottom in CC1.keys():
                    kwargs[COLOR] = Color[bottom.name.split("_")[0]]
                    kwargs[RULE] = (TrickWallRule.PASS_THRU
                                    if top == CC1.BLUE_WALL_FAKE
                                    else TrickWallRule.SOLID)
                if COLOR not in kwargs:
                    kwargs[COLOR] = Color.BLUE
                cell.terrain = LevelElem(Id.TRICK_WALL, **kwargs)

            elif top == CC1.NOT_USED_0:
                pass

            elif top == CC1.THIEF:
                kwargs = {
                    RULE: ThiefRule.KEYS if top == bottom else ThiefRule.TOOLS
                }
                cell.terrain = LevelElem(Id.THIEF, **kwargs)

            elif top == CC1.SOCKET:
                kwargs = CellConverter.colorize(bottom)
                cell.terrain_mod = LevelElem(Id.SOCKET, **kwargs)
                if kwargs:
                    if "extend-color" in conversion_rules:
                        populate(CC1.FLOOR, bottom)
                    return
                if bottom in CC1.valid().difference(CC1.pickups()).difference(
                        CC1.mobs()):
                    populate(bottom)

            elif top in CC1.buttons():
                CellConverter.do_buttons(cell, top, bottom, channel)
                if (bottom in CC1.valid().difference(CC1.mobs())
                        .difference(CC1.pickups())
                        .difference(CC1.buttons())
                        .difference({CC1.CLONER, })):
                    populate(bottom)

            elif top in CC1.toggles():
                kwargs = CellConverter.colorize(
                    bottom) or CellConverter.channelize(bottom)
                if COLOR not in kwargs:
                    kwargs[COLOR] = Color.GREEN
                kwargs[RULE] = (ToggleWallRule.STARTS_OPEN
                                if top == CC1.TOGGLE_FLOOR
                                else ToggleWallRule.STARTS_SHUT)
                cell.terrain_mod = LevelElem(Id.TOGGLE_WALL, **kwargs)
                if bottom in CC1.valid().difference(CC1.mobs()):
                    populate(bottom)

            elif top == CC1.TELEPORT:
                kwargs = CellConverter.colorize(
                    bottom) or CellConverter.channelize(bottom)
                if COLOR not in kwargs:
                    kwargs[COLOR] = Color.BLUE
                cell.terrain = LevelElem(Id.TELEPORT, **kwargs)

            elif top == CC1.BOMB:
                kwargs = CellConverter.colorize(bottom)
                if COLOR not in kwargs:
                    kwargs[COLOR] = Color.RED
                cell.pickup = LevelElem(Id.BOMB, **kwargs)
                if bottom in CC1.valid().difference(CC1.pickups()).difference(
                        CC1.mobs()):
                    populate(bottom)

            elif top == CC1.TRAP:
                # traps that start shut
                if bottom in CC1.keys().union(CC1.doors()).union({CC1.TRAP, }):
                    kwargs = {}
                    if bottom == CC1.TRAP:
                        index = 7
                    else:
                        c = bottom.name.split("_")[0]
                        index = list(Color).index(c) + (
                            4 if type in CC1.doors() else 0)
                    kwargs[COLOR] = list(Color)[index]
                    kwargs[RULE] = TrapRule.STARTS_SHUT
                    if channel:
                        kwargs[CHANNEL] = channel

                # traps that start open
                else:
                    kwargs = (CellConverter.colorize(bottom) or
                              CellConverter.channelize(bottom))
                    kwargs[COLOR] = kwargs.get(COLOR, Color.TAN)
                    if channel:
                        kwargs[CHANNEL] = channel
                cell.terrain = LevelElem(Id.TRAP, **kwargs)

            elif top == CC1.INV_WALL_APP:
                kwargs = CellConverter.colorize(bottom)
                kwargs[RULE] = TrickWallRule.INVISIBLE_BECOMES_WALL
                cell.terrain = LevelElem(Id.TRICK_WALL, **kwargs)

            elif top == CC1.GRAVEL:
                if bottom == CC1.GRAVEL:
                    cell.terrain = LevelElem(Id.SPACE)
                else:
                    cell.terrain = LevelElem(Id.GRAVEL)

            elif top == CC1.POP_UP_WALL:
                kwargs = CellConverter.colorize(bottom) or CellConverter.count(
                    bottom)
                # If a mob starts here, make the count 2 so that it will
                # be 1 after the mob moves off. This matches Lynx and MS
                # behavior.
                if cell.mob:
                    kwargs[COUNT] = 2
                cell.terrain = LevelElem(Id.POP_UP_WALL, **kwargs)

            elif top == CC1.HINT:
                cell.terrain = LevelElem(Id.HINT)

            elif top == CC1.CLONER:
                kwargs = (CellConverter.colorize(bottom) or
                          CellConverter.channelize(bottom))
                if COLOR not in kwargs:
                    kwargs[COLOR] = Color.RED
                if channel:
                    kwargs[CHANNEL] = channel
                cell.terrain = LevelElem(Id.CLONER, **kwargs)

            elif top == CC1.DROWN_CHIP:
                kwargs = CellConverter.count(bottom)
                kwargs[RULE] = SteppingStoneRule.WATER
                cell.terrain = LevelElem(Id.STEPPING_STONE, **kwargs)

            elif top in (CC1.BURNED_CHIP0, CC1.BURNED_CHIP1):
                kwargs = CellConverter.count(bottom)
                kwargs[RULE] = SteppingStoneRule.FIRE
                cell.terrain = LevelElem(Id.STEPPING_STONE, **kwargs)

            elif top == CC1.NOT_USED_1:
                pass

            elif top == CC1.NOT_USED_2:
                pass

            elif top == CC1.NOT_USED_3:
                if bottom == CC1.BLUE_WALL_REAL:
                    populate(CC1.POP_UP_WALL)
                cell.mob = LevelElem(Id.ICE_BLOCK)
                if bottom in CC1.valid().difference(
                        CC1.mobs()) and bottom != CC1.BLUE_WALL_REAL:
                    populate(bottom)

            elif top == CC1.CHIP_EXIT:
                pass

            elif top == CC1.UNUSED_EXIT_0:
                pass

            elif top == CC1.UNUSED_EXIT_1:
                pass

            elif top == CC1.CHIP_SWIMMING_N:
                pass

            elif top == CC1.CHIP_SWIMMING_W:
                pass

            elif top == CC1.CHIP_SWIMMING_S:
                pass

            elif top == CC1.CHIP_SWIMMING_E:
                pass

            elif top in CC1.monsters().difference(CC1.tanks()):
                rule, direction = top.name.split("_")
                kwargs = {
                    RULE: MonsterRule[rule],
                    DIRECTION: Direction[direction]
                }
                cell.mob = LevelElem(Id.MONSTER, **kwargs)
                if bottom not in CC1.mobs():
                    populate(bottom)

            elif top in CC1.tanks():
                kwargs = {}
                if bottom in CC1.tanks().union(CC1.clone_blocks()):
                    # Robot (like CC2 yellow tank)
                    offset = 0
                    d = CC1.dirs(top)
                    if d == CC1.dirs(bottom.left()):
                        offset = 1
                    elif d == CC1.dirs(bottom.reverse()):
                        offset = 2
                    elif d == CC1.dirs(bottom.right()):
                        offset = 3

                    if bottom in CC1.clone_blocks():
                        offset += 4
                    kwargs[COLOR] = list(Color)[offset + 1]
                    kwargs[DIRECTION] = Direction[d]
                    cell.mob = LevelElem(Id.ROBOT, **kwargs)
                else:
                    kwargs = CellConverter.colorize(
                        bottom) or CellConverter.channelize(bottom)
                    if COLOR not in kwargs:
                        kwargs[COLOR] = Color.BLUE
                    kwargs[DIRECTION] = Direction[CC1.dirs(top)]
                    cell.mob = LevelElem(Id.TANK, **kwargs)
                    if bottom not in CC1.mobs():
                        populate(bottom)

            elif top in CC1.keys():
                kwargs = CellConverter.count(bottom)
                color = Color[top.name.split("_")[0]]
                kwargs[COLOR] = color
                if color == Color.BLUE:
                    kwargs[RULE] = KeyRule.FRAGILE
                elif color == Color.YELLOW:
                    kwargs[RULE] = KeyRule.ACTING_DIRT
                elif color == Color.GREEN:
                    kwargs[RULE] = KeyRule.ACTING_DIRT
                    kwargs[COUNT] = "+"
                if bottom in COLOR_CODE:
                    kwargs.update(CellConverter.colorize(bottom))
                elif bottom in NUMBER_CODE:
                    kwargs.update(CellConverter.count(bottom))
                cell.pickup = LevelElem(Id.KEY, **kwargs)
                if bottom not in CC1.mobs():
                    populate(bottom)

            elif top in CC1.boots():
                kwargs = {RULE: (ToolRule.ITEM_BARRIER if top == bottom
                                 else ToolRule.DEFAULT)}
                kwargs.update(CellConverter.count(bottom))
                eid = Id[top.name]
                cell.pickup = LevelElem(eid, **kwargs)
                if bottom in CC1.valid().difference(CC1.pickups()).difference(
                        CC1.mobs()):
                    populate(bottom)

            elif top in CC1.players():
                kwargs = {
                    DIRECTION: Direction[CC1.dirs(top)]
                }
                cell.mob = LevelElem(Id.PLAYER, **kwargs)
                if bottom not in CC1.mobs():
                    populate(bottom)

        populate(cc1_cell.top, cc1_cell.bottom)
        if not cell.terrain:
            cell.terrain = LevelElem(Id.FLOOR)
        return cell

    @staticmethod
    def do_buttons(cell, top, bottom, channel):
        kwargs = {}
        if top == CC1.GREEN_BUTTON:
            if bottom in COLOR_CODE:
                kwargs = CellConverter.colorize(bottom)
                kwargs[RULE] = ButtonRule.TOGGLE
            elif bottom in NUMBER_CODE:
                kwargs = CellConverter.channelize(bottom)
                kwargs[RULE] = ButtonRule.TOGGLE
            elif bottom == CC1.GREEN_BUTTON:
                kwargs[RULE] = ButtonRule.HOLD_ONE
                kwargs[COLOR] = Color.GREEN
            elif bottom == CC1.CLONE_BUTTON:
                kwargs[RULE] = ButtonRule.HOLD_ONE
                kwargs[COLOR] = Color.YELLOW
            elif bottom == CC1.CLONER:
                kwargs[RULE] = ButtonRule.DPAD
                kwargs[COLOR] = Color.GREEN
            else:
                kwargs[RULE] = ButtonRule.TOGGLE
                kwargs[COLOR] = Color.GREEN
        elif top == CC1.TANK_BUTTON:
            if bottom == top:
                kwargs[RULE] = ButtonRule.HOLD_ONE
                kwargs[COLOR] = Color.BLUE
            elif bottom == CC1.TRAP_BUTTON:
                kwargs[RULE] = ButtonRule.HOLD_ONE
                kwargs[COLOR] = Color.CYAN
            elif bottom in COLOR_CODE:
                kwargs = CellConverter.colorize(bottom)
                kwargs[RULE] = ButtonRule.HOLD_ALL
            elif bottom in NUMBER_CODE:
                kwargs = CellConverter.channelize(bottom)
                kwargs[COLOR] = Color.BLUE
                kwargs[RULE] = ButtonRule.HOLD_ALL
            elif bottom == CC1.CLONER:
                kwargs[RULE] = ButtonRule.DPAD
                kwargs[COLOR] = Color.BLUE
            else:
                kwargs[RULE] = ButtonRule.TOGGLE
                kwargs[COLOR] = Color.BLUE
        elif top == CC1.CLONE_BUTTON:
            if channel and bottom in COLOR_CODE:
                kwargs = CellConverter.colorize(bottom)
                kwargs[CHANNEL] = channel
                kwargs[RULE] = ButtonRule.TOGGLE
            elif bottom == top:
                kwargs[RULE] = ButtonRule.HOLD_ONE
                kwargs[COLOR] = Color.RED
            elif bottom in NUMBER_CODE:
                kwargs = CellConverter.channelize(bottom)
                kwargs[COLOR] = Color.RED
                kwargs[RULE] = ButtonRule.HOLD_ONE
            elif bottom == CC1.CLONER:
                kwargs[COLOR] = Color.RED
                kwargs[RULE] = ButtonRule.DPAD
            elif bottom == CC1.TANK_BUTTON:
                kwargs[COLOR] = Color.MAGENTA
                kwargs[RULE] = ButtonRule.HOLD_ONE
            else:
                kwargs[RULE] = ButtonRule.TOGGLE
                # unassigned red buttons might unintentionally
                # act as toggles for red elements, so assign otherwise
                kwargs[CHANNEL] = channel or "NONE"
                kwargs[COLOR] = Color.RED
        elif top == CC1.TRAP_BUTTON:
            if bottom == CC1.GREEN_BUTTON:
                kwargs[RULE] = ButtonRule.HOLD_ONE
                kwargs[COLOR] = Color.ORANGE
            elif bottom == top:
                kwargs[RULE] = ButtonRule.HOLD_ONE
                kwargs[COLOR] = Color.TAN
            elif channel and bottom in COLOR_CODE:
                kwargs = CellConverter.colorize(bottom)
                kwargs[RULE] = ButtonRule.HOLD_ONE
                kwargs[CHANNEL] = channel
            elif bottom == CC1.CLONER:
                kwargs[RULE] = ButtonRule.DPAD
                kwargs[COLOR] = Color.TAN
            elif bottom in NUMBER_CODE:
                kwargs = CellConverter.channelize(bottom)
                kwargs[RULE] = ButtonRule.DPAD
            else:
                kwargs[RULE] = ButtonRule.HOLD_ONE
                # unassigned tan buttons might unintentionally
                # act as toggles for tan elements, so assign otherwise
                kwargs[CHANNEL] = channel or "NONE"
                kwargs[COLOR] = Color.TAN
        cell.terrain_mod = LevelElem(Id.BUTTON, **kwargs)
