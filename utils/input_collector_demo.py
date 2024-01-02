import pygame
from hybrid_cc.ui import InputCollector


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Input Collector")
    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    input_collector = InputCollector()

    logic_tick = 0
    movement_tick = 0
    inputs = []

    # Game loop
    running = True
    while running:
        screen.fill((0, 0, 0))  # Clear screen

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Capture key press events at 40 Hz.
        input_collector.capture_keypress_events(events)

        # Collect inputs at 10Hz (every 4th frame)
        if logic_tick % 4 == 0:
            movement_tick += 1
            inputs = input_collector.collect()

        def render(text, x, y):
            rendered = font.render(f"{text}", True, (255, 255, 255))
            screen.blit(rendered, (x, y))

        render(f"Logic tick: {logic_tick}", 50, 10)
        render(f"Movement tick: {movement_tick}", 50, 30)

        # Display inputs
        for i, key in enumerate(inputs):
            render(f"{key}", 50, 60 + i * 30)

        logic_tick += 1  # Increment frame counter

        pygame.display.flip()
        # 40 frames per second. Every 4th tick is a movement tick.
        clock.tick(40)


if __name__ == "__main__":
    main()
