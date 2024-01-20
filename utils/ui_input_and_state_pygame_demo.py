import pygame
from hybrid_cc.ui.ui_gamestate_manager import UIGamestateManager


class UIInputAndStateDemo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Input and State Demo")
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        self.state = UIGamestateManager()

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Clear screen
            running = self.state.do_events()
            self.render_screen()

            pygame.display.flip()
            self.clock.tick(40)

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
        elif self.state.is_load:
            self.render_centered("Load Levelset", 280)
        elif self.state.is_select:
            self.render_centered("Select Level", 280)

    def render(self, text, x, y, color=(255, 255, 255)):
        rendered = self.font.render(text, True, color)
        self.screen.blit(rendered, (x, y))


if __name__ == "__main__":
    game = UIInputAndStateDemo()
    game.run()
