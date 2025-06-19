import pygame
import numpy as np
import math
from OpenGL.GL import *
from OpenGL.GLU import *


class ScalingDemo:
    def __init__(self):
        """Initialize the scaling  with extended grid"""
        pygame.init()

        # Bigger window size
        self.width, self.height = 1200, 900
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption(
            "2D Scaling ")

        # Set up OpenGL
        glClearColor(1.0, 1.0, 1.0, 1.0)  # White background
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Extended orthographic projection (-10 to +10 on both axes)
        gluOrtho2D(-11, 11, -11, 11)
        glMatrixMode(GL_MODELVIEW)

        # Enable line smoothing
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Line vertices in homogeneous coordinates [x, y, 1]
        # Positioned more centrally in the new coordinate system
        self.original_line = np.array([
            [2.0, 2.0, 1.0],  # Start point
            [2.0, 4.0, 1.0]   # End point
        ], dtype=np.float32)

        # Scaling parameters (will be set by user input)
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.scaling_center_x = 0.0
        self.scaling_center_y = 0.0

    def create_scaling_matrix(self, sx, sy, center_x=0.0, center_y=0.0):
        """Create a 3x3 scaling matrix for homogeneous coordinates
        Scales around a specified center point (default is origin)"""

        if center_x == 0.0 and center_y == 0.0:
            # Simple scaling around origin
            return np.array([
                [sx,  0.0, 0.0],
                [0.0, sy,  0.0],
                [0.0, 0.0, 1.0]
            ], dtype=np.float32)
        else:
            # Scaling around arbitrary point: T(center) * S * T(-center)
            # This is equivalent to: translate to origin, scale, translate back
            return np.array([
                [sx,  0.0, center_x * (1 - sx)],
                [0.0, sy,  center_y * (1 - sy)],
                [0.0, 0.0, 1.0]
            ], dtype=np.float32)

    def transform_line(self, line_points, transformation_matrix):
        """Apply transformation matrix to line points"""
        # Multiply each point by the transformation matrix
        transformed_points = []
        for point in line_points:
            # Matrix multiplication: T * point
            transformed_point = np.dot(transformation_matrix, point)
            transformed_points.append(transformed_point)
        return np.array(transformed_points)

    def draw_line(self, line_points, color):
        """Draw a line given two points"""
        glColor3f(*color)
        glLineWidth(3.0)
        glBegin(GL_LINES)
        for point in line_points:
            # Use only x and y coordinates (ignore homogeneous coordinate)
            glVertex2f(point[0], point[1])
        glEnd()

    def draw_point(self, x, y, color, size=6.0):
        """Draw a point at specified coordinates"""
        glPointSize(size)
        glColor3f(*color)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    def draw_grid(self):
        """Draw extended grid lines for better visualization (-10 to +10)"""
        glLineWidth(0.5)
        glColor3f(0.8, 0.8, 0.8)  # Light gray color

        # Vertical grid lines from -10 to +10
        for x in range(-10, 11):
            glBegin(GL_LINES)
            glVertex2f(x, -10)
            glVertex2f(x, 10)
            glEnd()

        # Horizontal grid lines from -10 to +10
        for y in range(-10, 11):
            glBegin(GL_LINES)
            glVertex2f(-10, y)
            glVertex2f(10, y)
            glEnd()

    def draw_axes(self):
        """Draw coordinate axes for reference"""
        glLineWidth(2.0)
        glColor3f(0.0, 0.0, 0.0)  # Black color for axes

        # X-axis (horizontal line through y=0)
        glBegin(GL_LINES)
        glVertex2f(-10, 0)
        glVertex2f(10, 0)
        glEnd()

        # Y-axis (vertical line through x=0)
        glBegin(GL_LINES)
        glVertex2f(0, -10)
        glVertex2f(0, 10)
        glEnd()

        # Draw axis marks
        glPointSize(3.0)
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        # X-axis marks
        for i in range(-10, 11):
            if i != 0:  # Skip the origin
                glVertex2f(i, -0.2)
        # Y-axis marks
        for i in range(-10, 11):
            if i != 0:  # Skip the origin
                glVertex2f(-0.2, i)
        glEnd()

        # Highlight the origin
        glPointSize(6.0)
        glColor3f(1.0, 0.0, 0.0)  # Red color for origin
        glBegin(GL_POINTS)
        glVertex2f(0, 0)
        glEnd()

    def get_user_input(self):
        """Get scaling parameters from user input"""
        print("\nEnter scaling parameters:")

        while True:
            try:
                print("\nScaling factor options:")
                print("1. Uniform scaling (same factor for X and Y)")
                print("2. Non-uniform scaling (different factors for X and Y)")
                choice = input("Enter choice (1 or 2): ").strip()

                if choice == "1":
                    scale_factor = float(
                        input("Enter uniform scaling factor: "))
                    sx, sy = scale_factor, scale_factor
                elif choice == "2":
                    sx = float(input("Enter X scaling factor (sx): "))
                    sy = float(input("Enter Y scaling factor (sy): "))
                else:
                    print("Invalid choice. Using uniform scaling.")
                    scale_factor = float(
                        input("Enter uniform scaling factor: "))
                    sx, sy = scale_factor, scale_factor

                print("\nChoose scaling center:")
                print("1. Origin (0, 0)")
                print("2. Custom point")
                center_choice = input("Enter choice (1 or 2): ").strip()

                if center_choice == "1":
                    center_x, center_y = 0.0, 0.0
                elif center_choice == "2":
                    center_x = float(input("Enter center X coordinate: "))
                    center_y = float(input("Enter center Y coordinate: "))
                else:
                    print("Invalid choice. Using origin (0, 0)")
                    center_x, center_y = 0.0, 0.0

                # Validate scaling factors
                if sx == 0 or sy == 0:
                    print("Warning: Zero scaling factor will collapse the object!")
                    confirm = input("Continue anyway? (y/n): ").lower()
                    if confirm != 'y':
                        continue

                return sx, sy, center_x, center_y

            except ValueError:
                print("Please enter valid numbers!")

    def get_scaling_description(self):
        """Get description of the scaling transformation"""
        if abs(self.scale_x - self.scale_y) < 0.001:
            scale_type = f"Uniform scaling (factor: {self.scale_x:.2f})"
        else:
            scale_type = f"Non-uniform scaling (sx: {self.scale_x:.2f}, sy: {
                self.scale_y:.2f})"

        if self.scaling_center_x == 0.0 and self.scaling_center_y == 0.0:
            center_desc = "around origin"
        else:
            center_desc = f"around point ({self.scaling_center_x:.1f}, {
                self.scaling_center_y:.1f})"

        return f"{scale_type} {center_desc}"

    def display_original_info(self):
        """Display information about the original line"""
        print("=== 2D Geometric Scaling Demo ===")
        print("Grid scale: -10 to +10 (both X and Y axes)")
        print(f"\nOriginal line endpoints:")
        print(f"  Start: ({self.original_line[0][0]:.1f}, {
              self.original_line[0][1]:.1f})")
        print(f"  End:   ({self.original_line[1][0]:.1f}, {
              self.original_line[1][1]:.1f})")
        print(f"\nThe RED line shows the original position.")
        print("The RED dot marks the origin (0,0)")
        print("\nScaling types you can explore:")
        print("- Uniform scaling: Same factor for both X and Y (maintains shape)")
        print("- Non-uniform scaling: Different factors for X and Y (distorts shape)")
        print("- Scaling around origin vs. custom point")
        print("- Negative scaling factors (includes reflection)")
        print("\nPress SPACE to continue and enter scaling parameters...")

    def display_transformation_info(self):
        """Display current transformation information"""
        print(f"\nScaling Applied:")
        print(f"Transformation: {self.get_scaling_description()}")

        # Show the scaling matrix
        scaling_matrix = self.create_scaling_matrix(
            self.scale_x, self.scale_y, self.scaling_center_x, self.scaling_center_y)
        print(f"\nScaling Matrix:")
        print(f"[{scaling_matrix[0][0]:6.3f}  {
              scaling_matrix[0][1]:6.3f}  {scaling_matrix[0][2]:6.3f}]")
        print(f"[{scaling_matrix[1][0]:6.3f}  {
              scaling_matrix[1][1]:6.3f}  {scaling_matrix[1][2]:6.3f}]")
        print(f"[{scaling_matrix[2][0]:6.3f}  {
              scaling_matrix[2][1]:6.3f}  {scaling_matrix[2][2]:6.3f}]")

        # Calculate scaled points
        scaled_line = self.transform_line(self.original_line, scaling_matrix)

        print(f"\nScaled line endpoints:")
        print(f"  Start: ({scaled_line[0][0]:.1f}, {scaled_line[0][1]:.1f})")
        print(f"  End:   ({scaled_line[1][0]:.1f}, {scaled_line[1][1]:.1f})")

        # Additional information about the transformation
        if self.scale_x > 0 and self.scale_y > 0:
            if self.scale_x > 1 or self.scale_y > 1:
                print("Effect: Object enlarged (magnification)")
            elif self.scale_x < 1 or self.scale_y < 1:
                print("Effect: Object reduced (minification)")
            else:
                print("Effect: No size change")
        else:
            print("Effect: Includes reflection due to negative scaling factor(s)")

        print(f"\nVisualization:")
        print(f"  Red line: Original position")
        print(f"  Blue line: Scaled position")
        if self.scaling_center_x != 0.0 or self.scaling_center_y != 0.0:
            print(f"  Green dot: Center of scaling")
        print(f"  Red dot: Origin (0,0)")
        print(f"\nPress 'N' for new scaling or ESC to exit")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        show_original = True
        show_scaled = False
        need_input = False

        print("2D OpenGL Scaling Demo with Extended Grid")

        # Display initial information
        self.display_original_info()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE and show_original and not show_scaled:
                        # Move to input phase
                        need_input = True
                        show_original = False
                    elif event.key == pygame.K_n and show_scaled:  # Press 'N' for new scaling
                        show_scaled = False
                        show_original = True
                        self.display_original_info()

            # Get user input for scaling parameters
            if need_input:
                (self.scale_x, self.scale_y,
                 self.scaling_center_x, self.scaling_center_y) = self.get_user_input()
                self.display_transformation_info()
                show_scaled = True
                need_input = False

            # Clear the screen
            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()

            # Draw grid and axes
            self.draw_grid()
            self.draw_axes()

            if show_original or show_scaled:
                # Always draw original line in red
                self.draw_line(self.original_line, (1.0, 0.0, 0.0))

            if show_scaled:
                # Create scaling matrix with user input
                scaling_matrix = self.create_scaling_matrix(
                    self.scale_x, self.scale_y, self.scaling_center_x, self.scaling_center_y)

                # Apply scaling to the line
                scaled_line = self.transform_line(
                    self.original_line, scaling_matrix)

                # Draw scaled line in blue
                self.draw_line(scaled_line, (0.0, 0.0, 1.0))

                # Draw center of scaling in green (if not at origin)
                if self.scaling_center_x != 0.0 or self.scaling_center_y != 0.0:
                    self.draw_point(self.scaling_center_x,
                                    self.scaling_center_y, (0.0, 1.0, 0.0), 8.0)

            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

        pygame.quit()


def main():
    """Main function to run the scaling demo"""
    print("Starting 2D OpenGL Scaling Demo...")
    print("Required libraries: pygame, PyOpenGL, numpy")

    try:
        demo = ScalingDemo()
        demo.run()
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Install with: pip install pygame PyOpenGL numpy")
    except Exception as e:
        print(f"Error running demo: {e}")


if __name__ == "__main__":
    main()
