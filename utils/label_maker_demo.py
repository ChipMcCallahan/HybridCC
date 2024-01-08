import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from hybrid_cc.gfx.label_maker import LabelMaker


class LabelMakerDemo:
    def __init__(self, root):
        self.count = 0
        self.root = root
        root.title("LabelMaker Demo")

        # Defaults
        default_text_color = "yellow"
        default_bg_color = "black"
        default_position = 5
        default_label_text = "128"

        # Left side - Inputs
        left_frame = tk.Frame(root)
        left_frame.pack(side="left", fill="y")

        # Text color dropdown
        tk.Label(left_frame, text="Text Color:").pack()
        self.text_color_var = tk.StringVar(value=default_text_color)
        text_color_dropdown = ttk.Combobox(left_frame,
                                           textvariable=self.text_color_var,
                                           values=["red", "green", "blue",
                                                   "white", "black"])
        text_color_dropdown.pack()
        text_color_dropdown.bind("<<ComboboxSelected>>", self.update_label)

        # Background color dropdown
        tk.Label(left_frame, text="Background Color:").pack()
        self.bg_color_var = tk.StringVar(value=default_bg_color)
        bg_color_dropdown = ttk.Combobox(left_frame,
                                         textvariable=self.bg_color_var,
                                         values=["red", "green", "blue",
                                                 "white", "black"])
        bg_color_dropdown.pack()
        bg_color_dropdown.bind("<<ComboboxSelected>>", self.update_label)

        # Position input box
        tk.Label(left_frame, text="Position (1-9):").pack()
        self.position_var = tk.StringVar(value=str(default_position))
        position_entry = tk.Entry(left_frame, textvariable=self.position_var)
        position_entry.pack()
        position_entry.bind("<KeyRelease>", self.update_label)

        # Label text input box
        tk.Label(left_frame, text="Label Text:").pack()
        self.label_text_var = tk.StringVar(value=default_label_text)
        label_text_entry = tk.Entry(left_frame,
                                    textvariable=self.label_text_var)
        label_text_entry.pack()
        label_text_entry.bind("<KeyRelease>", self.update_label)

        # Right side - Output image
        self.image_label = tk.Label(root)
        self.image_label.pack(side="right", fill="both", expand=True)

        # Initialize LabelMaker
        self.label_maker = LabelMaker(text_color=default_text_color,
                                      bg_color=default_bg_color,
                                      position=default_position
                                      )

        # Generate initial label
        self.update_label()

    def update_label(self, event=None):
        # Update LabelMaker attributes
        self.label_maker.text_color = self.text_color_var.get()
        self.label_maker.bg_color = self.bg_color_var.get()
        self.label_maker.position = int(self.position_var.get())

        # Generate and display the label
        label_image = self.label_maker.make(self.label_text_var.get())
        self.count += 1

        tk_image = ImageTk.PhotoImage(label_image)
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image  # Keep a reference

        # Create a scaled-up version of the label
        scaled_size = (label_image.width * 4, label_image.height * 4)
        scaled_image = label_image.resize(scaled_size, Image.NEAREST)
        scaled_tk_image = ImageTk.PhotoImage(scaled_image)

        # Check if the second image label exists, else create it
        if hasattr(self, 'scaled_image_label'):
            self.scaled_image_label.configure(image=scaled_tk_image)
        else:
            self.scaled_image_label = tk.Label(self.root,
                                               image=scaled_tk_image)
            self.scaled_image_label.pack(side="right", fill="both",
                                         expand=True)

        # Update the reference to the scaled image to prevent garbage collection
        self.scaled_image_label.image = scaled_tk_image


if __name__ == "__main__":
    root = tk.Tk()
    app = LabelMakerDemo(root)
    root.mainloop()
