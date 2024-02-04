import tkinter as tk
from tkinter import simpledialog

import pygame

from hybrid_cc.ui.sfx_player import SfxPlayer


class SfxDemo:
    def __init__(self, master, sound_effects_player):
        self.master = master
        self.sound_effects_player = sound_effects_player
        master.title("Sound Effects Player")

        self.listbox = tk.Listbox(master)
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        for name in sound_effects_player.sounds.keys():
            self.listbox.insert(tk.END, name)

        self.listbox.bind('<<ListboxSelect>>', self.play_selected_sfx)

    def play_selected_sfx(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            sfx_name = event.widget.get(index)
            self.sound_effects_player.play(sfx_name)

# Example usage
if __name__ == "__main__":
    pygame.mixer.init()
    root = tk.Tk()
    sfx_player = SfxPlayer()
    app = SfxDemo(root, sfx_player)
    root.mainloop()