import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

# --- Module 1: OpenGL Rendering ---


class OpenGLRenderer:
    def __init__(self, width, height, caption):
        pygame.init()
        self.width, self.height = width, height
        pygame.display.set_mode((self.width, self.height),
                                pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(caption)
        self._setup_opengl()

    def _setup_opengl(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)  # White background
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-11, 11, -11, 11)  # Extended orthographic projection
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def clear_screen(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

    def draw_line(self, line_points, color, line_width=3.0):
        glColor3f(*color)
        glLineWidth(line_width)
        glBegin(GL_LINES)
        for point in line_points:
            glVertex2f(point[0], point[1])
        glEnd()

    def draw_grid(self):
        glLineWidth(0.5)
        glColor3f(0.8, 0.8, 0.8)  # Light gray color
        for x in range(-10, 11):
            glBegin(GL_LINES)
            glVertex2f(x, -10)
            glVertex2f(x, 10)
            glEnd()
        for y in range(-10, 11):
            glBegin(GL_LINES)
            glVertex2f(-10, y)
            glVertex2f(10, y)
            glEnd()

    def draw_axes(self):
        glLineWidth(2.0)
        glColor3f(0.0, 0.0, 0.0)  # Black color for axes
        glBegin(GL_LINES)
        glVertex2f(-10, 0)
        glVertex2f(10, 0)
        glEnd()
        glBegin(GL_LINES)
        glVertex2f(0, -10)
        glVertex2f(0, 10)
        glEnd()

        glPointSize(3.0)
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        for i in range(-10, 11):
            if i != 0:
                glVertex2f(i, -0.2)
        for i in range(-10, 11):
            if i != 0:
                glVertex2f(-0.2, i)
        glEnd()

        glPointSize(6.0)
        glColor3f(1.0, 0.0, 0.0)  # Red color for origin
        glBegin(GL_POINTS)
        glVertex2f(0, 0)
        glEnd()

    def update_display(self):
        pygame.display.flip()

# --- Module 2: Geometric Transformations ---


class GeometricTransformations:
    @staticmethod
    def create_translation_matrix(tx, ty):
        """Create a 3x3 translation matrix for homogeneous coordinates"""
        return np.array([
            [1.0, 0.0, tx],
            [0.0, 1.0, ty],
            [0.0, 0.0, 1.0]
        ], dtype=np.float32)

    @staticmethod
    def transform_points(points, transformation_matrix):
        """Apply transformation matrix to a set of points"""
        transformed_points = []
        for point in points:
            transformed_point = np.dot(transformation_matrix, point)
            transformed_points.append(transformed_point)
        return np.array(transformed_points)

# --- Module 3: User Interface & Console Output ---


class UserInterface:
    def __init__(self, original_line_points):
        self.original_line = original_line_points

    def get_translation_input(self):
        print("\nEnter translation factors:")
        while True:
            try:
                tx = float(input("Enter X translation (tx): "))
                ty = float(input("Enter Y translation (ty): "))

                # Check visibility based on hardcoded original line points
                min_x = min(
                    self.original_line[0][0] + tx, self.original_line[1][0] + tx)
                max_x = max(
                    self.original_line[0][0] + tx, self.original_line[1][0] + tx)
                min_y = min(
                    self.original_line[0][1] + ty, self.original_line[1][1] + ty)
                max_y = max(
                    self.original_line[0][1] + ty, self.original_line[1][1] + ty)

                if (-10 <= min_x <= max_x <= 10) and (-10 <= min_y <= max_y <= 10):
                    return tx, ty
                else:
                    print(
                        "Warning: Translation will move line outside visible area (-10 to +10)")
                    choice = input("Continue anyway? (y/n): ").lower()
                    if choice == 'y':
                        return tx, ty
                    print("Please enter different values.")
            except ValueError:
                print("Please enter valid numbers!")

    def display_original_line_info(self):
        print(f"\nOriginal line endpoints:")
        print(f"  Start: ({self.original_line[0][0]:.1f}, {
              self.original_line[0][1]:.1f})")
        print(f"  End:   ({self.original_line[1][0]:.1f}, {
              self.original_line[1][1]:.1f})")
        print(f"\nThe RED line shows the original position.")
        print("The RED dot marks the origin (0,0)")
        print("Press SPACE to continue and enter translation factors...")

    def display_translated_line_info(self, tx, ty, translated_line_points):
        print(f"\nTransformation Applied:")
        print(f"Translation Matrix:")
        print(f"[1.0  0.0  {tx:6.2f}]")
        print(f"[0.0  1.0  {ty:6.2f}]")
        print(f"[0.0  0.0   1.00]")

        print(f"\nTranslated line endpoints:")
        print(f"  Start: ({translated_line_points[0][0]:.1f}, {
              translated_line_points[0][1]:.1f})")
        print(f"  End:   ({translated_line_points[1][0]:.1f}, {
              translated_line_points[1][1]:.1f})")
        print(f"\nVisualization:")
        print(f"  Red line: Original position")
        print(f"  Blue line: Translated position")
        print(f"  Red dot: Origin (0,0)")
        print(f"\nPress 'N' for new translation or ESC to exit")

# --- Main Application Logic ---


class TranslationDemo:
    def __init__(self):
        # Line vertices in homogeneous coordinates [x, y, 1]
        self.original_line = np.array([
            [2.0, 2.0, 1.0],  # Start point
            [6.0, 4.0, 1.0]   # End point
        ], dtype=np.float32)

        self.tx = 0.0
        self.ty = 0.0

        self.renderer = OpenGLRenderer(
            1200, 900, "translation")
        self.ui = UserInterface(self.original_line)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        show_original = True
        show_translated = False
        need_input = False

        self.ui.display_original_line_info()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE and show_original and not show_translated:
                        need_input = True
                        show_original = False
                    elif event.key == pygame.K_n and show_translated:
                        show_translated = False
                        show_original = True
                        self.ui.display_original_line_info()

            if need_input:
                self.tx, self.ty = self.ui.get_translation_input()
                translation_matrix = GeometricTransformations.create_translation_matrix(
                    self.tx, self.ty)
                translated_line = GeometricTransformations.transform_points(
                    self.original_line, translation_matrix)
                self.ui.display_translated_line_info(
                    self.tx, self.ty, translated_line)
                show_translated = True
                need_input = False

            self.renderer.clear_screen()
            self.renderer.draw_grid()
            self.renderer.draw_axes()

            if show_original or show_translated:
                self.renderer.draw_line(self.original_line, (1.0, 0.0, 0.0))

            if show_translated:
                translation_matrix = GeometricTransformations.create_translation_matrix(
                    self.tx, self.ty)
                translated_line = GeometricTransformations.transform_points(
                    self.original_line, translation_matrix)
                self.renderer.draw_line(translated_line, (0.0, 0.0, 1.0))

            self.renderer.update_display()
            clock.tick(60)

        pygame.quit()


def main():
    try:
        demo = TranslationDemo()
        demo.run()
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Install with: pip install pygame PyOpenGL numpy")
    except Exception as e:
        print(f"Error running demo: {e}")


if __name__ == "__main__":
    main()
