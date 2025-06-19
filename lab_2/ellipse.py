import tkinter as tk
from tkinter import ttk


def midpoint_ellipse_algorithm_with_steps(xc, yc, rx, ry):
    """Mid-point Ellipse Drawing Algorithm with step tracking"""
    points = []
    steps = []

    def plot_ellipse_points(xc, yc, x, y):
        """Plot all 4 symmetric points of the ellipse"""
        return [
            (xc + x, yc + y),  # Quadrant 1
            (xc - x, yc + y),  # Quadrant 2
            (xc + x, yc - y),  # Quadrant 3
            (xc - x, yc - y),  # Quadrant 4
        ]

    # Region 1: where slope < -1
    x = 0
    y = ry
    rx2 = rx * rx
    ry2 = ry * ry

    # Initial decision parameter for region 1
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)

    steps.append(f"Initial values: x={x}, y={y}")
    steps.append(f"rx²={rx2}, ry²={ry2}")
    steps.append(f"Initial p1={p1:.2f}")
    steps.append("--- REGION 1 (slope < -1) ---")

    # Plot initial points
    points.extend(plot_ellipse_points(xc, yc, x, y))

    # Region 1: Continue while slope < -1
    while (2 * ry2 * x) < (2 * rx2 * y):
        x += 1

        if p1 < 0:
            # Choose pixel (x+1, y)
            p1 += 2 * ry2 * x + ry2
            steps.append(f"Step {x}: p1<0, choose (x+1,y) → ({x},{y}), p1={p1:.2f}")
        else:
            # Choose pixel (x+1, y-1)
            y -= 1
            p1 += 2 * ry2 * x - 2 * rx2 * y + ry2
            steps.append(f"Step {x}: p1≥0, choose (x+1,y-1) → ({x},{y}), p1={p1:.2f}")

        points.extend(plot_ellipse_points(xc, yc, x, y))

    steps.append("--- REGION 2 (slope ≥ -1) ---")

    # Region 2: where slope >= -1
    # Initial decision parameter for region 2
    p2 = ry2 * (x + 0.5) * (x + 0.5) + rx2 * (y - 1) * (y - 1) - rx2 * ry2
    steps.append(f"Initial p2={p2:.2f}")

    # Region 2: Continue until y = 0
    step_count = 0
    while y > 0:
        y -= 1
        step_count += 1

        if p2 > 0:
            # Choose pixel (x, y-1)
            p2 -= 2 * rx2 * y + rx2
            steps.append(f"R2 Step {step_count}: p2>0, choose (x,y-1) → ({x},{y}), p2={p2:.2f}")
        else:
            # Choose pixel (x+1, y-1)
            x += 1
            p2 += 2 * ry2 * x - 2 * rx2 * y + rx2
            steps.append(f"R2 Step {step_count}: p2≤0, choose (x+1,y-1) → ({x},{y}), p2={p2:.2f}")

        points.extend(plot_ellipse_points(xc, yc, x, y))

    steps.append(f"Total points generated: {len(points)}")
    return points, steps


class EllipseVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Mid-Point Ellipse Algorithm with Steps")
        self.root.geometry("1200x700")

        # Configure root grid
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
        input_frame = ttk.LabelFrame(self.left_frame, text="Ellipse Parameters", padding="10")
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Center coordinates
        ttk.Label(input_frame, text="Center X:").grid(row=0, column=0, padx=5)
        self.xc_var = tk.StringVar(value="200")
        ttk.Entry(input_frame, textvariable=self.xc_var, width=8).grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Center Y:").grid(row=0, column=2, padx=5)
        self.yc_var = tk.StringVar(value="150")
        ttk.Entry(input_frame, textvariable=self.yc_var, width=8).grid(row=0, column=3, padx=5)

        # Radii
        ttk.Label(input_frame, text="X-Radius:").grid(row=1, column=0, padx=5, pady=(10, 0))
        self.rx_var = tk.StringVar(value="80")
        ttk.Entry(input_frame, textvariable=self.rx_var, width=8).grid(row=1, column=1, padx=5, pady=(10, 0))

        ttk.Label(input_frame, text="Y-Radius:").grid(row=1, column=2, padx=5, pady=(10, 0))
        self.ry_var = tk.StringVar(value="50")
        ttk.Entry(input_frame, textvariable=self.ry_var, width=8).grid(row=1, column=3, padx=5, pady=(10, 0))

        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=(15, 0))

        ttk.Button(button_frame, text="Draw Ellipse", command=self.draw_ellipse).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)

        # Canvas
        self.canvas = tk.Canvas(self.left_frame, bg="white")
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # Right side - Algorithm steps panel
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

    def draw_ellipse(self):
        """Draw the ellipse using mid-point algorithm and show steps"""
        try:
            xc = int(self.xc_var.get())
            yc = int(self.yc_var.get())
            rx = int(self.rx_var.get())
            ry = int(self.ry_var.get())
        except ValueError:
            return

        # Clear previous ellipse
        self.canvas.delete("ellipse")

        # Get points and steps from mid-point ellipse algorithm
        points, steps = midpoint_ellipse_algorithm_with_steps(xc, yc, rx, ry)

        # Draw each pixel
        for x, y in points:
            self.canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1,
                                         fill="purple", outline="purple", tags="ellipse")

        # Draw center point
        self.canvas.create_oval(xc - 3, yc - 3, xc + 3, yc + 3,
                                fill="red", outline="darkred", tags="ellipse")

        # Draw axes for reference
        self.canvas.create_line(xc - rx, yc, xc + rx, yc,
                                fill="lightblue", dash=(5, 5), tags="ellipse")
        self.canvas.create_line(xc, yc - ry, xc, yc + ry,
                                fill="lightblue", dash=(5, 5), tags="ellipse")

        # Update steps panel
        self.update_steps_panel(steps)

    def update_steps_panel(self, steps):
        """Update the algorithm steps panel"""
        self.steps_text.delete(1.0, tk.END)

        # Add header
        header = f"Mid-Point Ellipse Algorithm Steps\n"
        header += "=" * 40 + "\n\n"
        self.steps_text.insert(tk.END, header)

        # Add each step
        for i, step in enumerate(steps, 1):
            if step.startswith("---"):
                self.steps_text.insert(tk.END, f"\n{step}\n")
            else:
                self.steps_text.insert(tk.END, f"{step}\n")

        # Scroll to top
        self.steps_text.see(1.0)

    def clear_canvas(self):
        """Clear the canvas and steps"""
        self.canvas.delete("ellipse")
        self.draw_grid()
        self.steps_text.delete(1.0, tk.END)
        self.steps_text.insert(tk.END, "Click 'Draw Ellipse' to see algorithm steps...")


if __name__ == "__main__":
    root = tk.Tk()
    app = EllipseVisualizer(root)
    root.mainloop()
