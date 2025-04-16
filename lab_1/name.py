from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Window size
width, height = 800, 500


def draw_A(x, y, size):
    # Draw letter A using lines
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x + size / 2, y + size)
    glVertex2f(x + size, y)
    glVertex2f(x + size / 2, y + size)
    glVertex2f(x + size * 0.2, y + size * 0.5)
    glVertex2f(x + size * 0.8, y + size * 0.5)
    glEnd()


def draw_S(x, y, size):
    # Draw letter S using lines
    glBegin(GL_LINE_STRIP)
    glVertex2f(x + size, y + size)
    glVertex2f(x, y + size)
    glVertex2f(x, y + size / 2)
    glVertex2f(x + size, y + size / 2)
    glVertex2f(x + size, y)
    glVertex2f(x, y)
    glEnd()


def draw_H(x, y, size):
    # Draw letter H using lines
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x, y + size)
    glVertex2f(x + size, y)
    glVertex2f(x + size, y + size)
    glVertex2f(x, y + size / 2)
    glVertex2f(x + size, y + size / 2)
    glEnd()


def draw_W(x, y, size):
    # Draw letter W using lines
    glBegin(GL_LINES)
    glVertex2f(x, y + size)
    glVertex2f(x + size * 0.25, y)
    glVertex2f(x + size * 0.25, y)
    glVertex2f(x + size * 0.5, y + size * 0.7)
    glVertex2f(x + size * 0.5, y + size * 0.7)
    glVertex2f(x + size * 0.75, y)
    glVertex2f(x + size * 0.75, y)
    glVertex2f(x + size, y + size)
    glEnd()


def draw_I(x, y, size):
    # Draw letter I using lines
    glBegin(GL_LINES)
    glVertex2f(x + size / 2, y)
    glVertex2f(x + size / 2, y + size)
    glEnd()


def draw_N(x, y, size):
    # Draw letter N using lines
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x, y + size)
    glVertex2f(x, y + size)
    glVertex2f(x + size, y)
    glVertex2f(x + size, y)
    glVertex2f(x + size, y + size)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0, 0, 0.5)
    glLineWidth(5)

    # Starting x position and spacing
    x = 50
    y = 100
    size = 60
    spacing = 30

    # Draw each letter with spacing
    draw_A(x, y, size)
    x += size + spacing
    draw_S(x, y, size)
    x += size + spacing
    draw_H(x, y, size)
    x += size + spacing
    draw_W(x, y, size)
    x += size + spacing
    draw_I(x, y, size)
    x += size + spacing
    draw_N(x, y, size)
    x += size + spacing
    draw_I(x, y, size)

    glFlush()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("Draw ASHWINI ")
    glClearColor(1, 1, 1, 1)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMainLoop()


if __name__ == "__main__":
    main()

