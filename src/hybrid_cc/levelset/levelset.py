from cc_tools import DATHandler

from hybrid_cc.levelset.level import Level


class Levelset:
    def __init__(self):
        self.levels = []

    @staticmethod
    def load_from_dat(dat_file_name):
        cc1_levels = DATHandler.read(dat_file_name).levels
        new_levelset = Levelset()
        current_group = []

        def create_new_level_from_current_group():
            new_levelset.levels.append(
                Level.create_from_cc1_levels(*current_group))

        for cc1_level in cc1_levels:
            if cc1_level.title == "":
                current_group.append(cc1_level)
            else:
                create_new_level_from_current_group()
                current_group = [cc1_level]

        # Don't forget to process the last group
        create_new_level_from_current_group()
