import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *


class CompositeTransformDemo:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (0, 0), pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        self.width, self.height = 1400, 1000
        pygame.display.set_caption("2D Composite Transformations ")

        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-21, 21, -21, 21)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.original_line = np.array([
            [0.0, 2.0, 1.0],
            [1.0, 3.0, 1.0]
        ], dtype=np.float32)

    def create_translation_matrix(self, tx, ty):
        return np.array([
            [1.0, 0.0, tx],
            [0.0, 1.0, ty],
            [0.0, 0.0, 1.0]
        ], dtype=np.float32)

    def create_scaling_matrix(self, sx, sy):
        return np.array([
            [sx,  0.0, 0.0],
            [0.0, sy,  0.0],
            [0.0, 0.0, 1.0]
        ], dtype=np.float32)

    def create_shearing_matrix(self, shx, shy):
        return np.array([
            [1.0, shx, 0.0],
            [shy, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ], dtype=np.float32)

    def create_rotation_matrix(self, theta):
        rad = np.radians(theta)
        cos_t = np.cos(rad)
        sin_t = np.sin(rad)
        return np.array([
            [cos_t, -sin_t, 0.0],
            [sin_t,  cos_t, 0.0],
            [0.0,    0.0,   1.0]
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

    def draw_grid(self):
        glLineWidth(0.5)
        glColor3f(0.8, 0.8, 0.8)
        for x in range(-20, 21):
            glBegin(GL_LINES)
            glVertex2f(x, -20)
            glVertex2f(x, 20)
            glEnd()
        for y in range(-20, 21):
            glBegin(GL_LINES)
            glVertex2f(-20, y)
            glVertex2f(20, y)
            glEnd()

    def draw_axes(self):
        glLineWidth(2.0)
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex2f(-20, 0)
        glVertex2f(20, 0)
        glEnd()
        glBegin(GL_LINES)
        glVertex2f(0, -20)
        glVertex2f(0, 20)
        glEnd()

        glPointSize(6.0)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_POINTS)
        glVertex2f(0, 0)
        glEnd()

    def get_composite_input(self):
        print("\nEnter parameters for composite transformation:")
        tx = float(input("Translation X (tx): "))
        ty = float(input("Translation Y (ty): "))
        sx = float(input("Scaling X (sx): "))
        sy = float(input("Scaling Y (sy): "))
        shx = float(input("Shearing X (shx): "))
        shy = float(input("Shearing Y (shy): "))
        angle = float(input("Rotation angle (degrees): "))

        T = self.create_translation_matrix(tx, ty)
        S = self.create_scaling_matrix(sx, sy)
        H = self.create_shearing_matrix(shx, shy)
        R = self.create_rotation_matrix(angle)

        # Order: Translate -> Shear -> Scale -> Rotate
        return R @ S @ H @ T

    def display_matrix(self, mat):
        print("\nComposite Transformation Matrix:")
        for row in mat:
            print(f"[{row[0]:6.3f}  {row[1]:6.3f}  {row[2]:6.3f}]")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        transformed_line = None

        print("2D Composite Transformation Demo")
        print("Original line endpoints:")
        print(f"  Start: ({self.original_line[0][0]}, {
              self.original_line[0][1]})")
        print(f"  End:   ({self.original_line[1][0]}, {
              self.original_line[1][1]})")
        print("\nPress SPACE to apply transformation. Press ESC to exit.")

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        M = self.get_composite_input()
                        self.display_matrix(M)
                        transformed_line = self.transform_line(
                            self.original_line, M)
                        print(f"\nTransformed line:")
                        print(f"  Start: ({transformed_line[0][0]:.1f}, {
                              transformed_line[0][1]:.1f})")
                        print(f"  End:   ({transformed_line[1][0]:.1f}, {
                              transformed_line[1][1]:.1f})")

            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()
            self.draw_grid()
            self.draw_axes()
            self.draw_line(self.original_line, (1.0, 0.0, 0.0))
            if transformed_line is not None:
                self.draw_line(transformed_line, (0.0, 0.5, 1.0))
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


def main():
    print("Starting 2D Composite Transformation Demo...")
    print("Requires: pygame, PyOpenGL, numpy")
    try:
        demo = CompositeTransformDemo()
        demo.run()
    except Exception as e:
        print(f"Error: {e}")
        print("Install missing dependencies: pip install pygame PyOpenGL numpy")


if __name__ == "__main__":
    main()
