import logging
import tkinter as tk
from importlib import resources
from tkinter import filedialog, Menu
from PIL import ImageTk, Image
import importlib.resources

from hybrid_cc.game.elements.elem import Elem
from hybrid_cc.game.gameboard import Gameboard
from hybrid_cc.gfx.gfx_provider import GfxProvider
from hybrid_cc.gfx.sprite_assembly.utils.labeler import Labeler
from hybrid_cc.gfx.sprite_assembly.utils.stacker import Stacker
from hybrid_cc.levelset.dat_conversions.dat_converter import DATConverter


class GameboardInspectorDemo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.gameboard = None
        self.cropped_image_label = None
        self.original_level_image = None
        self.tk_image = None
        self.cropped_img_ref = None
        self.tile_label = None
        self.h_scroll = None
        self.v_scroll = None
        self.canvas = None
        self.sprite_set_menu = None
        self.configure(bg='black')  # Set the background color
        self.title("Gameboard Inspector Demo")
        self.geometry("1200x1200")  # Adjust as needed
        self.show_secrets_var = tk.BooleanVar()
        self.show_secrets_var.set(True)
        self.show_monster_order_var = tk.BooleanVar()
        self.show_monster_order_var.set(True)
        self.sprite_set_name = tk.StringVar()
        self.combobox_active = False  # Flag to track if Combobox is active

        self.selected_tile = None  # To keep track of the selection rectangle
        self.tile_label = None  # Label to display the tile position
        self.menu_bar = None
        self.file_menu = None
        self.level_title_label = None
        self.level_image_label = None
        self.level_set = None
        self.current_level_index = 0
        self.gameboard_imager = GameboardImager()
        self.view_menu = None

        self.package = 'hybrid_cc.sets.dat'
        self.package_dir = importlib.resources.files(self.package)
        file_path = self.package_dir / "CCLP1.dat"

        if file_path:
            self.level_set = DATConverter.convert_levelset(file_path)

        self.init_ui()

    def init_ui(self):
        # Menu for opening level sets
        self.menu_bar = Menu(self)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open Level Set",
                                   command=self.load_level_set)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.config(menu=self.menu_bar)

        # Adding a View menu with a Toggle Secrets checkbutton
        self.view_menu = Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_checkbutton(label="Show Secrets", onvalue=True,
                                       offvalue=False,
                                       variable=self.show_secrets_var,
                                       command=self.display_gameboard)
        self.view_menu.add_checkbutton(label="Show Monster Order", onvalue=True,
                                       offvalue=False,
                                       variable=self.show_monster_order_var,
                                       command=self.display_gameboard)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        # Labels for level title and image
        self.level_title_label = tk.Label(self, text="")
        self.level_title_label.pack()
        # Create a canvas and scrollbars for the image
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.v_scroll = tk.Scrollbar(self, orient="vertical",
                                     command=self.canvas.yview)
        self.h_scroll = tk.Scrollbar(self, orient="horizontal",
                                     command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set,
                              xscrollcommand=self.h_scroll.set)

        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        # This frame will hold the image label
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.level_image_label = tk.Label(self.frame)
        self.level_image_label.pack()

        self.tile_label = tk.Label(self, text="")
        self.tile_label.pack()

        # Label for displaying cropped image
        self.cropped_image_label = tk.Label(self, borderwidth=2, relief="solid")
        self.cropped_image_label.pack(side="right", padx=10)

        self.bind("<Left>", self.previous_level)
        self.bind("<Right>", self.next_level)
        self.bind('s', lambda event: self.toggle_secrets())
        self.bind('m', lambda event: self.toggle_monster_order())
        self.bind("<Escape>", self.clear_focus)

        # Bind the mousewheel/trackpad scrolling to the canvas
        self.canvas.bind_all("<MouseWheel>",
                             self.on_mousewheel)  # For Windows vertical scroll
        self.canvas.bind_all("<Shift-MouseWheel>",
                             self.on_horizontal_scroll)  # For Windows horizontal scroll
        self.canvas.bind_all("<Button-4>",
                             self.on_mousewheel)  # For Linux vertical scroll
        self.canvas.bind_all("<Button-5>",
                             self.on_mousewheel)  # For Linux vertical scroll
        self.canvas.bind_all("<Shift-Button-4>",
                             self.on_horizontal_scroll)  # For Linux horizontal scroll
        self.canvas.bind_all("<Shift-Button-5>",
                             self.on_horizontal_scroll)  # For Linux horizontal scroll
        self.bind_all("<2>", self.on_mousewheel)
        self.canvas.bind("<Button-1>",
                         self.on_canvas_click)  # Bind left mouse click

        if self.level_set:
            self.display_gameboard()

    def clear_focus(self, event=None):
        """
        Clear focus from all widgets. This will ensure that the Combobox
        loses focus when Escape is pressed or when clicking elsewhere in the window.
        """
        self.focus_set()

    def set_combobox_active(self, active):
        self.combobox_active = active

    def toggle_secrets(self):
        self.show_secrets_var.set(not self.show_secrets_var.get())
        self.display_gameboard()

    def toggle_monster_order(self):
        self.show_monster_order_var.set(not self.show_monster_order_var.get())
        self.display_gameboard()

    def load_level_set(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            self.current_level_index = 0
            self.level_set = DATConverter.convert_levelset(file_path)
            self.display_gameboard()

    def display_gameboard(self):
        self.gameboard_imager.set_show_secrets(self.show_secrets_var.get())
        self.gameboard_imager.set_show_monster_order(
            self.show_monster_order_var.get())

        if self.level_set and 0 <= self.current_level_index < len(
                self.level_set.levels):
            gameboard = Gameboard(
                self.level_set.levels[self.current_level_index])
            self.log_elem_stats()
            self.gameboard = gameboard
            self.level_title_label.config(text=f"Title: {gameboard.title}")
            level_images = self.gameboard_imager.gameboard_image(gameboard)

            # Handle 3D levels if needed
            self.original_level_image = level_images[
                0]  # Keep a reference to the original PIL image
            self.tk_image = ImageTk.PhotoImage(self.original_level_image)
            self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def next_level(self, event):
        if self.level_set and self.current_level_index < len(
                self.level_set.levels) - 1:
            self.current_level_index += 1
            self.display_gameboard()

    def previous_level(self, event):
        if self.level_set and self.current_level_index > 0:
            self.current_level_index -= 1
            self.display_gameboard()

    def on_mousewheel(self, event):
        # Determine the scrolling direction and amount
        if event.num == 5 or event.delta > 0:
            scroll = -1
        elif event.num == 4 or event.delta < 0:
            scroll = 1
        else:
            return  # Do nothing for other events

        # Adjust the scrolling for MacOS or Linux if needed
        if event.num in (4, 5):
            scroll *= 3  # Increase scroll amount for Linux

        # Perform the scrolling
        self.canvas.yview_scroll(scroll, "units")

    def on_horizontal_scroll(self, event):
        # Determine the scrolling direction and amount for horizontal scroll
        scroll = -1 if event.delta > 0 else 1

        # Adjust the scrolling amount for Linux if needed
        if event.num in (4, 5):
            scroll *= 3  # Increase scroll amount for Linux

        # Perform the horizontal scrolling
        self.canvas.xview_scroll(scroll, "units")

    def log_tile_stats(self, x, y):
        print(f"Position ({x}, {y}).")
        elems = self.gameboard.get((x, y, 0)).all()
        for elem in elems:
            print(elem.lookup_key)

    def log_elem_stats(self):
        instances = Elem.instances.items()
        print(f"found {len(instances)} instances")

    def on_canvas_click(self, event):
        # Get the scroll fractions
        xview_frac, _ = self.canvas.xview()
        yview_frac, _ = self.canvas.yview()

        # Get the total scrollable size of the canvas
        scrollable_width = self.canvas.bbox("all")[2]
        scrollable_height = self.canvas.bbox("all")[3]

        # Calculate the actual position on the canvas, accounting for the scroll
        canvas_x = int((event.x + (scrollable_width * xview_frac)) // 32) * 32
        canvas_y = int((event.y + (scrollable_height * yview_frac)) // 32) * 32

        # Adjust these if needed based on the image position
        # (if the image does not start at (0,0) of the canvas)
        self.highlight_tile(canvas_x, canvas_y)
        self.update_info_panel(canvas_x, canvas_y)
        self.log_tile_stats(canvas_x // 32, canvas_y // 32)

    def highlight_tile(self, tile_x, tile_y):
        # Delete previous selection rectangle
        if self.selected_tile:
            self.canvas.delete(self.selected_tile)

        # Draw a new red rectangle around the selected tile
        self.selected_tile = self.canvas.create_rectangle(
            tile_x, tile_y, tile_x + 32, tile_y + 32,
            outline='red', width=2
        )

    def update_info_panel(self, tile_x, tile_y):
        # Update the tile information
        self.tile_label.config(
            text=f"Selected Tile: ({tile_x // 32}, {tile_y // 32})")

        # Calculate the bounds for cropping the selected tile
        crop_bounds = (tile_x, tile_y, tile_x + 32, tile_y + 32)

        # Crop the selected tile from the original image
        cropped_img = self.original_level_image.crop(crop_bounds)
        cropped_img = ImageTk.PhotoImage(cropped_img)

        # Display the cropped image in the new label
        self.cropped_image_label.config(image=cropped_img)

        # Keep a reference to the cropped image to avoid garbage collection
        self.cropped_img_ref = cropped_img


class GameboardImager:
    """Class that creates level images"""

    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.show_secrets = None
        self.set_show_secrets(True)
        self.show_monster_order = None
        self.set_show_monster_order(True)
        self.gfx_provider = GfxProvider()
        self.labeler = Labeler()
        self.stacker = Stacker()
        # TODO: draw arrows on cloner blocks

    def set_show_secrets(self, show_secrets):
        """Set the show_secrets boolean on self and CC1SpriteSet."""
        self.show_secrets = show_secrets

    def set_show_monster_order(self, show_monster_order):
        """Set the show_monster_order boolean."""
        self.show_monster_order = show_monster_order

    def gameboard_image(self, gameboard):
        """Create a PNG image from a Gameboard."""
        images = []
        x, y, z = gameboard.size
        for k in range(z):
            images.append(Image.new("RGBA", (32 * x, 32 * y)))

            for j in range(y):
                for i in range(x):
                    p = (i, j, k)
                    cell = gameboard.get(p)

                    elems = [e for e in [
                        cell.terrain, cell.terrain_mod, cell.pickup,
                        cell.mob] + list(cell.sides.values()) if e is not None]
                    kwargs = {"show_secrets": self.show_secrets}
                    for elem in elems:
                        if isinstance(elem, tuple):
                            print(elem, p)
                    tile_images = [
                        self.gfx_provider.provide_one(elem, **kwargs)
                        for elem in elems]
                    tile_img = self.stacker.stack(*tile_images)

                    if (self.show_monster_order and
                            p in gameboard.move_handler.movement):
                        index = str(gameboard.move_handler.movement.index(p))
                        tile_img = self.stacker.stack(tile_img,
                                                      self.labeler.label(index,
                                                                         1))

                    images[k].paste(tile_img, (i * 32, j * 32), tile_img)
        return images


if __name__ == "__main__":
    # Define the logging format to include the file name, function name,
    # and line number
    log_format = '%(filename)s - %(funcName)s - Line %(lineno)d - %(message)s'

    # Set up logging to use the format defined above and output to the
    # console at the DEBUG level
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    app = GameboardInspectorDemo()
    app.mainloop()
