import tkinter as tk
from tkinter import ttk


def dda_algorithm(x1, y1, x2, y2):
    """DDA algorithm implementation"""
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        return [(x1, y1)]

    x_inc = dx / steps
    y_inc = dy / steps

    points = []
    x, y = x1, y1

    for i in range(int(steps) + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc

    return points


class SimpleDDAVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("DDA Line Drawing")
        self.root.geometry("800x600")

        self.setup_ui()
        self.draw_grid()

    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Line Coordinates", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Start point
        ttk.Label(input_frame, text="Start Point - X1:").grid(row=0, column=0, padx=5)
        self.x1_var = tk.StringVar(value="50")
        ttk.Entry(input_frame, textvariable=self.x1_var, width=8).grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Y1:").grid(row=0, column=2, padx=5)
        self.y1_var = tk.StringVar(value="50")
        ttk.Entry(input_frame, textvariable=self.y1_var, width=8).grid(row=0, column=3, padx=5)

        # End point
        ttk.Label(input_frame, text="End Point - X2:").grid(row=1, column=0, padx=5, pady=(10, 0))
        self.x2_var = tk.StringVar(value="200")
        ttk.Entry(input_frame, textvariable=self.x2_var, width=8).grid(row=1, column=1, padx=5, pady=(10, 0))

        ttk.Label(input_frame, text="Y2:").grid(row=1, column=2, padx=5, pady=(10, 0))
        self.y2_var = tk.StringVar(value="150")
        ttk.Entry(input_frame, textvariable=self.y2_var, width=8).grid(row=1, column=3, padx=5, pady=(10, 0))

        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=(15, 0))

        ttk.Button(button_frame, text="Draw Line", command=self.draw_line).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)

        # Canvas
        self.canvas = tk.Canvas(main_frame, bg="white", width=700, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=10)

    def draw_grid(self):
        """Draw a simple grid"""
        width = 700
        height = 400
        grid_size = 20

        for i in range(0, width, grid_size):
            self.canvas.create_line(i, 0, i, height, fill="lightgray", width=1)

        for i in range(0, height, grid_size):
            self.canvas.create_line(0, i, width, i, fill="lightgray", width=1)

    def draw_line(self):
        """Draw the DDA line"""
        try:
            x1 = int(self.x1_var.get())
            y1 = int(self.y1_var.get())
            x2 = int(self.x2_var.get())
            y2 = int(self.y2_var.get())
        except ValueError:
            return

        # Clear previous line
        self.canvas.delete("line")

        # Get points from DDA algorithm
        points = dda_algorithm(x1, y1, x2, y2)

        # Draw each pixel
        for x, y in points:
            self.canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1,
                                         fill="blue", outline="blue", tags="line")

        # Draw start and end points
        self.canvas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3,
                                fill="green", outline="darkgreen", tags="line")
        self.canvas.create_oval(x2 - 3, y2 - 3, x2 + 3, y2 + 3,
                                fill="red", outline="darkred", tags="line")

    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas.delete("line")
        self.draw_grid()


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleDDAVisualizer(root)
    root.mainloop()
