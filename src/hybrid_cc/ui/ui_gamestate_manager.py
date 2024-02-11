import importlib.resources
import sys
from pathlib import Path

import pygame

from hybrid_cc.game.elements.instances.button import Button
from hybrid_cc.game.elements.instances.force import Force
from hybrid_cc.game.elements.instances.ice import Ice
from hybrid_cc.game.elements.instances.player import Player
from hybrid_cc.game.elements.instances.teleport import Teleport
from hybrid_cc.game.elements.tool import Tool
from hybrid_cc.game.gameboard import Gameboard
from hybrid_cc.game.request import DestroyRequest, CreateRequest, LoseRequest, \
    WinRequest, UIInteractionRequest
from hybrid_cc.levelset.dat_conversions.dat_converter import DATConverter
from hybrid_cc.replays.replay import Replay
from hybrid_cc.shared import Id
from hybrid_cc.shared.bomb_rule import BombRule
from hybrid_cc.ui import InputCollector
from hybrid_cc.ui.sfx_player import SfxPlayer
from hybrid_cc.ui.ui_gamestate import UIGamestate
from hybrid_cc.ui.ui_hints import UIHints

KEY_MAP = {
    pygame.K_UP: "N",
    pygame.K_DOWN: "S",
    pygame.K_LEFT: "W",
    pygame.K_RIGHT: "E"
}


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
        self.package_json = importlib.resources.files(
            "hybrid_cc.solutions.official")
        self.package_tws = importlib.resources.files(
            "hybrid_cc.solutions.parsed_tws")
        self.sfx_player = SfxPlayer()
        self.reset()

    def do_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
                        fname = f"{setname}-{lvlnum}-{title}"

                        self.saved_replay = self.gameboard.replay.save_to_file(
                            directory, self.level.title, fname)
                if event.key == pygame.K_l and self.state.is_start:
                    self.get_replay()
                    if self.replay:
                        self.reset(self.replay.seed)
                        self.state.replay()
                if event.key == pygame.K_q and self.state.is_start:
                    self.get_replay("ms_tws")
                    if self.replay:
                        self.reset(self.replay.seed)
                        self.state.replay()
                if event.key == pygame.K_w and self.state.is_start:
                    self.get_replay("lynx_tws")
                    if self.replay:
                        self.reset(self.replay.seed)
                        self.state.replay()

                if event.key == pygame.K_F9:
                    self.gameboard.lose(cause="QUIT", p=Player.instance.p)

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
                elif event.key == pygame.K_z:
                    # DEBUG: this fast forwards to 2.5 seconds prior to death
                    if self.state.replay() and self.gameboard.replay.last_tick:
                        self.replay = self.gameboard.replay
                        self.reset(self.replay.seed)
                        end_tick = max(0, self.replay.last_tick - 20)
                        for tick in range(1, end_tick):
                            inputs = self.replay.get(tick)
                            self.gameboard.do_logic(inputs.dirs())
                            self.logic_tick += 4
                            self.movement_tick += 1
        if self.state.is_play or self.state.is_replay:
            subtick = self.logic_tick % 4

            pressed = pygame.key.get_pressed()
            self.input_collector.capture(
                [KEY_MAP[k] for k in KEY_MAP if pressed[k]])

            # Collect inputs at 10Hz (every 4th frame)
            if subtick == 0:
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

            sounds = set()
            for ui_hint in UIHints.pending:
                if isinstance(ui_hint, DestroyRequest):
                    src, tgt, p = ui_hint.src, ui_hint.tgt, ui_hint.p
                    if tgt.id == Id.BOMB:
                        key = (tgt.color, tgt.channel)
                        index = [BombRule.STARTS_ARMED,
                                 BombRule.STARTS_DISARMED].index(
                            tgt.rule)
                        current_state = Button.signal[key]
                        is_armed = (index + current_state) % 2 == 0
                        if is_armed:
                            sounds.add("bomb")
                        else:
                            sounds.add("whisk")
                    elif tgt.id == Id.CHIP:
                        sounds.add("MSCLICK3")
                    elif tgt.id == Id.KEY or isinstance(tgt, Tool):
                        if src.id == Id.PLAYER:
                            sounds.add("MSBLIP2")
                        else:
                            sounds.add("whisk")
                    elif Id.WATER in (src.id, tgt.id):
                        sounds.add("splash")
                    elif tgt.id == Id.DOOR:
                        sounds.add("MSDOOR")
                    elif tgt.id == Id.DIRT:
                        sounds.add("whisk")
                    elif tgt.id == Id.SOCKET:
                        sounds.add("door")
                    elif tgt.id in (
                            Id.POP_UP_WALL, Id.STEPPING_STONE, Id.TRICK_WALL):
                        sounds.add("bump")
                elif isinstance(ui_hint, CreateRequest):
                    p, id = ui_hint.p, ui_hint.id
                    if id == Id.WALL:
                        sounds.add("popup")
                elif isinstance(ui_hint, LoseRequest):
                    sounds.add("MSBUMMER")
                elif isinstance(ui_hint, WinRequest):
                    sounds.add("tada")
                elif isinstance(ui_hint, UIInteractionRequest):
                    src, tgt, p, type = (
                        ui_hint.src, ui_hint.tgt, ui_hint.p, ui_hint.type)
                    if tgt.id == Id.FIRE:
                        sounds.add("crackle")
                    elif tgt.id == Id.WATER:
                        sounds.add("plip")
                    elif tgt is Ice or tgt.id == Id.ICE:
                        if type == "slide":
                            sounds.add("skate")
                        else:
                            sounds.add("snick")
                    elif tgt is Force or tgt.id == Id.FORCE:
                        if type == "slide":
                            sounds.add("force")
                        else:
                            sounds.add("snick")
                    elif tgt.id == Id.BUTTON:
                        sounds.add("MSPOP2")
                    elif tgt is Teleport or tgt.id == Id.TELEPORT:
                        sounds.add("MSTELEPORT")
                    elif tgt.id == Id.DIRT_BLOCK:
                        sounds.add("block")
                    elif tgt.id == Id.ICE_BLOCK:
                        sounds.add("skate")
                    elif tgt.id == Id.THIEF:
                        sounds.add("MSSTRIKE")
            for sound in sounds:
                self.sfx_player.play(sound)
            UIHints.pending.clear()
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

    def get_replay(self, mode="test"):
        setname = str(self.level_set.name).split(".")[0]
        title = f"{setname}-{self.level_index + 1}-{self.level.title}"
        if mode == "test":
            resources = self.package_json.iterdir()
        else:
            resources = self.package_tws.iterdir()
            title += "-MS" if mode == "ms_tws" else "-LYNX"

        title = Replay.sanitize_filename(title)
        for resource in resources:
            if str(resource.name).startswith(title):
                self.replay = Replay.load_from_file(resource)
                return
        self.replay = None
