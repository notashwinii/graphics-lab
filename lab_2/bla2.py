import tkinter as tk
from tkinter import ttk


def bresenham_steep_line(x1, y1, x2, y2):
    """Bresenham line algorithm implementation for slope m > 1 """
    points = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Check if line is  (m > 1)
    if dy <= dx:
        return None


def bresenham(x1, y1, x2, y2):
    """Bresenham line algorithm implementation for slope m > 1 with step tracking"""
    points = []
    steps = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    steps.append(f"Initial values: P1({x1},{y1}), P2({x2},{y2})")
    steps.append(f"dx = {dx}, dy = {dy}")

    # Check if line is actually steep (m > 1)
    if dy <= dx:
        steps.append(f"Error: dy ≤ dx ({dy} ≤ {dx}), slope ≤ 1")
        return None, steps

    slope = dy / dx if dx != 0 else float('inf')
    steps.append(f"Slope = dy/dx = {slope:.3f} > 1 (steep line)")

    # Determine direction
    x_step = 1 if x1 < x2 else -1
    y_step = 1 if y1 < y2 else -1

    steps.append(f"Direction: x_step = {x_step}, y_step = {y_step}")

    # For steep lines, we iterate over y and calculate x
    decision = 2 * dx - dy
    steps.append(f"Initial decision parameter: 2*dx - dy = {decision}")
    steps.append("--- Point Generation (Y is major axis) ---")

    x, y = x1, y1

    # Iterate over y (major axis for steep lines)
    for i in range(dy + 1):
        points.append((x, y))
        steps.append(f"Step {i}: Plot ({x},{y})")

        if decision > 0:
            x += x_step
            decision += 2 * (dx - dy)
            steps.append(f"  Decision > 0: Move diagonal, new decision = {decision}")
        else:
            decision += 2 * dx
            steps.append(f"  Decision ≤ 0: Move vertical, new decision = {decision}")

        y += y_step

    steps.append(f"Total points generated: {len(points)}")
    return points, steps


class BresenhamVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Bresenham Line Drawing (m > 1) with Algorithm Steps")
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

        # Input frame (top of left side)
        input_frame = ttk.LabelFrame(self.left_frame, text="Line Coordinates (Slope > 1)", padding="10")
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Start point
        ttk.Label(input_frame, text="Start Point - X1:").grid(row=0, column=0, padx=5)
        self.x1_var = tk.StringVar(value="100")
        ttk.Entry(input_frame, textvariable=self.x1_var, width=8).grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Y1:").grid(row=0, column=2, padx=5)
        self.y1_var = tk.StringVar(value="50")
        ttk.Entry(input_frame, textvariable=self.y1_var, width=8).grid(row=0, column=3, padx=5)

        # End point
        ttk.Label(input_frame, text="End Point - X2:").grid(row=1, column=0, padx=5, pady=(10, 0))
        self.x2_var = tk.StringVar(value="150")
        ttk.Entry(input_frame, textvariable=self.x2_var, width=8).grid(row=1, column=1, padx=5, pady=(10, 0))

        ttk.Label(input_frame, text="Y2:").grid(row=1, column=2, padx=5, pady=(10, 0))
        self.y2_var = tk.StringVar(value="300")
        ttk.Entry(input_frame, textvariable=self.y2_var, width=8).grid(row=1, column=3, padx=5, pady=(10, 0))

        # Slope display
        self.slope_var = tk.StringVar(value="Slope: -")
        ttk.Label(input_frame, textvariable=self.slope_var, font=("Arial", 10, "bold")).grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="w")

        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=(15, 0))

        ttk.Button(button_frame, text="Draw Line", command=self.draw_line).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)

        # Canvas
        self.canvas = tk.Canvas(self.left_frame, bg="white")
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # Right side
        self.right_frame = ttk.Frame(self.root, padding="10")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.rowconfigure(1, weight=1)

        # Steps title
        steps_title = ttk.Label(self.right_frame, text="Algorithm Steps",
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
            self.canvas.create_line(i, 0, i, height, fill="lightgray", tags="grid")

        # Draw horizontal lines
        for i in range(0, height, grid_size):
            self.canvas.create_line(0, i, width, i, fill="lightgray", tags="grid")

    def on_canvas_resize(self, event):
        """Handle canvas resize event"""
        self.draw_grid()

    def calculate_slope(self, x1, y1, x2, y2):
        """Calculate and return slope"""
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0:
            return float('inf') if dy != 0 else 0

        return abs(dy / dx)

    def draw_line(self):
        """Draw the Bresenham line  and show algorithm steps"""
        try:
            x1 = int(self.x1_var.get())
            y1 = int(self.y1_var.get())
            x2 = int(self.x2_var.get())
            y2 = int(self.y2_var.get())
        except ValueError:
            self.slope_var.set("Error: Invalid coordinates")
            return

        # Calculate slope
        slope = self.calculate_slope(x1, y1, x2, y2)

        # Clear previous line
        self.canvas.delete("line")

        # Get points and steps from Bresenham algorithm for steep lines
        points, steps = bresenham(x1, y1, x2, y2)

        if points is None:
            self.slope_var.set(f"Slope: {slope:.3f} (Error: m ≤ 1, need m > 1)")
            self.update_steps_panel(steps)
            return

        # Draw each pixel
        for x, y in points:
            self.canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1,
                                         fill="red", outline="red", tags="line")

        # Draw start and end points
        self.canvas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3,
                                fill="green", outline="darkgreen", tags="line")
        self.canvas.create_oval(x2 - 3, y2 - 3, x2 + 3, y2 + 3,
                                fill="blue", outline="darkblue", tags="line")

        self.slope_var.set(f"Slope: {slope:.3f} ({len(points)} points)")

        # Update steps panel
        self.update_steps_panel(steps)

    def update_steps_panel(self, steps):
        """Update the algorithm steps panel"""
        self.steps_text.delete(1.0, tk.END)

        # Add header
        header = f" Bresenham Algorithm Steps\n"
        header += "=" * 40 + "\n\n"
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
        self.slope_var.set("Slope: -")
        self.steps_text.delete(1.0, tk.END)
        self.steps_text.insert(tk.END, "Click 'Draw Line' to see algorithm steps...")


if __name__ == "__main__":
    root = tk.Tk()
    app = BresenhamVisualizer(root)
    root.mainloop()
