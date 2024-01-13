import logging

from cc_tools import DATHandler

from hybrid_cc.levelset import Level, Levelset
from hybrid_cc.levelset.dat_conversions.cell_converter import CellConverter
from hybrid_cc.shared import Id
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.space_rule import SpaceRule
from hybrid_cc.shared.toggle_wall_rule import ToggleWallRule
from hybrid_cc.shared.trick_wall_rule import TrickWallRule


class DATConverter:
    @staticmethod
    def convert_levelset(dat_file_name):
        cc1_levels = DATHandler.read(dat_file_name).levels
        new_levelset = Levelset(dat_file_name)

        current_group = []

        def create_new_level_from_current_group():
            if not current_group:
                return
            level = DATConverter.convert_level(*current_group)
            new_levelset.levels.append(level)

        for cc1_level in cc1_levels:
            # Untitled levels are interpreted as z-layers on top of the
            # last titled level.
            if cc1_level.title == "":
                current_group.append(cc1_level)
            else:
                create_new_level_from_current_group()
                current_group = [cc1_level]

        # Don't forget to process the last group
        create_new_level_from_current_group()

        logging.info(f"{len(new_levelset.levels)} levels converted.")
        return new_levelset

    @staticmethod
    def convert_level(*cc1_levels):
        """
        Method to create a Level instance from a CC1 level format.
        """
        x_size, y_size, z_size = 32, 32, len(cc1_levels)
        level = Level(x_size, y_size, z_size)
        level.title = cc1_levels[0].title
        level.time = cc1_levels[0].time
        level.chips[Color.GREY] = sum(
            cc1_level.chips for cc1_level in cc1_levels)

        channels = {}
        next_trap = 1
        next_cloner = 1
        for z, cc1_level in enumerate(cc1_levels):
            for p in cc1_level.movement:
                x, y = p % 32, p // 32
                level.movement.append((x, y, z))
            for src, dst in cc1_level.traps.items():
                x1, y1 = src % 32, src // 32
                x2, y2 = dst % 32, dst // 32
                source = (x1, y1, z)
                target = (x2, y2, z)
                if target in channels:
                    channel = channels[target]
                else:
                    channel = f"T{next_trap}"
                    next_trap += 1
                channels[target] = channel
                channels[source] = channel
            for src, dst in cc1_level.cloners.items():
                x1, y1 = src % 32, src // 32
                x2, y2 = dst % 32, dst // 32
                source = (x1, y1, z)
                target = (x2, y2, z)
                if target in channels:
                    channel = channels[target]
                else:
                    channel = f"C{next_cloner}"
                    next_cloner += 1
                channels[target] = channel
                channels[source] = channel

        for i in range(x_size):
            for j in range(y_size):
                for k in range(z_size):
                    p = (i, j, k)
                    cc1_cell = cc1_levels[k].at(j * 32 + i)
                    cell = CellConverter.convert(cc1_cell,
                                                 channels.get(p, None))
                    if (cell.pickup and cell.pickup.id == Id.CHIP
                            and cell.pickup.color):
                        level.chips[cell.pickup.color] = level.chips.get(
                            cell.pickup.color, 0) + 1
                    if cell.terrain.id == Id.SPACE and k > 0:
                        below = level.get((i, j, k - 1))
                        if below.contains(Id.MONSTER):
                            cell.terrain.rule = SpaceRule.DEADLY_BELOW
                        elif below.contains_any(Id.DIRT_BLOCK, Id.ICE_BLOCK):
                            cell.terrain.rule = SpaceRule.SOLID_BELOW
                        elif below.contains(Id.TOGGLE_WALL):
                            elem = below.get_elem_by_id(Id.TOGGLE_WALL)
                            if elem.rule == ToggleWallRule.STARTS_SHUT:
                                cell.terrain.rule = SpaceRule.SOLID_BELOW
                        elif below.contains(Id.TRICK_WALL):
                            elem = below.get_elem_by_id(Id.TRICK_WALL)
                            if elem.rule not in (
                                    TrickWallRule.INVISIBLE_BECOMES_WALL,
                                    TrickWallRule.PERMANENTLY_INVISIBLE):
                                cell.terrain.rule = SpaceRule.MAYBE_SOLID_BELOW

                    level.put(p, cell)
        return level
