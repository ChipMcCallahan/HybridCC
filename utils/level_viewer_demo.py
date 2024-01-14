import logging
import os
import tkinter as tk
from importlib import resources
from tkinter import filedialog, Menu
from PIL import ImageTk
import importlib.resources

from hybrid_cc.levelset.dat_conversions.dat_converter import DATConverter
from hybrid_cc.utils.level_imager import LevelImager


class CC1LevelViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.h_scroll = None
        self.v_scroll = None
        self.canvas = None
        self.sprite_set_menu = None
        self.configure(bg='black')  # Set the background color
        self.title("Level Viewer")
        self.geometry("1200x1200")  # Adjust as needed
        self.show_secrets_var = tk.BooleanVar()
        self.show_secrets_var.set(True)
        self.show_monster_order_var = tk.BooleanVar()
        self.show_monster_order_var.set(True)
        self.sprite_set_name = tk.StringVar()
        self.combobox_active = False  # Flag to track if Combobox is active

        self.menu_bar = None
        self.file_menu = None
        self.level_title_label = None
        self.level_image_label = None
        self.level_set = None
        self.current_level_index = 0
        self.level_imager = LevelImager()
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
                                       command=self.display_level)
        self.view_menu.add_checkbutton(label="Show Monster Order", onvalue=True,
                                       offvalue=False,
                                       variable=self.show_monster_order_var,
                                       command=self.display_level)
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

        if self.level_set:
            self.display_level()

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
        self.display_level()

    def toggle_monster_order(self):
        self.show_monster_order_var.set(not self.show_monster_order_var.get())
        self.display_level()

    def load_level_set(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            self.current_level_index = 0
            self.level_set = DATConverter.convert_levelset(file_path)
            self.display_level()

    def display_level(self):
        self.level_imager.set_show_secrets(self.show_secrets_var.get())
        self.level_imager.set_show_monster_order(
            self.show_monster_order_var.get())

        if self.level_set and 0 <= self.current_level_index < len(
                self.level_set.levels):
            level = self.level_set.levels[self.current_level_index]
            self.level_title_label.config(text=f"Title: {level.title}")
            level_images = self.level_imager.level_image(level)

            # TODO: handle 3D levels
            level_image = level_images[0]
            tk_image = ImageTk.PhotoImage(level_image)
            self.level_image_label.config(image=tk_image)
            self.level_image_label.image = tk_image  # Keep a reference

            # Update the scroll region to encompass the image
            self.frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def next_level(self, event):
        if self.level_set and self.current_level_index < len(
                self.level_set.levels) - 1:
            self.current_level_index += 1
            self.display_level()

    def previous_level(self, event):
        if self.level_set and self.current_level_index > 0:
            self.current_level_index -= 1
            self.display_level()

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


if __name__ == "__main__":
    # Define the logging format to include the file name, function name,
    # and line number
    log_format = '%(filename)s - %(funcName)s - Line %(lineno)d - %(message)s'

    # Set up logging to use the format defined above and output to the
    # console at the DEBUG level
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    app = CC1LevelViewer()
    app.mainloop()
