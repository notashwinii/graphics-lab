import tkinter as tk
from tkinter import ttk


def dda_algorithm_with_steps(x1, y1, x2, y2):
    """DDA algorithm implementation """
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    step_log = []
    step_log.append(f"Initial values: P1({x1},{y1}), P2({x2},{y2})")
    step_log.append(f"dx = {dx}, dy = {dy}")
    step_log.append(f"Steps = max(|dx|, |dy|) = {steps}")

    if steps == 0:
        step_log.append("No steps needed - single point")
        return [(x1, y1)], step_log

    x_inc = dx / steps
    y_inc = dy / steps

    step_log.append(f"x_increment = dx/steps = {x_inc:.3f}")
    step_log.append(f"y_increment = dy/steps = {y_inc:.3f}")
    step_log.append("--- Point Generation ---")

    points = []
    x, y = x1, y1

    for i in range(int(steps) + 1):
        rounded_x, rounded_y = round(x), round(y)
        points.append((rounded_x, rounded_y))

        if i < 10:  # Show first 10 steps in detail
            step_log.append(f"Step {i}: x={x:.2f}, y={y:.2f} → ({rounded_x},{rounded_y})")
        elif i == 10:
            step_log.append("... (remaining steps)")

        x += x_inc
        y += y_inc

    step_log.append(f"Total points generated: {len(points)}")
    return points, step_log


class DDAVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("DDA Line Drawing with Algorithm Steps")
        self.root.geometry("1200x700")

        # Configure root grid for resizing
        self.root.columnconfigure(0, weight=3)  # Canvas area
        self.root.columnconfigure(1, weight=1)  # Steps panel
        self.root.rowconfigure(0, weight=1)

        self.setup_ui()
        self.draw_grid()

    def setup_ui(self):
        """Setup the user interface"""
        # Left side - Canvas area
        self.left_frame = ttk.Frame(self.root, padding="10")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(1, weight=1)

        # Input frame
        input_frame = ttk.LabelFrame(self.left_frame, text="Line Coordinates", padding="10")
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

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

        # Canvas (resizable)
        self.canvas = tk.Canvas(self.left_frame, bg="white")
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # Right side - Algorithm steps panel
        self.right_frame = ttk.Frame(self.root, padding="10")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.rowconfigure(1, weight=1)

        # Steps title
        steps_title = ttk.Label(self.right_frame, text="DDA Algorithm Steps",
                                font=("Arial", 12, "bold"))
        steps_title.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Steps text area with scrollbar
        steps_frame = ttk.Frame(self.right_frame)
        steps_frame.grid(row=1, column=0, sticky="nsew")
        steps_frame.columnconfigure(0, weight=1)
        steps_frame.rowconfigure(0, weight=1)

        self.steps_text = tk.Text(steps_frame, wrap=tk.WORD, font=("Courier", 9))
        scrollbar = ttk.Scrollbar(steps_frame, orient="vertical", command=self.steps_text.yview)
        self.steps_text.configure(yscrollcommand=scrollbar.set)

        self.steps_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def draw_grid(self):
        """Draw a resizable grid"""
        self.canvas.delete("grid")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1:  # Canvas not yet rendered
            return

        grid_size = 20

        # Draw vertical lines
        for i in range(0, width, grid_size):
            self.canvas.create_line(i, 0, i, height, fill="lightgray", width=1, tags="grid")

        # Draw horizontal lines
        for i in range(0, height, grid_size):
            self.canvas.create_line(0, i, width, i, fill="lightgray", width=1, tags="grid")

    def on_canvas_resize(self, event):
        """Handle canvas resize event"""
        self.draw_grid()

    def draw_line(self):
        """Draw the DDA line and show algorithm steps"""
        try:
            x1 = int(self.x1_var.get())
            y1 = int(self.y1_var.get())
            x2 = int(self.x2_var.get())
            y2 = int(self.y2_var.get())
        except ValueError:
            return

        # Clear previous line
        self.canvas.delete("line")

        # Get points and steps from DDA algorithm
        points, steps = dda_algorithm_with_steps(x1, y1, x2, y2)

        # Draw each pixel
        for x, y in points:
            self.canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1,
                                         fill="blue", outline="blue", tags="line")

        # Draw start and end points
        self.canvas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3,
                                fill="green", outline="darkgreen", tags="line")
        self.canvas.create_oval(x2 - 3, y2 - 3, x2 + 3, y2 + 3,
                                fill="red", outline="darkred", tags="line")

        # Update steps panel
        self.update_steps_panel(steps)

    def update_steps_panel(self, steps):
        """Update the algorithm steps panel"""
        self.steps_text.delete(1.0, tk.END)

        # Add header
        header = f"DDA Line Algorithm Steps\n"
        header += "=" * 30 + "\n\n"
        self.steps_text.insert(tk.END, header)

        # Add each step
        for step in steps:
            if step.startswith("---"):
                self.steps_text.insert(tk.END, f"\n{step}\n")
            else:
                self.steps_text.insert(tk.END, f"{step}\n")

        # Scroll to top
        self.steps_text.see(1.0)

    def clear_canvas(self):
        """Clear the canvas and steps"""
        self.canvas.delete("line")
        self.draw_grid()
        self.steps_text.delete(1.0, tk.END)
        self.steps_text.insert(tk.END, "Click 'Draw Line' to see DDA algorithm steps...")


if __name__ == "__main__":
    root = tk.Tk()
    app = DDAVisualizer(root)
    root.mainloop()
