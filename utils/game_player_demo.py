import importlib.resources
import logging
import os

import pygame
import pygame_menu

from hybrid_cc.gfx.pygame_gfx_provider import PygameGfxProvider
from hybrid_cc.ui.music_player import MusicPlayer
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
        self.font = pygame.font.Font(None, 24)
        self.clock = pygame.time.Clock()
        self.state_mgr = UIGamestateManager()
        self.package_dir = importlib.resources.files("hybrid_cc.sets.dat")
        self.gfx = PygameGfxProvider()
        self.music_player = MusicPlayer()
        self.music_player.start(menu=True)

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
        def on_select(i):
            self.show_loading()
            self.state_mgr.set_level(i)
            self.run_events()

        menu = pygame_menu.Menu('Select Level', 800, 600,
                                theme=BLACK_THEME,
                                onclose=pygame_menu.events.BACK)

        for i, lvl in enumerate(self.state_mgr.level_set.levels):
            menu.add.button(f"{i+1}: {lvl.title}", on_select, i)

        menu.add.button('Back', self.show_levelset_menu)
        menu.mainloop(self.screen)

    def run_events(self):
        self.music_player.stop()
        self.music_player.start(menu=False)
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Clear screen
            running = self.state_mgr.do_events()
            self.render_screen()

            pygame.display.flip()
            hz = 2 * HZ if pygame.key.get_pressed()[pygame.K_LSHIFT] else HZ
            hz = 10000 * HZ if pygame.key.get_pressed()[pygame.K_F2] else hz
            self.clock.tick(hz)
        self.music_player.stop()
        self.music_player.start(menu=True)

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

    @staticmethod
    def render_centered_subsurface(surface, subsurface, y):
        w, h = surface.get_size()
        sw, sh = subsurface.get_size()
        surface.blit(subsurface, ((w - sw) / 2, y))

    def render_screen(self):
        if self.state_mgr.is_start:
            self.render_view_extras()
            self.render_viewport()
            self.blit_centered_rect(self.screen, (400, 96))
            self.render_centered_text(self.screen,
                                      self.state_mgr.gameboard.title)
        elif self.state_mgr.is_pause:
            self.render_centered_text(self.screen, "Paused")
            self.render_centered_text_bottom(
                "Resume with Enter, Spacebar, F5, or any arrow key."
            )
        elif self.state_mgr.is_play or self.state_mgr.is_replay:
            self.render_view_extras()
            self.render_viewport()
            if self.state_mgr.is_replay:
                self.render_centered_text_bottom("Replay active.\n"
                                                 "Press arrow keys to take over"
                                                 " at any time.")
        elif self.state_mgr.is_win:
            r = self.state_mgr.gameboard.result
            msg = (
                f"Level: {self.state_mgr.level.title}\n \n"
                f"{r.color.name} Exit at position: {r.p}.\n"
                f"Time Elapsed: {r.tick / 10} Seconds.\n"
                f"Score: {r.score}")
            self.render_viewport("Excellent!")
            self.render_centered_text_top(msg)

            base_menu = (
                "[Enter] to continue to next level.\n"
                "[Esc] to retry this level.\n"
                "[F6] to retry with replay assist.\n"
            )
            appx = (
                "[S] to save the replay."
                if not self.state_mgr.saved_replay
                else f"[Replay saved to {self.state_mgr.saved_replay}]"
            )

            self.render_centered_text_bottom(
                base_menu + appx
            )
        elif self.state_mgr.is_lose:
            r = self.state_mgr.gameboard.result
            msg = (
                f"Level: {self.state_mgr.level.title}\n"
                f"Cause of Death: {r.cause}.\n"
                f"Position: {r.p}.\n"
                f"Time Elapsed: {r.tick / 10} Seconds.")
            self.render_viewport("Bummer!")
            self.render_centered_text_top(msg)
            base_menu = (
                "[Enter] or [Esc] to retry this level.\n"
                "[F6] to retry with replay assist.\n"
            )
            appx = (
                "[S] to save the replay."
                if not self.state_mgr.saved_replay
                else f"[Replay saved to {self.state_mgr.saved_replay}]"
            )
            self.render_centered_text_bottom(base_menu + appx)

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

    def render_centered_text_top(self, text):
        surface = pygame.Surface((288, 120))
        self.render_centered_wrapped_text(surface, text, self.font,
                                          (255, 255, 255))
        self.render_centered_subsurface(self.screen, surface, 18)

    def render_centered_text_bottom(self, text):
        surface = pygame.Surface((600, 120))
        self.render_centered_wrapped_text(surface, text, self.font,
                                          (255, 255, 255))
        self.render_centered_subsurface(self.screen, surface, 444 + 18)

    def render_view_extras(self):
        self.render_centered_text_top(self.state_mgr.level.title)

        self.render_text(f"Time Remaining: "
                         f"{self.state_mgr.gameboard.time_remaining()}", 10,
                         10)
        self.render_text(f"Chips Remaining", 10, 50)
        y_index = 70
        for color, count in self.state_mgr.gameboard.chips_remaining().items():
            flicker = (self.state_mgr.movement_tick // 8) % 2
            text = (f"{count}" if count > 0 or flicker else "")
            self.render_text(text, 10, y_index, color.value)
            y_index += 20

        tools = self.gfx.provide_tools()
        keys = self.gfx.provide_keys()

        margin = 8

        if tools:
            self.render_centered_subsurface(self.screen, tools,
                                            444 + 2 * margin)
        if keys:
            self.render_centered_subsurface(self.screen, keys,
                                            444 + 2 * margin + 32 + margin)

        if self.state_mgr.gameboard.show_hint:
            surface = pygame.Surface((228, 288))
            text = self.state_mgr.gameboard.hint
            self.render_centered_wrapped_text(surface, text, self.font,
                                              (255, 255, 255))
            self.screen.blit(surface, (544 + 16, 156))

    @staticmethod
    def render_centered_wrapped_text(surface, text, font, color):
        def wrap_text(_text, _font, max_width):
            paragraphs = _text.split('\n')  # Split by newline characters
            wrapped_lines = []

            for paragraph in paragraphs:
                if not paragraph:
                    wrapped_lines.append("")  # Ensure blank lines are respected
                    continue
                words = paragraph.split()
                line_words = []
                while words:
                    # Check if adding the next word exceeds max_width
                    if (_font.size(' '.join(line_words + [words[0]]))[
                            0] <= max_width):
                        line_words.append(words.pop(0))
                    else:
                        # If the line is not empty, wrap it before adding a
                        # large word
                        if line_words:
                            wrapped_lines.append(' '.join(line_words))
                            line_words = []
                        # If the line is empty and a single word is too wide,
                        # add the word to the line and force a wrap
                        else:
                            line_words.append(words.pop(0))
                            wrapped_lines.append(' '.join(line_words))
                            line_words = []  # Reset for the next line
                # Add the last line if it has any words
                if line_words:
                    wrapped_lines.append(' '.join(line_words))

            return wrapped_lines

        lines = wrap_text(text, font, surface.get_width())
        total_height = sum(font.size(line)[1] for line in lines)
        y = (surface.get_height() - total_height) // 2

        for line in lines:
            if line:  # Skip rendering for empty lines (purely newlines)
                line_surface = font.render(line, True, color)
                line_width, line_height = line_surface.get_size()
                x = (surface.get_width() - line_width) // 2
                surface.blit(line_surface, (x, y))
                y += line_height  # Move to the next line position, even for
                # empty lines

    def render_viewport(self, centered_text=None):
        # viewport_size = 11  # will clip this to 9x9
        # cx, cy, cz = self.state_mgr.gameboard.camera.position
        # margin = viewport_size // 2
        # top_left_position = (cx - margin, cy - margin, cz)
        nw, se = self.state_mgr.gameboard.camera.get_tile_bounds(
            self.state_mgr.logic_tick)

        terrain = {}
        terrain_mod = {}
        pickup = {}
        mob = {}
        sides = {}
        for i in range(nw[0], se[0] + 1):
            for j in range(nw[1], se[1] + 1):
                p = (i, j, 0)
                cell = self.state_mgr.gameboard.get((i, j, 0))
                if cell.terrain:
                    terrain[p] = cell.terrain
                if cell.terrain_mod:
                    terrain_mod[p] = cell.terrain_mod
                if cell.pickup:
                    pickup[p] = cell.pickup
                if cell.mob:
                    mob[p] = cell.mob
                if cell.get_sides():
                    sides_list = cell.get_sides()
                    if p not in sides:
                        sides[p] = []
                    for elem in sides_list:
                        sides[p].append(elem)

        viewport = self.gfx.provide_viewport((terrain, terrain_mod,
                                              pickup, mob, sides),
                                             self.state_mgr.logic_tick,
                                             nw, se,
                                             self.state_mgr.gameboard.camera)
        if centered_text:
            self.blit_centered_rect(viewport, (320 - 32, 96))
            self.render_centered_text(viewport, centered_text)

        self.screen.blit(viewport, (400 - (32 * 9) / 2,
                                    300 - (32 * 9) / 2))


if __name__ == "__main__":
    # Define the logging format to include the file name, function name,
    # and line number
    log_format = '%(filename)s - %(funcName)s - Line %(lineno)d - %(message)s'

    # Set up logging to use the format defined above and output to the
    # console at the DEBUG level
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    game = GamePlayerDemo()
    game.run()
