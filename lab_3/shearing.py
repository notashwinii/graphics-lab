import pygame
import numpy as np
import math
from OpenGL.GL import *
from OpenGL.GLU import *


class ShearingDemo:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption(
            "2D Shearing  ")

        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-11, 11, -11, 11)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.original_line = np.array([
            [0.0, 2.0, 1.0],
            [1.0, 3.0, 1.0]
        ], dtype=np.float32)

        self.shear_x = 0.0
        self.shear_y = 0.0

    def create_shearing_matrix(self, shx, shy):
        return np.array([
            [1.0, shx, 0.0],
            [shy, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ], dtype=np.float32)

    def transform_line(self, line_points, transformation_matrix):
        return np.array([np.dot(transformation_matrix, point) for point in line_points])

    def draw_line(self, line_points, color):
        glColor3f(*color)
        glLineWidth(3.0)
        glBegin(GL_LINES)
        for point in line_points:
            glVertex2f(point[0], point[1])
        glEnd()

    def draw_point(self, x, y, color, size=6.0):
        glPointSize(size)
        glColor3f(*color)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    def draw_grid(self):
        glLineWidth(0.5)
        glColor3f(0.8, 0.8, 0.8)
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
        glColor3f(0.0, 0.0, 0.0)
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
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        glVertex2f(0, 0)
        glEnd()

    def get_shearing_input(self):
        print("\nEnter shearing parameters:")
        while True:
            try:
                print("\nShearing axis options:")
                print("1. X-shear (horizontal distortion)")
                print("2. Y-shear (vertical distortion)")
                print("3. Both X and Y shear")
                choice = input("Enter choice (1/2/3): ").strip()

                if choice == "1":
                    shx = float(input("Enter X-shear factor (shx): "))
                    shy = 0.0
                elif choice == "2":
                    shx = 0.0
                    shy = float(input("Enter Y-shear factor (shy): "))
                elif choice == "3":
                    shx = float(input("Enter X-shear factor (shx): "))
                    shy = float(input("Enter Y-shear factor (shy): "))
                else:
                    print("Invalid choice. Defaulting to no shear.")
                    shx, shy = 0.0, 0.0
                return shx, shy
            except ValueError:
                print("Invalid input. Please enter numeric values.")

    def display_original_info(self):
        print("=== 2D Geometric Shearing Demo ===")
        print("Grid scale: -10 to +10 (both X and Y axes)")
        print(f"\nOriginal line endpoints:")
        print(f"  Start: ({self.original_line[0][0]:.1f}, {
              self.original_line[0][1]:.1f})")
        print(f"  End:   ({self.original_line[1][0]:.1f}, {
              self.original_line[1][1]:.1f})")
        print("\nThe RED line shows the original position.")
        print("The RED dot marks the origin (0,0)")
        print("\nPress SPACE to continue and enter shearing parameters...")

    def display_shearing_info(self):
        print("\nShearing Applied:")
        if self.shear_x != 0.0 and self.shear_y != 0.0:
            desc = f"Both X and Y shear (shx: {self.shear_x:.2f}, shy: {
                self.shear_y:.2f})"
        elif self.shear_x != 0.0:
            desc = f"X-axis shear (shx: {self.shear_x:.2f})"
        elif self.shear_y != 0.0:
            desc = f"Y-axis shear (shy: {self.shear_y:.2f})"
        else:
            desc = "No shearing applied"
        print(f"Transformation: {desc}")

        shear_matrix = self.create_shearing_matrix(self.shear_x, self.shear_y)
        print("\nShearing Matrix:")
        for row in shear_matrix:
            print(f"[{row[0]:6.3f}  {row[1]:6.3f}  {row[2]:6.3f}]")

        sheared_line = self.transform_line(self.original_line, shear_matrix)
        print(f"\nSheared line endpoints:")
        print(f"  Start: ({sheared_line[0][0]:.1f}, {sheared_line[0][1]:.1f})")
        print(f"  End:   ({sheared_line[1][0]:.1f}, {sheared_line[1][1]:.1f})")

        print("\nVisualization:")
        print("  Red line: Original position")
        print("  Purple line: Sheared position")
        print("\nPress 'N' for new shearing or ESC to exit")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        show_original = True
        show_sheared = False
        need_input = False

        print("2D OpenGL Shearing Demo with Extended Grid")
        self.display_original_info()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE and show_original and not show_sheared:
                        need_input = True
                        show_original = False
                    elif event.key == pygame.K_n and show_sheared:
                        show_sheared = False
                        show_original = True
                        self.display_original_info()

            if need_input:
                self.shear_x, self.shear_y = self.get_shearing_input()
                self.display_shearing_info()
                show_sheared = True
                need_input = False

            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()
            self.draw_grid()
            self.draw_axes()

            if show_original or show_sheared:
                self.draw_line(self.original_line, (1.0, 0.0, 0.0))

            if show_sheared:
                shear_matrix = self.create_shearing_matrix(
                    self.shear_x, self.shear_y)
                sheared_line = self.transform_line(
                    self.original_line, shear_matrix)
                self.draw_line(sheared_line, (0.5, 0.0, 0.5))  # Purple

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


def main():
    print("Starting 2D OpenGL Shearing Demo...")
    print("Required libraries: pygame, PyOpenGL, numpy")
    try:
        demo = ShearingDemo()
        demo.run()
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Install with: pip install pygame PyOpenGL numpy")
    except Exception as e:
        print(f"Error running demo: {e}")


if __name__ == "__main__":
    main()
