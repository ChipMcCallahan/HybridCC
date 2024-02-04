import importlib.resources
import pygame


class SfxPlayer:
    def __init__(self):
        self.package_dir = importlib.resources.files("hybrid_cc.sfx.effects")
        self.sounds = self.load_sounds()

    def load_sounds(self):
        """Load all sound effects from the package directory and index them by name."""
        sounds = {}
        for f in self.package_dir.iterdir():
            if f.suffix.lower() in ['.wav', '.ogg', '.mp3']:  # Supported sound formats
                sound_name = f.stem  # Use the file stem (name without suffix) as the key
                sounds[sound_name] = pygame.mixer.Sound(str(f))
        return sounds

    def play(self, name):
        """Play a sound effect by its name."""
        sound = self.sounds.get(name)
        if sound:
            sound.play()
        else:
            print(f"Sound effect '{name}' not found.")
