# pylint:disable=no-member
"""
Module for managing keyboard input in Pygame applications.

This module defines the InputCollector class, which is responsible for tracking
keyboard events and maintaining a list of currently pressed keys.
"""

import pygame


class InputCollector:
    """
    A class for collecting and managing keyboard input events in Pygame.

    This class tracks the current state of specific keyboard keys (arrow keys in this case)
    and provides methods to capture and process these keypress events.

    Attributes:
        pressed_keys (list): A list of keys that are currently pressed.
        released_keys (list): A list of keys that were recently released.
    """

    def __init__(self):
        """
        Initializes the InputCollector with empty lists for pressed_keys and unpressed_keys.
        """
        self.pressed_keys = []
        self.released_keys = []

    def capture_keypress_events(self, events):
        """
        Captures keypress events from Pygame and updates the pressed and unpressed keys lists.

        Args:
            events (list): A list of Pygame events to process.
        """
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in self.key_map:
                self.pressed_keys.append(self.key_map[event.key])

            elif event.type == pygame.KEYUP and event.key in self.key_map:
                self.released_keys.append(self.key_map[event.key])

    @property
    def key_map(self):
        """
        Returns a dictionary mapping Pygame key constants to direction strings.

        Maps the arrow keys to corresponding direction strings: 'N', 'S', 'W', and 'E'.
        """
        return {
            pygame.K_UP: "N",
            pygame.K_DOWN: "S",
            pygame.K_LEFT: "W",
            pygame.K_RIGHT: "E"
        }

    def collect(self):
        """
        Processes the collected key events and returns the current state of
        pressed keys.

        This method returns a copy of the pressed keys list after removing
        any keys that have been released. It then clears the unpressed keys
        list.

        Returns:
            list: A list of currently pressed keys.
        """
        pressed_copy = self.pressed_keys.copy()
        for unpressed in self.released_keys:
            if unpressed in self.pressed_keys:
                self.pressed_keys.remove(unpressed)
        self.released_keys.clear()

        return pressed_copy
