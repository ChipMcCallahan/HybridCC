import importlib.resources
import logging

import pygame
import random


#  TODO: Credit the game music
#
class MusicPlayer:
    def __init__(self):
        self.menu_track = None
        self.package_dir = importlib.resources.files("hybrid_cc.sfx.music")
        self.tracks = []
        self.current_track = None
        self.load_tracks()

    def load_tracks(self):
        """Load all music tracks from the package directory."""
        self.tracks = []
        for f in self.package_dir.iterdir():
            if f.suffix.lower() in ['.mp3', '.ogg']:
                if "easy_cheesy" in f.name:
                    self.menu_track = f
                else:
                    self.tracks.append(f)

    def start(self, menu=False):
        """Start playing music tracks randomly."""
        if not self.tracks:
            print("No tracks found in the package directory.")
            return

        if not pygame.mixer.music.get_busy():
            if menu and self.menu_track:
                self.play_menu_track()
            else:
                self.play_random_track()

    def play_random_track(self):
        """Select a random track to play."""
        self.current_track = random.choice(self.tracks)
        pygame.mixer.music.load(str(self.current_track))
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(
            pygame.USEREVENT)  # Set an event for when the music ends
        self.log_current()

    def play_menu_track(self):
        """Play the menu track."""
        self.current_track = self.menu_track
        pygame.mixer.music.load(str(self.menu_track))
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(
            pygame.USEREVENT)  # Set an event for when the music ends
        self.log_current()

    def log_current(self):
        logging.info(f"Playing {self.current_track}")

    @staticmethod
    def stop():
        """Stop the music playback."""
        pygame.mixer.music.stop()

    def update(self):
        """Check if the current track has finished and start a new one."""
        for event in pygame.event.get(pygame.USEREVENT):
            if event.type == pygame.USEREVENT:
                self.play_random_track()
