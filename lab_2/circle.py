import tkinter as tk
from tkinter import ttk


def midpoint_circle_algorithm_with_steps(xc, yc, r):
    """Mid-point Circle Drawing Algorithm with step tracking"""
    points = []
    steps = []
    x = 0
    y = r
    p = 1 - r  # Initial decision parameter

    def plot_circle_points(xc, yc, x, y):
        """Plot all 8 symmetric points of the circle"""
        return [
            (xc + x, yc + y),  # Octant 1
            (xc - x, yc + y),  # Octant 2
            (xc + x, yc - y),  # Octant 3
            (xc - x, yc - y),  # Octant 4
            (xc + y, yc + x),  # Octant 5
            (xc - y, yc + x),  # Octant 6
            (xc + y, yc - x),  # Octant 7
            (xc - y, yc - x),  # Octant 8
        ]

    steps.append(f"Initial values: x={x}, y={y}")
    steps.append(f"Initial decision parameter: p = 1 - r = 1 - {r} = {p}")
    steps.append("--- Circle Point Generation ---")

    # Plot initial points
    points.extend(plot_circle_points(xc, yc, x, y))
    steps.append(f"Step 0: Plot 8 points for ({x},{y})")

    # Generate points for one octant, others by symmetry
    step_count = 1
    while x < y:
        x += 1

        if p < 0:
            # Choose pixel (x+1, y)
            p += 2 * x + 1
            steps.append(f"Step {step_count}: p={p - 2 * x - 1:.0f} < 0, choose E pixel")
            steps.append(f"  New position: ({x},{y}), p = p + 2x + 1 = {p}")
        else:
            # Choose pixel (x+1, y-1)
            y -= 1
            p += 2 * (x - y) + 1
            steps.append(f"Step {step_count}: p≥0, choose SE pixel")
            steps.append(f"  New position: ({x},{y}), p = p + 2(x-y) + 1 = {p}")

        points.extend(plot_circle_points(xc, yc, x, y))
        steps.append(f"  Plot 8 symmetric points for ({x},{y})")
        step_count += 1

    steps.append(f"Algorithm complete: x >= y ({x} >= {y})")
    steps.append(f"Total points generated: {len(points)}")
    return points, steps


class CircleVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Mid-Point Circle Drawing Algorithm with Steps")
        self.root.geometry("1200x700")

        # Configure root grid for resizing
        self.root.columnconfigure(0, weight=3)  # Canvas area gets more space
        self.root.columnconfigure(1, weight=1)  # Steps panel gets less space
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
        input_frame = ttk.LabelFrame(self.left_frame, text="Circle Parameters", padding="10")
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Center coordinates
        ttk.Label(input_frame, text="Center X:").grid(row=0, column=0, padx=5)
        self.xc_var = tk.StringVar(value="200")
        ttk.Entry(input_frame, textvariable=self.xc_var, width=8).grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Center Y:").grid(row=0, column=2, padx=5)
        self.yc_var = tk.StringVar(value="200")
        ttk.Entry(input_frame, textvariable=self.yc_var, width=8).grid(row=0, column=3, padx=5)

        # Radius
        ttk.Label(input_frame, text="Radius:").grid(row=1, column=0, padx=5, pady=(10, 0))
        self.r_var = tk.StringVar(value="50")
        ttk.Entry(input_frame, textvariable=self.r_var, width=8).grid(row=1, column=1, padx=5, pady=(10, 0))

        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=(15, 0))

        ttk.Button(button_frame, text="Draw Circle", command=self.draw_circle).pack(side=tk.LEFT, padx=5)
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
        for x in range(0, width, grid_size):
            self.canvas.create_line(x, 0, x, height, fill="lightgray", tags="grid")

        # Draw horizontal lines
        for y in range(0, height, grid_size):
            self.canvas.create_line(0, y, width, y, fill="lightgray", tags="grid")

    def on_canvas_resize(self, event):
        """Handle canvas resize event"""
        self.draw_grid()

    def draw_circle(self):
        """Draw the circle using mid-point algorithm and show steps"""
        try:
            xc = int(self.xc_var.get())
            yc = int(self.yc_var.get())
            r = int(self.r_var.get())
        except ValueError:
            return

        # Clear previous circle
        self.canvas.delete("circle")

        # Get points and steps from mid-point circle algorithm
        points, steps = midpoint_circle_algorithm_with_steps(xc, yc, r)

        # Draw each pixel
        for x, y in points:
            self.canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1,
                                         fill="blue", outline="blue", tags="circle")

        # Draw center point
        self.canvas.create_oval(xc - 3, yc - 3, xc + 3, yc + 3,
                                fill="red", outline="darkred", tags="circle")

        # Update steps panel
        self.update_steps_panel(steps)

    def update_steps_panel(self, steps):
        """Update the algorithm steps panel"""
        self.steps_text.delete(1.0, tk.END)

        # Add header
        header = f"Mid-Point Circle Algorithm Steps\n"
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
        self.canvas.delete("circle")
        self.draw_grid()
        self.steps_text.delete(1.0, tk.END)
        self.steps_text.insert(tk.END, "Click 'Draw Circle' to see algorithm steps...")


if __name__ == "__main__":
    root = tk.Tk()
    app = CircleVisualizer(root)
    root.mainloop()
