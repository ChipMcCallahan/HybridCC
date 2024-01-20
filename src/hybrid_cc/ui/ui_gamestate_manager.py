import importlib.resources

import pygame

from hybrid_cc.levelset.dat_conversions.dat_converter import DATConverter
from hybrid_cc.ui import InputCollector
from hybrid_cc.ui.ui_gamestate import UIGamestate


class UIGamestateManager:
    def __init__(self):
        self.logic_tick = 0
        self.movement_tick = 0
        self.inputs = []
        self.input_collector = InputCollector()
        self.state = UIGamestate()

        self.package = 'hybrid_cc.sets.dat'
        self.package_dir = importlib.resources.files(self.package)
        self.level_index = 0
        self.level_set = DATConverter.convert_levelset(
            self.package_dir / "CCLP1.dat")

    def do_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    self.toggle_pause()
                if event.key == pygame.K_ESCAPE:
                    if self.state.load():
                        pass
                    elif self.state.select():
                        pass
                    elif self.state.start():
                        self.reset()
                if event.key == pygame.K_w:  # Simulate Win condition
                    self.state.win()
                if event.key == pygame.K_l:  # Simulate Loss condition
                    self.state.lose()
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT,
                                 pygame.K_UP, pygame.K_DOWN]:
                    self.state.play()
                if event.key == pygame.K_RETURN:
                    if (self.state.is_play or self.state.is_pause or
                            self.state.is_start):
                        continue
                    elif self.state.start():
                        self.reset()
                    elif self.state.select():
                        pass
                    elif self.state.is_win and self.state.start():
                        # TODO: go to next level
                        self.reset()
                    elif self.state.is_lose and self.state.start():
                        self.reset()

        if self.state.is_play:
            pressed = pygame.key.get_pressed()
            self.input_collector.capture_keypress_events(events, pressed)

            # Collect inputs at 10Hz (every 4th frame)
            if self.logic_tick % 4 == 0:
                self.movement_tick += 1
                self.inputs = self.input_collector.collect()

            self.logic_tick += 1  # Increment frame counter
        return True

    def reset(self):
        self.logic_tick = 0
        self.movement_tick = 0
        self.inputs = []
        self.input_collector.reset()

    def toggle_pause(self):
        if self.state.is_pause:
            self.state.play()
        elif self.state.is_play:
            self.input_collector.reset()  # don't unpause with a movement queued
            self.state.pause()

    @property
    def is_start(self):
        return self.state.is_start

    @property
    def is_pause(self):
        return self.state.is_pause

    @property
    def is_play(self):
        return self.state.is_play

    @property
    def is_win(self):
        return self.state.is_win

    @property
    def is_lose(self):
        return self.state.is_lose

    @property
    def is_select(self):
        return self.state.is_select

    @property
    def is_load(self):
        return self.state.is_load
