import time
import tkinter as tk
from itertools import cycle
from tkinter import Listbox, Canvas
from PIL import ImageTk, Image

from hybrid_cc.game.request import DestroyRequest
from hybrid_cc.shared.hashable_object import HashableObject
from hybrid_cc.shared.tag import SWIMMING, PUSHING
from hybrid_cc.gfx.gfx_provider import GfxProvider
from hybrid_cc.levelset import LevelElem
from hybrid_cc.shared import Id, Direction
from hybrid_cc.shared.button_rule import ButtonRule
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.force_rule import ForceRule
from hybrid_cc.shared.key_rule import KeyRule
from hybrid_cc.shared.monster_rule import MonsterRule
from hybrid_cc.shared.space_rule import SpaceRule
from hybrid_cc.shared.stepping_stone_rule import SteppingStoneRule
from hybrid_cc.shared.thief_rule import ThiefRule
from hybrid_cc.shared.toggle_wall_rule import ToggleWallRule
from hybrid_cc.shared.tool_rule import ToolRule
from hybrid_cc.shared.trap_rule import TrapRule
from hybrid_cc.shared.trick_wall_rule import TrickWallRule


def monster(name, d):
    id = Id.MONSTER
    rule = MonsterRule[name.upper()]
    d = Direction[d]
    return HashableObject(id=id, d=d, rule=rule)


CURRENT_STATE = "current_state"
ELIB = []
for name in ["ball", "walker", "teeth", "blob",
             "fireball", "glider", "ant", "paramecium"]:
    ELIB.append(
        [DestroyRequest(src=None, p=(0, 0, 0),
                        tgt=monster(name, d)) for d in "NESW"])


class TranimationDemo:
    def __init__(self, root):
        self.root = root
        root.title("GFX Viewer")

        # Listbox for elemids
        self.listbox = Listbox(root)
        # Calculate the width required for the longest entry
        max_width = max(len(entry) for entry in ELIB) + 5
        self.listbox.config(width=max_width)
        self.listbox.pack(side="left", fill="y")

        # Canvas for displaying images with a scrollbar
        canvas_frame = tk.Frame(root)
        canvas_frame.pack(side="right", fill="both", expand=True)

        self.canvas = Canvas(canvas_frame, width=500, height=500)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical",
                                 command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.animate_toggle = True  # Initial state of the animation toggle

        # Store the image references to prevent garbage collection
        self.image_refs = []
        self.animation_thread = None

        self.animations = {}  # Dictionary to keep track of multiple animations

        self.gfx = GfxProvider()

        index = 0
        for entry in ELIB:
            self.listbox.insert("end",f"{str(index)}")

        # Binding Listbox selection event
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        root.bind('<space>', self.toggle_animation)

    def toggle_animation(self, event=None):
        self.animate_toggle = not self.animate_toggle
        self.update_canvas(self.listbox.get(self.listbox.curselection()[0]))

    def update_canvas(self, selected_id):
        self.stop_animations()
        self.canvas.delete("all")
        self.image_refs.clear()

        elements = self.get_images(selected_id)
        x_offset, y_offset = 0, 10
        initial_y_offset = y_offset

        for i, elem in enumerate(elements):
            if isinstance(elem, list):
                if isinstance(elem[0], list):  # It's a 2D grid
                    self.display_grid(elem, x_offset, y_offset)
                    x_offset += 32 * len(elem[0])  # Increment x for next column
                    y_offset = initial_y_offset  # Reset y for new column
                else:  # It's a 1D list of images
                    if self.should_animate():
                        self.start_animation(i, elem, x_offset)
                    else:
                        # Display images vertically
                        for img in elem:
                            self.display_single_image(img, x_offset, y_offset)
                            y_offset += 32  # Increment y for next image in column
                    x_offset += 32  # Increment x for next column
                    y_offset = initial_y_offset  # Reset y for new column
            else:  # Single image
                self.display_single_image(elem, x_offset, y_offset)
                y_offset += 32  # Increment y for next image in column

            if y_offset != initial_y_offset:  # If we added images in a column
                x_offset += 32  # Increment x for next column
                y_offset = initial_y_offset  # Reset y for new column

        # Ensure canvas is updated before calculating scroll region
        self.canvas.update_idletasks()
        # Update the scroll region to encompass the new canvas size
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def display_grid(self, images, x, y):
        if isinstance(images[0], list):  # Check if it's a 2D grid
            for row in images:
                x_offset = x
                for img in row:
                    tk_img = ImageTk.PhotoImage(img)
                    self.canvas.create_image(x_offset, y, anchor="nw",
                                             image=tk_img)
                    self.image_refs.append(tk_img)
                    x_offset += 32
                y += 32  # Move to the next row
        else:  # It's a single list of images, not a 2D grid
            for img in images:
                tk_img = ImageTk.PhotoImage(img)
                self.canvas.create_image(x, y, anchor="nw", image=tk_img)
                self.image_refs.append(tk_img)
                y += 32  # Move down after each image

    def display_single_image(self, img, x, y):
        tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(x, y, anchor="nw",
                                 image=tk_img)  # Use y for vertical positioning
        self.image_refs.append(tk_img)

    def start_animation(self, anim_id, images, x):
        self.animations[anim_id] = {'images': cycle(images)}
        self.animate(anim_id, x)

    def animate(self, anim_id, x):
        if anim_id in self.animations:
            # Get the current frame
            img = next(self.animations[anim_id]['images'])

            # Create a grey background image of the same size
            bg_size = img.size
            grey_bg = Image.new('RGB', bg_size, color='grey')
            tk_grey_bg = ImageTk.PhotoImage(grey_bg)

            # First, draw the grey background
            self.canvas.create_image(x, 10, anchor="nw", image=tk_grey_bg)
            self.image_refs.append(tk_grey_bg)

            # Then, draw the animation frame
            tk_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(x, 10, anchor="nw", image=tk_img)
            self.image_refs.append(tk_img)

            # Schedule next frame update and store the task reference
            task = self.root.after(200, lambda: self.animate(anim_id, x))
            self.animations[anim_id]['task'] = task

    def run_animation(self, images, x):
        frame_duration = 1 / 5  # 1/5 of a second per frame
        for img in cycle(images):
            tk_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(x, 10, anchor="nw", image=tk_img)
            self.image_refs.append(tk_img)
            time.sleep(frame_duration)
            self.root.update()  # Update the root window for each frame

    def stop_animations(self):
        # Cancel scheduled animation tasks
        for anim_id in self.animations.keys():
            if 'task' in self.animations[anim_id]:
                self.root.after_cancel(self.animations[anim_id]['task'])
        self.animations.clear()

    def should_animate(self):
        # Now returns the state of the animate_toggle
        return self.animate_toggle

    def display_entry_over_canvas(self, entry_text):
        self.canvas.delete("entry_text")  # Remove previous text
        # Ensuring x, y coordinates and text are correctly passed
        self.canvas.create_text(
            10, 10,  # x, y coordinates
            text=entry_text,  # The text to display
            anchor="nw",  # Anchor point
            fill="white",  # Text color
            tags="entry_text"  # Tag for the text
        )

    def on_select(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.display_entry_over_canvas(value)
        self.update_canvas(value)

    def get_images(self, elib_entry):
        result = []
        for entry in ELIB[elib_entry]:
            elem, kwargs = None, {}
            if isinstance(entry, tuple):
                elem, kwargs = entry
            else:
                elem = entry
            result.append(self.gfx.provide(elem, **kwargs))

        return result


if __name__ == "__main__":
    _root = tk.Tk()
    app = TranimationDemo(_root)
    _root.mainloop()