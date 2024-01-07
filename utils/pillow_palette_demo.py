import tkinter as tk
from PIL import ImageColor


class ColorPaletteApp:
    def __init__(self, root):
        self.root = root
        root.title("Color Palette")

        # Canvas for displaying color palette
        self.canvas = tk.Canvas(root, width=800, height=800,
                                scrollregion=(0, 0, 1000, 2000))
        self.canvas.pack(side="left", fill="both", expand=True)

        # Adding a scrollbar
        scrollbar = tk.Scrollbar(root, command=self.canvas.yview)
        scrollbar.pack(side="left", fill="y")
        self.canvas.config(yscrollcommand=scrollbar.set)

        # Display colors
        self.display_colors()

    def display_colors(self):
        color_names = list(ImageColor.colormap.keys())
        x, y = 10, 10
        width, height = 150, 60  # Adjusted for better fit
        for i, name in enumerate(color_names):
            # Convert RGB to hex format
            rgb_val = ImageColor.getcolor(name, "RGB")
            hex_val = "#{:02x}{:02x}{:02x}".format(rgb_val[0], rgb_val[1],
                                                   rgb_val[2])

            self.canvas.create_rectangle(x, y, x + width, y + height,
                                         fill=hex_val, outline="black")
            # Adjust text position and size
            self.canvas.create_text(x + width / 2, y + height / 2,
                                    text=f"{name}\n{hex_val}", anchor="center",
                                    font=("Arial", 8))

            x += width + 10
            if (
                    i + 1) % 5 == 0:  # Adjust the number of colors per row to 5 for better visibility
                x = 10
                y += height + 20  # Increase spacing between rows


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPaletteApp(root)
    root.mainloop()
