import os
import pygame
import pygame_menu
import importlib.resources

from hybrid_cc.game.gameboard import Gameboard
from hybrid_cc.levelset.dat_conversions.dat_converter import DATConverter


class PygameMenuDemo:
    def __init__(self, package):
        # Initialize pygame and set up the screen
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((800, 600))
        self.package_dir = importlib.resources.files(package)
        self.level_set = None
        self.gameboard = None

    def show_loading(self):
        # Display loading screen
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render('Loading...', True,
                           (255, 255, 255))  # White text
        text_rect = text.get_rect(center=(400, 300))  # Center the text
        self.screen.blit(text, text_rect)
        pygame.display.flip()  # Update the display

    def get_levelset_files(self):
        resources = self.package_dir.iterdir()
        return [f for f in resources if f.suffix.lower() == '.dat']

    def show_levelset_menu(self):
        def on_select(file_path):
            self.show_loading()
            self.level_set = DATConverter.convert_levelset(file_path)
            self.show_level_menu()

        levelset_files = self.get_levelset_files()
        menu = pygame_menu.Menu('Load Levelset', 800, 600,
                                theme=pygame_menu.themes.THEME_DARK)

        for file in levelset_files:
            menu.add.button(file.name, on_select, file)

        menu.add.button('Exit', self.exit_game)
        menu.mainloop(self.screen)

    def show_level_menu(self):
        def on_select(_lvl):
            self.show_loading()
            self.gameboard = Gameboard(_lvl)
            print(f"built gameboard for level {_lvl.title}")

        menu = pygame_menu.Menu('Select Level', 800, 600,
                                theme=pygame_menu.themes.THEME_DARK)

        for lvl in self.level_set.levels:
            menu.add.button(lvl.title, on_select, lvl)

        menu.add.button('Back', self.show_levelset_menu)
        menu.mainloop(self.screen)

    def run(self):
        self.show_levelset_menu()

    @staticmethod
    def exit_game():
        pygame.quit()
        exit()


if __name__ == '__main__':
    package = 'hybrid_cc.sets.dat'  # Name of your package
    demo = PygameMenuDemo(package)
    demo.run()
