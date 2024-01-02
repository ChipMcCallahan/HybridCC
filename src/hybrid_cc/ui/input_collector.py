#pylint:disable=no-member
"""
Module for collecting and managing keyboard inputs in a Pygame application.

This module contains the InputCollector class, which is designed to track
keyboard inputs, specifically arrow key presses, and maintain a record of
keys pressed and released within a specified time frame.
"""

import pygame


class InputCollector:
    """
    A class to collect and manage keyboard inputs in a Pygame application.

    This class tracks the state of arrow keys (up, down, left, right) and
    provides an updated list of pressed keys, taking into account rapid key
    taps that might occur between input reads.

    Attributes:
        pressed_keys (list): A list of keys that are currently pressed down.
        keys_since_last_read (list): A list of keys pressed and released since
                                     the last input read.

    Methods:
        update(events): Updates the key states based on Pygame events.
        get_pressed_keys(): Returns a list of pressed keys.
    """
    def __init__(self):
        """
        Initializes the InputCollector with empty lists for pressed_keys and
        keys_since_last_read.
        """
        self.pressed_keys = []
        self.keys_since_last_read = []

    def capture_keypress_events(self, events):
        """
        Updates the state of pressed keys based on Pygame events. This method
        should be called more frequently than the collect() method. Its purpose
        is to track key presses in between collections.

        Args:
            events (list): A list of Pygame events to process.

        This method updates the pressed_keys list by adding or removing keys
        based on KEYDOWN and KEYUP events. It also tracks keys that are pressed
        and released rapidly in keys_since_last_read.
        """
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in self.key_map:
                self.pressed_keys.append(self.key_map[event.key])
                self.keys_since_last_read.append(self.key_map[event.key])

            elif event.type == pygame.KEYUP and event.key in self.key_map:
                self.pressed_keys.remove(self.key_map[event.key])

    @property
    def key_map(self):
        """
        Returns a dictionary mapping Pygame key constants to direction strings.

        The direction strings are "N", "S", "W", and "E" corresponding to the
        up, down, left, and right arrow keys, respectively.
        """
        return {
            pygame.K_UP: "N",
            pygame.K_DOWN: "S",
            pygame.K_LEFT: "W",
            pygame.K_RIGHT: "E"
        }

    def collect(self):
        """
        Returns a list of currently pressed keys, including those tapped
        rapidly since the last time this method was called. Note that due to
        keyboard ghosting this only returns 2 directions even if all 4 are
        pressed. This method should be called on movement ticks to collect
        inputs.

        This method returns a combined list of currently pressed keys and keys
        that were pressed and released since the last read. It ensures that
        rapid key taps are not missed.

        Returns:
            list: A list of pressed keys.
        """
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
