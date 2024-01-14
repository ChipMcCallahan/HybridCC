import pygame
from hybrid_cc.ui import InputCollector
from hybrid_cc.ui.ui_gamestate_manager import UIGamestateManager


class UIInputAndStateDemo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Input and State Demo")
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

        self.input_collector = InputCollector()

        self.logic_tick = 0
        self.movement_tick = 0
        self.inputs = []
        self.state = UIGamestateManager()

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Clear screen

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F5:
                        self.toggle_pause()
                    if event.key == pygame.K_ESCAPE:
                        self.reset()
                    if event.key == pygame.K_w:  # Win condition
                        self.state.win()
                    if event.key == pygame.K_l:  # Lose condition
                        self.state.lose()
                    if event.key in [
                            pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,
                            pygame.K_DOWN]:
                        self.state.play()
                    if event.key == pygame.K_RETURN:
                        if self.state.is_win:
                            # TODO: go to next level
                            self.reset()
                        elif self.state.is_lose:
                            self.reset()

            if self.state.is_play:
                pressed = pygame.key.get_pressed()
                self.input_collector.capture_keypress_events(events, pressed)

                # Collect inputs at 10Hz (every 4th frame)
                if self.logic_tick % 4 == 0:
                    self.movement_tick += 1
                    self.inputs = self.input_collector.collect()

                self.logic_tick += 1  # Increment frame counter

            self.render_screen()

            pygame.display.flip()
            self.clock.tick(40)

    def render_screen(self):
        if self.state.is_start:
            self.render("Ready", 350, 280)
        elif self.state.is_pause:
            self.render("Paused", 350, 280)
        elif self.state.is_play:
            self.render(f"Logic tick: {self.logic_tick}", 50, 10)
            self.render(f"Movement tick: {self.movement_tick}", 50, 30)

            # Display inputs
            for i, key in enumerate(self.inputs):
                self.render(f"{key}", 50, 60 + i * 30)
        elif self.state.is_win:
            self.render("You Win!", 350, 280)
        elif self.state.is_lose:
            self.render("You Lose!", 350, 280)

    def render(self, text, x, y, color=(255, 255, 255)):
        rendered = self.font.render(text, True, color)
        self.screen.blit(rendered, (x, y))

    def reset(self):
        self.logic_tick = 0
        self.movement_tick = 0
        self.inputs = []
        self.input_collector.reset()
        self.state.start()

    def toggle_pause(self):
        if self.state.is_pause:
            self.state.play()
        elif self.state.is_play:
            self.input_collector.reset()  # don't unpause with a movement queued
            self.state.pause()


if __name__ == "__main__":
    game = UIInputAndStateDemo()
    game.run()
