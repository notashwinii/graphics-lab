import pygame
import numpy as np
import math
from OpenGL.GL import *
from OpenGL.GLU import *


class RotationDemo:
    def __init__(self):
        """Initialize the rotation demo with extended grid"""
        pygame.init()

        # Bigger window size
        self.width, self.height = 1200, 900
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption(
            "2D Rotation Demo - Extended Grid (-10 to +10)")

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

        # Rotation factors (will be set by user input)
        self.angle_degrees = 0.0
        self.rotation_center_x = 0.0
        self.rotation_center_y = 0.0

    def create_rotation_matrix(self, angle_degrees, center_x=0.0, center_y=0.0):
        """Create a 3x3 rotation matrix for homogeneous coordinates
        Rotates around a specified center point (default is origin)"""
        angle_rad = math.radians(angle_degrees)
        cos_theta = math.cos(angle_rad)
        sin_theta = math.sin(angle_rad)

        if center_x == 0.0 and center_y == 0.0:
            # Simple rotation around origin
            return np.array([
                [cos_theta, -sin_theta, 0.0],
                [sin_theta,  cos_theta, 0.0],
                [0.0,        0.0,       1.0]
            ], dtype=np.float32)
        else:
            # Rotation around arbitrary point: T(center) * R * T(-center)
            # This is equivalent to: translate to origin, rotate, translate back
            return np.array([
                [cos_theta, -sin_theta, center_x -
                    center_x*cos_theta + center_y*sin_theta],
                [sin_theta,  cos_theta, center_y -
                    center_x*sin_theta - center_y*cos_theta],
                [0.0,        0.0,       1.0]
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
        """Get rotation parameters from user input"""
        print("\nEnter rotation parameters:")

        while True:
            try:
                angle = float(input("Enter rotation angle in degrees: "))

                print("\nChoose rotation center:")
                print("1. Origin (0, 0)")
                print("2. Custom point")
                choice = input("Enter choice (1 or 2): ").strip()

                if choice == "1":
                    center_x, center_y = 0.0, 0.0
                elif choice == "2":
                    center_x = float(input("Enter center X coordinate: "))
                    center_y = float(input("Enter center Y coordinate: "))
                else:
                    print("Invalid choice. Using origin (0, 0)")
                    center_x, center_y = 0.0, 0.0

                return angle, center_x, center_y

            except ValueError:
                print("Please enter valid numbers!")

    def display_original_info(self):
        """Display information about the original line"""
        print("=== 2D Geometric Rotation Demo ===")
        print("Grid scale: -10 to +10 (both X and Y axes)")
        print(f"\nOriginal line endpoints:")
        print(f"  Start: ({self.original_line[0][0]:.1f}, {
              self.original_line[0][1]:.1f})")
        print(f"  End:   ({self.original_line[1][0]:.1f}, {
              self.original_line[1][1]:.1f})")
        print(f"\nThe RED line shows the original position.")
        print("The RED dot marks the origin (0,0)")
        print("Press SPACE to continue and enter rotation parameters...")

    def display_transformation_info(self):
        """Display current transformation information"""
        print(f"\nRotation Applied:")
        print(f"Angle: {self.angle_degrees:.1f} degrees ({
              math.radians(self.angle_degrees):.3f} radians)")
        print(f"Center of rotation: ({self.rotation_center_x:.1f}, {
              self.rotation_center_y:.1f})")

        # Show the rotation matrix
        rotation_matrix = self.create_rotation_matrix(
            self.angle_degrees, self.rotation_center_x, self.rotation_center_y)
        print(f"\nRotation Matrix:")
        print(f"[{rotation_matrix[0][0]:6.3f}  {
              rotation_matrix[0][1]:6.3f}  {rotation_matrix[0][2]:6.3f}]")
        print(f"[{rotation_matrix[1][0]:6.3f}  {
              rotation_matrix[1][1]:6.3f}  {rotation_matrix[1][2]:6.3f}]")
        print(f"[{rotation_matrix[2][0]:6.3f}  {
              rotation_matrix[2][1]:6.3f}  {rotation_matrix[2][2]:6.3f}]")

        # Calculate rotated points
        rotated_line = self.transform_line(self.original_line, rotation_matrix)

        print(f"\nRotated line endpoints:")
        print(f"  Start: ({rotated_line[0][0]:.1f}, {rotated_line[0][1]:.1f})")
        print(f"  End:   ({rotated_line[1][0]:.1f}, {rotated_line[1][1]:.1f})")
        print(f"\nVisualization:")
        print(f"  Red line: Original position")
        print(f"  Blue line: Rotated position")
        print(f"  Green dot: Center of rotation")
        print(f"  Red dot: Origin (0,0)")
        print(f"\nPress 'N' for new rotation or ESC to exit")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        show_original = True
        show_rotated = False
        need_input = False

        print("2D OpenGL Rotation Demo with Extended Grid")

        # Display initial information
        self.display_original_info()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE and show_original and not show_rotated:
                        # Move to input phase
                        need_input = True
                        show_original = False
                    elif event.key == pygame.K_n and show_rotated:  # Press 'N' for new rotation
                        show_rotated = False
                        show_original = True
                        self.display_original_info()

            # Get user input for rotation parameters
            if need_input:
                self.angle_degrees, self.rotation_center_x, self.rotation_center_y = self.get_user_input()
                self.display_transformation_info()
                show_rotated = True
                need_input = False

            # Clear the screen
            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()

            # Draw grid and axes
            self.draw_grid()
            self.draw_axes()

            if show_original or show_rotated:
                # Always draw original line in red
                self.draw_line(self.original_line, (1.0, 0.0, 0.0))

            if show_rotated:
                # Create rotation matrix with user input
                rotation_matrix = self.create_rotation_matrix(
                    self.angle_degrees, self.rotation_center_x, self.rotation_center_y)

                # Apply rotation to the line
                rotated_line = self.transform_line(
                    self.original_line, rotation_matrix)

                # Draw rotated line in blue
                self.draw_line(rotated_line, (0.0, 0.0, 1.0))

                # Draw center of rotation in green (if not at origin)
                if self.rotation_center_x != 0.0 or self.rotation_center_y != 0.0:
                    self.draw_point(self.rotation_center_x,
                                    self.rotation_center_y, (0.0, 1.0, 0.0), 8.0)

            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

        pygame.quit()


def main():
    """Main function to run the rotation demo"""
    print("Starting 2D OpenGL Rotation Demo...")
    print("Required libraries: pygame, PyOpenGL, numpy")

    try:
        demo = RotationDemo()
        demo.run()
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Install with: pip install pygame PyOpenGL numpy")
    except Exception as e:
        print(f"Error running demo: {e}")


if __name__ == "__main__":
    main()
