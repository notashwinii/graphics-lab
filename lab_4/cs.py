import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Clipping window boundaries
xmin, ymin = 100, 100
xmax, ymax = 300, 300

# Outcode bit constants
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000


def compute_outcode(x, y):
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP
    return code


def cohen_sutherland_clip(x0, y0, x1, y1):
    outcode0 = compute_outcode(x0, y0)
    outcode1 = compute_outcode(x1, y1)
    accept = False

    while True:
        if outcode0 == 0 and outcode1 == 0:
            accept = True
            break
        elif (outcode0 & outcode1) != 0:
            break
        else:
            outcode_out = outcode0 if outcode0 != 0 else outcode1
            x, y = 0.0, 0.0

            if outcode_out & TOP:
                x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
                y = ymax
            elif outcode_out & BOTTOM:
                x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
                y = ymin
            elif outcode_out & RIGHT:
                y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
                x = xmax
            elif outcode_out & LEFT:
                y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
                x = xmin

            if outcode_out == outcode0:
                x0, y0 = x, y
                outcode0 = compute_outcode(x0, y0)
            else:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1)

    if accept:
        return (x0, y0, x1, y1)
    else:
        return None


def draw_line(x0, y0, x1, y1, color):
    glColor3fv(color)
    glBegin(GL_LINES)
    glVertex2f(x0, y0)
    glVertex2f(x1, y1)
    glEnd()


def draw_rectangle(xmin, ymin, xmax, ymax, color):
    glColor3fv(color)
    glBegin(GL_LINE_LOOP)
    glVertex2f(xmin, ymin)
    glVertex2f(xmax, ymin)
    glVertex2f(xmax, ymax)
    glVertex2f(xmin, ymax)
    glEnd()


def main():
    pygame.init()
    display = (400, 400)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Set orthographic projection using glOrtho (not gluOrtho2D)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, display[0], 0, display[1], -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Example line endpoints (partially outside clipping window)
    x0, y0 = 50, 150
    x1, y1 = 350, 250

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT)

        # Draw clipping rectangle in red
        draw_rectangle(xmin, ymin, xmax, ymax, (1, 0, 0))

        # Draw original line in blue
        draw_line(x0, y0, x1, y1, (0, 0, 1))

        # Draw clipped line in green (if any)
        clipped_line = cohen_sutherland_clip(x0, y0, x1, y1)
        if clipped_line:
            draw_line(*clipped_line, (0, 1, 0))

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()
