import pygame


def right(d):
    return "NESW"[("NESW".index(d) + 1) % 4]


def reverse(d):
    return "NESW"[("NESW".index(d) + 2) % 4]


def left(d):
    return "NESW"[("NESW".index(d) + 3) % 4]


class InputCollector:
    def __init__(self):
        self.pressed_keys = []
        self.keys_since_last_read = []

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in self.key_map:
                self.pressed_keys.append(self.key_map[event.key])
                self.keys_since_last_read.append(self.key_map[event.key])

            elif event.type == pygame.KEYUP and event.key in self.key_map:
                self.pressed_keys.remove(self.key_map[event.key])

    @property
    def key_map(self):
        return {
            pygame.K_UP: "N",
            pygame.K_DOWN: "S",
            pygame.K_LEFT: "W",
            pygame.K_RIGHT: "E"
        }

    # Note that due to keyboard ghosting this only returns 2 directions even
    # if all 4 are pressed.
    def get_pressed_keys(self):
        # Start with currently pressed keys. Append any keys that were pressed
        # and released since last read. This ensures we collect all key taps.
        pressed = self.pressed_keys.copy()
        for k in self.keys_since_last_read:
            if k not in pressed:
                pressed.append(k)

        self.keys_since_last_read.clear()
        # Optionally, add logic to sort 'pressed' based on the order in
        # 'self.active_keys'
        return pressed


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

        input_collector.update(events)

        # Update inputs at 10Hz (every 4th frame)
        if logic_tick % 4 == 0:
            movement_tick += 1
            inputs = input_collector.get_pressed_keys()

        # Display inputs
        for i, key in enumerate(inputs):
            text = font.render(f"{key}", True, (255, 255, 255))
            screen.blit(text, (50, 50 + i * 30))

        logic_tick += 1  # Increment frame counter

        pygame.display.flip()
        # 40 frames per second. Every 4th tick is a movement tick.
        clock.tick(40)


if __name__ == "__main__":
    main()
