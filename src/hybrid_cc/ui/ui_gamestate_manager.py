import importlib.resources
from pathlib import Path

import pygame

from hybrid_cc.game.gameboard import Gameboard
from hybrid_cc.levelset.dat_conversions.dat_converter import DATConverter
from hybrid_cc.replays.replay import Replay
from hybrid_cc.ui import InputCollector
from hybrid_cc.ui.ui_gamestate import UIGamestate


class UIGamestateManager:
    def __init__(self):
        self.replay = None
        self.level_index = None
        self.logic_tick = 0
        self.movement_tick = 0
        self.inputs = []
        self.input_collector = InputCollector()
        self.state = UIGamestate()
        self.gameboard = None
        self.level_set = None
        self.level = None
        self.saved_replay = ""
        self.package_dir = importlib.resources.files(
            "hybrid_cc.json.official_replays")
        self.reset()

    def do_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F5:
                    self.toggle_pause()
                if event.key == pygame.K_ESCAPE:
                    if self.state.start():
                        self.reset()
                    elif self.is_start:
                        return False
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT,
                                 pygame.K_UP, pygame.K_DOWN]:
                    self.state.play()
                if event.key == pygame.K_n:
                    self.next_level()
                if event.key == pygame.K_p:
                    self.previous_level()
                if event.key == pygame.K_s:
                    if not self.saved_replay and (
                            self.state.is_win or self.state.is_lose):
                        directory = self.get_default_save_path()

                        setname = self.level_set.name
                        title = self.gameboard.title
                        lvlnum = self.level_index + 1
                        fname = f"{setname}-{lvlnum}-{title}.json"

                        self.saved_replay = self.gameboard.replay.save_to_file(
                            directory, self.level.title, fname)
                if event.key == pygame.K_l and self.state.is_start:
                    self.get_replay()
                    if self.replay:
                        self.reset(self.replay.seed)
                        self.state.replay()

                if event.key == pygame.K_F9:
                    self.state.lose()

                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if self.state.is_play or self.state.is_replay:
                        continue
                    elif self.state.is_pause or self.state.is_start:
                        self.state.play()
                    elif self.state.is_win:
                        self.next_level()
                    elif self.state.start():
                        self.reset()
                if event.key == pygame.K_F6:
                    if self.state.replay():
                        self.replay = self.gameboard.replay
                        self.reset(self.replay.seed)
        if self.state.is_play or self.state.is_replay:
            pressed = pygame.key.get_pressed()

            # Collect inputs on every logic tick EXCEPT for the first one
            # after a movement tick. Tradeoff between missing a move and
            # over-moving which happens a lot without this check.
            if self.logic_tick % 4 != 1:
                self.input_collector.capture_keypress_events(events, pressed)

            # Collect inputs at 10Hz (every 4th frame)
            if self.logic_tick % 4 == 0:
                self.movement_tick += 1
                self.inputs = self.input_collector.collect()

                if self.state.is_replay:
                    if self.inputs:
                        self.state.play()
                    else:
                        replay_input = self.replay.get(self.movement_tick)
                        self.inputs = replay_input.dirs()

                self.gameboard.do_logic(self.inputs)
                if self.gameboard.state == Gameboard.State.WIN:
                    self.state.win()
                elif self.gameboard.state == Gameboard.State.LOSE:
                    self.state.lose()
            self.logic_tick += 1  # Increment frame counter
        elif self.state.is_win or self.state.is_lose:
            self.logic_tick += 1  # Keep the animation going
        return True

    def reset(self, seed=None):
        self.logic_tick = 0
        self.movement_tick = 0
        self.inputs = []
        self.input_collector.reset()
        self.setup_gameboard(seed)
        self.saved_replay = ""

    def toggle_pause(self):
        if self.state.is_pause:
            self.state.play()
        elif self.state.is_play:
            self.input_collector.reset()  # don't unpause with a movement queued
            self.state.pause()

    def load_set(self, file_path):
        self.level_set = DATConverter.convert_levelset(file_path)

    def setup_gameboard(self, seed=None):
        if self.level:
            self.gameboard = Gameboard(self.level, seed)

    def set_level(self, i):
        self.level_index = i
        self.level = self.level_set.levels[i]
        self.reset()

    def next_level(self):
        i = (self.level_index + 1) % len(self.level_set.levels)
        self.set_level(i)
        self.state.start()

    def previous_level(self):
        i = (self.level_index - 1) % len(self.level_set.levels)
        self.set_level(i)
        self.state.start()

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
    def is_replay(self):
        return self.state.is_replay

    @property
    def is_win(self):
        return self.state.is_win

    @property
    def is_lose(self):
        return self.state.is_lose

    @staticmethod
    def get_default_save_path():
        home_dir = Path.home()
        save_dir = home_dir / "hybridcc_replays"
        save_dir.mkdir(exist_ok=True)  # Create if not there
        return save_dir

    def get_replay(self):
        resources = self.package_dir.iterdir()
        setname = str(self.level_set.name).split(".")[0]
        title = f"{setname}-{self.level_index + 1}-{self.level.title}.json"
        for resource in resources:
            if str(resource.name) == title:
                self.replay = Replay.load_from_file(resource)
                return
        self.replay = None
