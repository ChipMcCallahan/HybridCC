import time
import tkinter as tk
from itertools import cycle
from tkinter import Listbox, Canvas
from PIL import ImageTk

from hybrid_cc.gfx.gfx_provider import GfxProvider
from hybrid_cc.levelset import Elem
from hybrid_cc.shared import Id
from hybrid_cc.shared.color import Color
from hybrid_cc.shared.trick_wall_rule import TrickWallRule


class GfxViewerApp:
    def __init__(self, root):
        self.root = root
        root.title("GFX Viewer")

        # Listbox for elemids
        self.listbox = Listbox(root)
        self.listbox.pack(side="left", fill="y")

        # Canvas for displaying images with a scrollbar
        canvas_frame = tk.Frame(root)
        canvas_frame.pack(side="right", fill="both", expand=True)

        self.canvas = Canvas(canvas_frame, width=500, height=500)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=scrollbar.set)


        self.animate_toggle = True  # Initial state of the animation toggle

        # Store the image references to prevent garbage collection
        self.image_refs = []
        self.animation_thread = None

        self.animations = {}  # Dictionary to keep track of multiple animations

        self.gfx = GfxProvider()

        # Hardcoded list of elemids
        elemids = [Id[n] for n in (
            "FLOOR",
            "WALL",
            "EXIT",
            "WATER",
            "FIRE",
            "TRICK_WALL"
        )]
        for elem in elemids:
            self.listbox.insert("end", elem.name)

        # Binding Listbox selection event
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        root.bind('<space>', self.toggle_animation)


    def toggle_animation(self, event=None):
        self.animate_toggle = not self.animate_toggle
        self.update_canvas(self.listbox.get(self.listbox.curselection()[0]))

    def update_canvas(self, selected_eid):
        self.canvas.delete("all")
        self.image_refs.clear()
        self.stop_animations()

        elements = self.get_images(selected_eid)
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

        # Update the scroll region to encompass the new canvas size
        self.canvas.update_idletasks()  # Ensure canvas is updated before calculating scroll region
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
        self.animations[anim_id] = cycle(images)
        self.animate(anim_id, x)

    def animate(self, anim_id, x):
        if anim_id in self.animations:
            img = next(self.animations[anim_id])
            tk_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(x, 10, anchor="nw", image=tk_img)
            self.image_refs.append(tk_img)
            self.root.after(200, lambda: self.animate(anim_id, x))  # Schedule next frame update

    def run_animation(self, images, x):
        frame_duration = 1 / 5  # 1/5 of a second per frame
        for img in cycle(images):
            tk_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(x, 10, anchor="nw", image=tk_img)
            self.image_refs.append(tk_img)
            time.sleep(frame_duration)
            self.root.update()  # Update the root window for each frame

    def stop_animations(self):
        self.animations.clear()

    def should_animate(self):
        # Now returns the state of the animate_toggle
        return self.animate_toggle

    def on_select(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.update_canvas(value)

    def get_images(self, elemid_str):
        images = []
        elemid = Id[elemid_str]
        if elemid == Id.FLOOR:
            for color in Color:
                floor = Elem(elemid, color=color)
                images.append(self.gfx.floor(floor))
        elif elemid == Id.WALL:
            for color in Color:
                wall = Elem(elemid, color=color)
                images.append(self.gfx.wall(wall))
        elif elemid == Id.EXIT:
            for color in Color:
                if color == Color.GREY:
                    continue
                exit = Elem(elemid, color=color)
                images.append(self.gfx.exit(exit))
        elif elemid == Id.WATER:
            images.append(self.gfx.water())
        elif elemid == Id.FIRE:
            images.append(self.gfx.fire())
        elif elemid == Id.TRICK_WALL:
            for rule in TrickWallRule:
                subimages = []
                for color in Color:
                    elem = Elem(elemid, rule=rule, color=color)
                    subimages.append(self.gfx.trick_wall(elem))
                images.append(subimages)
        return images


if __name__ == "__main__":
    _root = tk.Tk()
    app = GfxViewerApp(_root)
    _root.mainloop()
