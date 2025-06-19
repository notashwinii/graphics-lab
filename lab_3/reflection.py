import pygame
import numpy as np
import math
from OpenGL.GL import *
from OpenGL.GLU import *


class ReflectionDemo:
    def __init__(self):
        """Initialize the reflection demo with extended grid"""
        pygame.init()

        # Bigger window size
        self.width, self.height = 1200, 900
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption(
            "2D Reflection Demo - Extended Grid (-10 to +10)")

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
            [6.0, 4.0, 1.0]   # End point
        ], dtype=np.float32)

        # Reflection parameters (will be set by user input)
        self.reflection_type = ""
        self.reflection_line_a = 0.0  # For ax + by + c = 0
        self.reflection_line_b = 0.0
        self.reflection_line_c = 0.0

    def create_reflection_matrix_x_axis(self):
        """Create reflection matrix across X-axis (y = 0)"""
        return np.array([
            [1.0,  0.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0,  0.0, 1.0]
        ], dtype=np.float32)

    def create_reflection_matrix_y_axis(self):
        """Create reflection matrix across Y-axis (x = 0)"""
        return np.array([
            [-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ], dtype=np.float32)

    def create_reflection_matrix_line_y_equals_x(self):
        """Create reflection matrix across line y = x"""
        return np.array([
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0]
        ], dtype=np.float32)

    def create_reflection_matrix_line_y_equals_minus_x(self):
        """Create reflection matrix across line y = -x"""
        return np.array([
            [0.0, -1.0, 0.0],
            [-1.0,  0.0, 0.0],
            [0.0,  0.0, 1.0]
        ], dtype=np.float32)

    def create_reflection_matrix_arbitrary_line(self, a, b, c):
        """Create reflection matrix across arbitrary line ax + by + c = 0
        Formula: R = I - 2 * (n * n^T) / (n^T * n)
        where n = [a, b] is the normal vector to the line"""
        if a == 0 and b == 0:
            # Invalid line, return identity
            return np.eye(3, dtype=np.float32)

        # Normalize the line equation coefficients
        norm = math.sqrt(a*a + b*b)
        a_norm = a / norm
        b_norm = b / norm
        c_norm = c / norm

        # Reflection matrix for line ax + by + c = 0
        return np.array([
            [1 - 2*a_norm*a_norm,    -2*a_norm*b_norm,    -2*a_norm*c_norm],
            [-2*a_norm*b_norm, 1 - 2*b_norm*b_norm,    -2*b_norm*c_norm],
            [0.0,                 0.0,                 1.0]
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

    def draw_reflection_line(self, a, b, c, color):
        """Draw the line of reflection ax + by + c = 0"""
        if abs(b) > 0.001:  # Not vertical line
            # y = -(ax + c) / b
            x1, x2 = -10, 10
            y1 = -(a * x1 + c) / b
            y2 = -(a * x2 + c) / b
        elif abs(a) > 0.001:  # Vertical line
            # x = -c / a
            x1 = x2 = -c / a
            y1, y2 = -10, 10
        else:
            return  # Invalid line

        # Clip to visible area
        if abs(y1) > 10 or abs(y2) > 10:
            if abs(a) > 0.001:
                # Try horizontal clipping
                y1, y2 = -10, 10
                x1 = -(b * y1 + c) / a
                x2 = -(b * y2 + c) / a

        glColor3f(*color)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
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
        """Get reflection parameters from user input"""
        print("\nChoose reflection type:")
        print("1. Reflection across X-axis (y = 0)")
        print("2. Reflection across Y-axis (x = 0)")
        print("3. Reflection across line y = x")
        print("4. Reflection across line y = -x")
        print("5. Reflection across arbitrary line (ax + by + c = 0)")

        while True:
            try:
                choice = input("Enter choice (1-5): ").strip()

                if choice == "1":
                    return "x_axis", 0.0, 1.0, 0.0  # y = 0 is 0x + 1y + 0 = 0
                elif choice == "2":
                    return "y_axis", 1.0, 0.0, 0.0  # x = 0 is 1x + 0y + 0 = 0
                elif choice == "3":
                    return "y_equals_x", 1.0, -1.0, 0.0  # y = x is x - y = 0
                elif choice == "4":
                    return "y_equals_minus_x", 1.0, 1.0, 0.0  # y = -x is x + y = 0
                elif choice == "5":
                    print("Enter coefficients for line ax + by + c = 0:")
                    a = float(input("Enter coefficient a: "))
                    b = float(input("Enter coefficient b: "))
                    c = float(input("Enter coefficient c: "))

                    if a == 0 and b == 0:
                        print("Invalid line equation (a and b cannot both be 0)")
                        continue

                    return "arbitrary", a, b, c
                else:
                    print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

            except ValueError:
                print("Please enter valid numbers!")

    def get_reflection_matrix(self):
        """Get the appropriate reflection matrix based on user choice"""
        if self.reflection_type == "x_axis":
            return self.create_reflection_matrix_x_axis()
        elif self.reflection_type == "y_axis":
            return self.create_reflection_matrix_y_axis()
        elif self.reflection_type == "y_equals_x":
            return self.create_reflection_matrix_line_y_equals_x()
        elif self.reflection_type == "y_equals_minus_x":
            return self.create_reflection_matrix_line_y_equals_minus_x()
        elif self.reflection_type == "arbitrary":
            return self.create_reflection_matrix_arbitrary_line(
                self.reflection_line_a, self.reflection_line_b, self.reflection_line_c)
        else:
            return np.eye(3, dtype=np.float32)

    def get_reflection_description(self):
        """Get description of the reflection line"""
        if self.reflection_type == "x_axis":
            return "X-axis (y = 0)"
        elif self.reflection_type == "y_axis":
            return "Y-axis (x = 0)"
        elif self.reflection_type == "y_equals_x":
            return "Line y = x"
        elif self.reflection_type == "y_equals_minus_x":
            return "Line y = -x"
        elif self.reflection_type == "arbitrary":
            return f"Line {self.reflection_line_a:.1f}x + {self.reflection_line_b:.1f}y + {self.reflection_line_c:.1f} = 0"
        else:
            return "Unknown"

    def display_original_info(self):
        """Display information about the original line"""
        print(f"\nOriginal line endpoints:")
        print(f"  Start: ({self.original_line[0][0]:.1f}, {
              self.original_line[0][1]:.1f})")
        print(f"  End:   ({self.original_line[1][0]:.1f}, {
              self.original_line[1][1]:.1f})")
        print(f"\nThe RED line shows the original position.")
        print("The RED dot marks the origin (0,0)")
        print("Press SPACE to continue and choose reflection type...")

    def display_transformation_info(self):
        """Display current transformation information"""
        print(f"\nReflection Applied:")
        print(f"Reflection across: {self.get_reflection_description()}")

        # Show the reflection matrix
        reflection_matrix = self.get_reflection_matrix()
        print(f"\nReflection Matrix:")
        print(f"[{reflection_matrix[0][0]:6.3f}  {
              reflection_matrix[0][1]:6.3f}  {reflection_matrix[0][2]:6.3f}]")
        print(f"[{reflection_matrix[1][0]:6.3f}  {
              reflection_matrix[1][1]:6.3f}  {reflection_matrix[1][2]:6.3f}]")
        print(f"[{reflection_matrix[2][0]:6.3f}  {
              reflection_matrix[2][1]:6.3f}  {reflection_matrix[2][2]:6.3f}]")

        # Calculate reflected points
        reflected_line = self.transform_line(
            self.original_line, reflection_matrix)

        print(f"\nReflected line endpoints:")
        print(f"  Start: ({reflected_line[0][0]:.1f}, {
              reflected_line[0][1]:.1f})")
        print(f"  End:   ({reflected_line[1][0]:.1f}, {
              reflected_line[1][1]:.1f})")
        print(f"\nVisualization:")
        print(f"  Red line: Original position")
        print(f"  Blue line: Reflected position")
        print(f"  Green line: Line of reflection")
        print(f"  Red dot: Origin (0,0)")
        print(f"\nPress 'N' for new reflection or ESC to exit")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        show_original = True
        show_reflected = False
        need_input = False

        print("2D OpenGL Reflection Demo with Extended Grid")

        # Display initial information
        self.display_original_info()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE and show_original and not show_reflected:
                        # Move to input phase
                        need_input = True
                        show_original = False
                    elif event.key == pygame.K_n and show_reflected:  # Press 'N' for new reflection
                        show_reflected = False
                        show_original = True
                        self.display_original_info()

            # Get user input for reflection parameters
            if need_input:
                (self.reflection_type, self.reflection_line_a,
                 self.reflection_line_b, self.reflection_line_c) = self.get_user_input()
                self.display_transformation_info()
                show_reflected = True
                need_input = False

            # Clear the screen
            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()

            # Draw grid and axes
            self.draw_grid()
            self.draw_axes()

            if show_original or show_reflected:
                # Always draw original line in red
                self.draw_line(self.original_line, (1.0, 0.0, 0.0))

            if show_reflected:
                # Create reflection matrix with user input
                reflection_matrix = self.get_reflection_matrix()

                # Apply reflection to the line
                reflected_line = self.transform_line(
                    self.original_line, reflection_matrix)

                # Draw reflected line in blue
                self.draw_line(reflected_line, (0.0, 0.0, 1.0))

                # Draw line of reflection in green
                self.draw_reflection_line(
                    self.reflection_line_a, self.reflection_line_b, self.reflection_line_c,
                    (0.0, 0.8, 0.0))

            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

        pygame.quit()


def main():
    """Main function to run the reflection demo"""
    print("Starting 2D OpenGL Reflection Demo...")
    print("Required libraries: pygame, PyOpenGL, numpy")

    try:
        demo = ReflectionDemo()
        demo.run()
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Install with: pip install pygame PyOpenGL numpy")
    except Exception as e:
        print(f"Error running demo: {e}")


if __name__ == "__main__":
    main()
