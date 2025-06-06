import OpenGL.GL as gl
import OpenGL.GLUT as glut
import sys


def draw_rectangle(x, y, width, height):
    """Draw a filled rectangle"""
    gl.glBegin(gl.GL_QUADS)
    gl.glVertex2f(x, y)
    gl.glVertex2f(x + width, y)
    gl.glVertex2f(x + width, y + height)
    gl.glVertex2f(x, y + height)
    gl.glEnd()


def draw_letter_A(x, y, size):
    """Draw letter A using rectangles"""
    # Left vertical bar
    draw_rectangle(x, y, size / 8, size)
    # Right vertical bar
    draw_rectangle(x + 7 * size / 8, y, size / 8, size)
    # Top horizontal bar
    draw_rectangle(x + size / 8, y + 7 * size / 8, 6 * size / 8, size / 8)
    # Middle horizontal bar
    draw_rectangle(x + size / 8, y + size / 2, 6 * size / 8, size / 8)


def draw_letter_S(x, y, size):
    """Draw letter S using rectangles"""
    # Top horizontal bar
    draw_rectangle(x, y + 7 * size / 8, size, size / 8)
    # Top left vertical
    draw_rectangle(x, y + size / 2, size / 8, 3 * size / 8)
    # Middle horizontal bar
    draw_rectangle(x, y + 3 * size / 8, size, size / 8)
    # Bottom right vertical
    draw_rectangle(x + 7 * size / 8, y, size / 8, 3 * size / 8)
    # Bottom horizontal bar
    draw_rectangle(x, y, size, size / 8)


def draw_letter_H(x, y, size):
    """Draw letter H using rectangles"""
    # Left vertical bar
    draw_rectangle(x, y, size / 8, size)
    # Right vertical bar
    draw_rectangle(x + 7 * size / 8, y, size / 8, size)
    # Horizontal bar
    draw_rectangle(x + size / 8, y + size / 2, 6 * size / 8, size / 8)


def draw_letter_W(x, y, size):
    """Draw letter W using rectangles"""
    # Left vertical bar
    draw_rectangle(x, y, size / 8, size)
    # Right vertical bar
    draw_rectangle(x + 7 * size / 8, y, size / 8, size)

    # Left diagonal (going from bottom-left to top-center)
    draw_rectangle(x + size / 8, y + size / 8, size / 8, size / 8)
    draw_rectangle(x + 2 * size / 8, y + 2 * size / 8, size / 8, size / 8)
    draw_rectangle(x + 2.5 * size / 8, y + 3 * size / 8, size / 8, size / 8)
    draw_rectangle(x + 3 * size / 8, y + 4 * size / 8, size / 8, size / 8)

    # Right diagonal (going from top-center to bottom-right)
    draw_rectangle(x + 3.5 * size / 8, y + 4 * size / 8, size / 8, size / 8)
    draw_rectangle(x + 4 * size / 8, y + 3 * size / 8, size / 8, size / 8)
    draw_rectangle(x + 5 * size / 8, y + 2 * size / 8, size / 8, size / 8)
    draw_rectangle(x + 6 * size / 8, y + size / 8, size / 8, size / 8)


def draw_letter_I(x, y, size):
    """Draw letter I using rectangles"""
    # Top horizontal bar
    draw_rectangle(x, y + 7 * size / 8, size, size / 8)
    # Middle vertical bar
    draw_rectangle(x + 3 * size / 8, y, 2 * size / 8, size)
    # Bottom horizontal bar
    draw_rectangle(x, y, size, size / 8)


def draw_letter_N(x, y, size):
    """Draw letter N using rectangles"""
    # Left vertical bar
    draw_rectangle(x, y, size / 8, size)
    # Right vertical bar
    draw_rectangle(x + 7 * size / 8, y, size / 8, size)
    # Diagonal using properly positioned rectangles
    draw_rectangle(x + size / 8, y + 6 * size / 8, size / 8, size / 8)
    draw_rectangle(x + 2 * size / 8, y + 5 * size / 8, size / 8, size / 8)
    draw_rectangle(x + 3 * size / 8, y + 4 * size / 8, size / 8, size / 8)
    draw_rectangle(x + 4 * size / 8, y + 3 * size / 8, size / 8, size / 8)
    draw_rectangle(x + 5 * size / 8, y + 2 * size / 8, size / 8, size / 8)
    draw_rectangle(x + 6 * size / 8, y + size / 8, size / 8, size / 8)


def display():
    """Main display function"""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    # Set color to cyan
    gl.glColor3f(0.0, 1.0, 1.0)

    # Letter parameters
    letter_size = 60
    spacing = 80
    start_x = -280
    start_y = -30

    # Draw ASHWINI
    draw_letter_A(start_x, start_y, letter_size)
    draw_letter_S(start_x + spacing, start_y, letter_size)
    draw_letter_H(start_x + 2 * spacing, start_y, letter_size)
    draw_letter_W(start_x + 3 * spacing, start_y, letter_size)
    draw_letter_I(start_x + 4 * spacing, start_y, letter_size)
    draw_letter_N(start_x + 5 * spacing, start_y, letter_size)
    draw_letter_I(start_x + 6 * spacing, start_y, letter_size)

    glut.glutSwapBuffers()


def reshape(width, height):
    """Handle window reshape"""
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(-400, 400, -200, 200, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()


def main():
    """Main function"""
    glut.glutInit(sys.argv)
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB)
    glut.glutInitWindowSize(800, 300)
    glut.glutInitWindowPosition(100, 100)
    glut.glutCreateWindow("ASHWINI")

    # Set background color to dark blue
    gl.glClearColor(0.1, 0.1, 0.3, 1.0)

    glut.glutDisplayFunc(display)
    glut.glutReshapeFunc(reshape)

    glut.glutMainLoop()


if __name__ == "__main__":
    main()
