import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np

# Clipping window boundaries
xmin, ymin = 100, 100
xmax, ymax = 300, 300

# Polygon vertices (example)
polygon = np.array([[50, 150], [200, 350], [350, 250], [250, 100]])

def inside(p, edge):
    x, y = p
    if edge == 'left':
        return x >= xmin
    elif edge == 'right':
        return x <= xmax
    elif edge == 'bottom':
        return y >= ymin
    elif edge == 'top':
        return y <= ymax

def intersect(p1, p2, edge):
    x1, y1 = p1
    x2, y2 = p2
    if edge == 'left':
        x = xmin
        y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
    elif edge == 'right':
        x = xmax
        y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
    elif edge == 'bottom':
        y = ymin
        x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
    elif edge == 'top':
        y = ymax
        x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
    return np.array([x, y])

def clip_polygon(polygon, edge):
    clipped_polygon = []
    n = len(polygon)
    for i in range(n):
        curr_point = polygon[i]
        prev_point = polygon[i - 1]
        curr_inside = inside(curr_point, edge)
        prev_inside = inside(prev_point, edge)

        if curr_inside:
            if not prev_inside:
                clipped_polygon.append(intersect(prev_point, curr_point, edge))
            clipped_polygon.append(curr_point)
        elif prev_inside:
            clipped_polygon.append(intersect(prev_point, curr_point, edge))
    return np.array(clipped_polygon)

def sutherland_hodgman(polygon):
    for edge in ['left', 'right', 'top', 'bottom']:
        polygon = clip_polygon(polygon, edge)
        if len(polygon) == 0:
            break
    return polygon

def draw_polygon(polygon, color):
    glColor3fv(color)
    glBegin(GL_LINE_LOOP)
    for vertex in polygon:
        glVertex2fv(vertex)
    glEnd()

def draw_clipping_window():
    glColor3f(1, 0, 0)  # Red
    glBegin(GL_LINE_LOOP)
    glVertex2f(xmin, ymin)
    glVertex2f(xmax, ymin)
    glVertex2f(xmax, ymax)
    glVertex2f(xmin, ymax)
    glEnd()

def main():
    pygame.init()
    display = (500, 500)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glOrtho(0, 500, 0, 500, -1, 1)  # Set orthographic 2D projection

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT)

        # Draw clipping window
        draw_clipping_window()

        # Draw original polygon in blue
        draw_polygon(polygon, (0, 0, 1))

        # Draw clipped polygon in green
        clipped_poly = sutherland_hodgman(polygon)
        if len(clipped_poly) > 0:
            draw_polygon(clipped_poly, (0, 1, 0))

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
