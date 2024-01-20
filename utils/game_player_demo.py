import importlib.resources
import logging
import os

import pygame
import pygame_menu

from hybrid_cc.game.gameboard import Gameboard
from hybrid_cc.levelset.dat_conversions.dat_converter import DATConverter
from hybrid_cc.ui.ui_gamestate_manager import UIGamestateManager

BLACK_THEME = pygame_menu.themes.THEME_DARK.copy()
BLACK_THEME.background_color = (0, 0, 0)


class GamePlayerDemo:
    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Input and State Demo")
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.state = UIGamestateManager()
        self.package_dir = importlib.resources.files("hybrid_cc.sets.dat")
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
                                theme=BLACK_THEME)

        for file in levelset_files:
            menu.add.button(file.name, on_select, file)

        menu.add.button('Exit', self.exit_game)
        menu.mainloop(self.screen)

    def show_level_menu(self):
        def on_select(_lvl):
            self.show_loading()
            self.gameboard = Gameboard(_lvl)
            self.run_events()


        menu = pygame_menu.Menu('Select Level', 800, 600,
                                theme=BLACK_THEME)

        for lvl in self.level_set.levels:
            menu.add.button(lvl.title, on_select, lvl)

        menu.add.button('Back', self.show_levelset_menu)
        menu.mainloop(self.screen)

    def run_events(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Clear screen
            running = self.state.do_events()
            self.render_screen()

            pygame.display.flip()
            self.clock.tick(40)

    def run(self):
        self.show_levelset_menu()

    @staticmethod
    def exit_game():
        pygame.quit()
        exit()

    def render_centered(self, text, y, color=(255, 255, 255)):
        # Render the text to a surface
        text_surface = self.font.render(text, True, color)

        # Calculate x position to center the text
        screen_width = self.screen.get_width()
        text_width = text_surface.get_width()
        x = (screen_width - text_width) // 2

        # Blit the text surface at the calculated position
        self.screen.blit(text_surface, (x, y))

    def render_screen(self):
        if self.state.is_start:
            self.render_centered("Ready", 280)
        elif self.state.is_pause:
            self.render_centered("Paused", 280)
        elif self.state.is_play:
            self.render(f"Logic tick: {self.state.logic_tick}", 50, 10)
            self.render(f"Movement tick: {self.state.movement_tick}", 50, 30)

            # Display inputs
            for i, key in enumerate(self.state.inputs):
                self.render(f"{key}", 50, 60 + i * 30)
        elif self.state.is_win:
            self.render_centered("You Win!", 280)
        elif self.state.is_lose:
            self.render_centered("You Lose!", 280)

    def render(self, text, x, y, color=(255, 255, 255)):
        rendered = self.font.render(text, True, color)
        self.screen.blit(rendered, (x, y))


if __name__ == "__main__":
    # Define the logging format to include the file name, function name,
    # and line number
    log_format = '%(filename)s - %(funcName)s - Line %(lineno)d - %(message)s'

    # Set up logging to use the format defined above and output to the
    # console at the DEBUG level
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    game = GamePlayerDemo()
    game.run()
