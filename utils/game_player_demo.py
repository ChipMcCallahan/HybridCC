import importlib.resources
import logging
import os

import pygame
import pygame_menu

from hybrid_cc.gfx.pygame_gfx_provider import PygameGfxProvider
from hybrid_cc.ui.ui_gamestate_manager import UIGamestateManager

BLACK_THEME = pygame_menu.themes.THEME_DARK.copy()
BLACK_THEME.background_color = (0, 0, 0)
HZ = 40  # 40 IS NORMAL, 80 IS 2x

class GamePlayerDemo:
    def __init__(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Game Player Demo")
        self.font = pygame.font.Font(None, 20)
        self.clock = pygame.time.Clock()
        self.state_mgr = UIGamestateManager()
        self.package_dir = importlib.resources.files("hybrid_cc.sets.dat")
        self.gfx = PygameGfxProvider()

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
            self.state_mgr.load_set(file_path)
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
            self.state_mgr.set_level(_lvl)
            self.run_events()

        menu = pygame_menu.Menu('Select Level', 800, 600,
                                theme=BLACK_THEME)

        for lvl in self.state_mgr.level_set.levels:
            menu.add.button(lvl.title, on_select, lvl)

        menu.add.button('Back', self.show_levelset_menu)
        menu.mainloop(self.screen)

    def run_events(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Clear screen
            running = self.state_mgr.do_events()
            self.render_screen()

            pygame.display.flip()
            self.clock.tick(HZ)

    def run(self):
        self.show_levelset_menu()

    @staticmethod
    def exit_game():
        pygame.quit()
        exit()

    def render_text(self, text, x, y, color=(255, 255, 255)):
        rendered = self.font.render(text, True, color)
        self.screen.blit(rendered, (x, y))

    def render_centered_text(self, surface, text, color=(255, 255, 255)):
        # Render the text to a surface
        text_surface = self.font.render(text, True, color)

        # Calculate x and y positions to center the text on the given surface
        surface_width, surface_height = surface.get_size()
        text_width, text_height = text_surface.get_size()
        x = (surface_width - text_width) // 2
        y = (surface_height - text_height) // 2

        # Blit the text surface at the calculated position onto the provided
        # surface
        surface.blit(text_surface, (x, y))

    def render_screen(self):
        if self.state_mgr.is_start:
            self.render_viewport(self.state_mgr.gameboard.title)
        elif self.state_mgr.is_pause:
            self.render_centered_text(self.screen, "Paused")
        elif self.state_mgr.is_play:
            self.render_text(f"Time Remaining: "
                             f"{self.state_mgr.gameboard.time_remaining()}", 50, 10)
            self.render_viewport()
        elif self.state_mgr.is_win:
            self.render_viewport("You Win!")
        elif self.state_mgr.is_lose:
            self.render_viewport("You Lose!")

    @staticmethod
    def blit_centered_rect(surface, rect_size, opacity=128,
                           color=(128, 128, 128)):
        # Create a new surface for the rectangle with per-pixel alpha
        rect_surface = pygame.Surface(rect_size, pygame.SRCALPHA)

        # Fill the surface with the grey color and set the desired opacity
        rect_surface.fill((*color, opacity))

        # Calculate the position to center the rectangle on the given surface
        surface_width, surface_height = surface.get_size()
        rect_width, rect_height = rect_size
        x = (surface_width - rect_width) // 2
        y = (surface_height - rect_height) // 2

        # Blit the rectangle surface onto the provided surface at the
        # calculated position
        surface.blit(rect_surface, (x, y))

    def render_viewport(self, centered_text=None):
        viewport_size = 11  # will clip this to 9x9
        cx, cy, cz = self.state_mgr.gameboard.viewport_center(viewport_size)
        margin = viewport_size // 2

        terrain = {}
        terrain_mod = {}
        pickup = {}
        mob = {}
        sides = {}
        for i in range(cx - margin, cx + margin + 1):
            for j in range(cy - margin, cy + margin + 1):
                # relative x & y to viewport
                x, y = i - cx + margin, j - cy + margin
                cell = self.state_mgr.gameboard.get((i, j, cz))
                if cell.terrain:
                    terrain[(x, y)] = cell.terrain
                if cell.terrain_mod:
                    terrain_mod[(x, y)] = cell.terrain_mod
                if cell.pickup:
                    pickup[(x, y)] = cell.pickup
                if cell.mob:
                    mob[(x, y)] = cell.mob
                if cell.get_sides():
                    sides[(x, y)] = cell.get_sides()

        viewport = self.gfx.provide_viewport(viewport_size,
                                             (terrain, terrain_mod,
                                              pickup, mob, sides),
                                             self.state_mgr.logic_tick)
        if centered_text:
            self.blit_centered_rect(viewport, (320 - 32, 96))
            self.render_centered_text(viewport, centered_text)
        self.screen.blit(viewport, (240, 140))


if __name__ == "__main__":
    # Define the logging format to include the file name, function name,
    # and line number
    log_format = '%(filename)s - %(funcName)s - Line %(lineno)d - %(message)s'

    # Set up logging to use the format defined above and output to the
    # console at the DEBUG level
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    game = GamePlayerDemo()
    game.run()
