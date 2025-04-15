import pygame  # For window creation and event handling
from pygame.locals import DOUBLEBUF, OPENGL  # OpenGL-specific pygame constants
from OpenGL.GL import *  # OpenGL functions
from OpenGL.GLU import gluPerspective  # GLU utility for setting up perspective
from OpenGL.GLUT import glutInit, glutStrokeCharacter, glutStrokeWidth, GLUT_STROKE_ROMAN  # GLUT for text rendering


def main():
    # Initialize pygame
    pygame.init()

    # Set up display dimensions
    display_width, display_height = 800, 600
    display = (display_width, display_height)

    # Create a window with OpenGL
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL Text Rendering - ASHWINI")

    # Initialize GLUT for text rendering capabilities
    glutInit()

    # field of view, aspect ratio, near clipping plane, far clipping plane
    gluPerspective(45, (display_width / display_height), 0.5, 50.0)

    # Move the scene away from the camera
    glTranslatef(0.0, 0.0, -15)

    # background color
    glClearColor(0.8, 0.78, 0.69, 1.0)

    # Text to display
    text = "ASHWINI"

    # Calculate text width
    text_scale = 0.02
    text_width = 0
    for char in text:
        text_width += glutStrokeWidth(GLUT_STROKE_ROMAN, ord(char))
    text_width *= text_scale

    # Main application loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Clear the screen and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set text color
        glColor3f(0, 0, 0)

        # Set line width for the stroke font
        glLineWidth(4.0)

        # Draw text centered
        glPushMatrix()
        # Position text at center by offsetting by half the text width
        glTranslatef(-text_width / 2, 0, 0)
        glScalef(0.02, 0.02, 0.02)
        # Render each character in "ASHWINI"
        for character in text:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(character))

        glPopMatrix()

        # Swap the buffers to display what was rendered
        pygame.display.flip()

        # Control the frame rate
        pygame.time.wait(10)

    # Clean up and exit
    pygame.quit()


if __name__ == "__main__":
    main()

