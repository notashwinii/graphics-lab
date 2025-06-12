import OpenGL.GL as gl
import numpy as np
import math


class ECGRenderer:
    def __init__(self, width, height):
        """Initialize ECG renderer using immediate mode OpenGL"""
        self.width = width
        self.height = height

        # Display parameters
        self.samples_per_pixel = 2.0
        self.voltage_scale = 150.0
        self.scroll_speed = 1.0

        # Colors (RGB)
        self.bg_color = (0.02, 0.02, 0.08)      # Dark blue
        self.major_grid_color = (0.2, 0.3, 0.2)  # Green grid
        self.minor_grid_color = (0.1, 0.15, 0.1)  # Darker green
        self.ecg_color = (0.0, 1.0, 0.2)         # Bright green

        # Setup OpenGL for immediate mode
        self.setup_opengl()

    def setup_opengl(self):
        """Setup OpenGL state for immediate mode rendering"""
        # Use orthographic projection
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, self.width, 0, self.height, -1, 1)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        # Enable blending for smooth lines
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_LINE_SMOOTH)
        gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)

    def draw_grid(self):
        """Draw ECG grid using immediate mode"""
        # Major grid lines (every 50 pixels)
        gl.glColor3f(*self.major_grid_color)
        gl.glLineWidth(1.0)
        gl.glBegin(gl.GL_LINES)

        # Vertical major lines
        for x in range(0, self.width + 1, 50):
            gl.glVertex2f(x, 0)
            gl.glVertex2f(x, self.height)

        # Horizontal major lines
        for y in range(0, self.height + 1, 50):
            gl.glVertex2f(0, y)
            gl.glVertex2f(self.width, y)

        gl.glEnd()

        # Minor grid lines (every 10 pixels)
        gl.glColor3f(*self.minor_grid_color)
        gl.glBegin(gl.GL_LINES)

        # Vertical minor lines
        for x in range(0, self.width + 1, 10):
            if x % 50 != 0:  # Don't overlap major lines
                gl.glVertex2f(x, 0)
                gl.glVertex2f(x, self.height)

        # Horizontal minor lines
        for y in range(0, self.height + 1, 10):
            if y % 50 != 0:  # Don't overlap major lines
                gl.glVertex2f(0, y)
                gl.glVertex2f(self.width, y)

        gl.glEnd()

    def draw_ecg_waveform(self, ecg_data):
        """Draw ECG waveform using immediate mode"""
        if not ecg_data or len(ecg_data) < 2:
            return

        center_y = self.height // 2

        # Calculate how many samples to display
        samples_to_show = int(self.width / self.samples_per_pixel)
        start_idx = max(0, len(ecg_data) - samples_to_show)

        # Draw ECG waveform
        gl.glColor3f(*self.ecg_color)
        gl.glLineWidth(2.5)
        gl.glBegin(gl.GL_LINE_STRIP)

        for i in range(start_idx, len(ecg_data)):
            # Calculate screen coordinates
            x = (i - start_idx) * self.samples_per_pixel
            y = center_y + (ecg_data[i] * self.voltage_scale)

            # Clamp Y to screen bounds
            y = max(5, min(self.height - 5, y))

            gl.glVertex2f(x, y)

        gl.glEnd()

    def draw_info_text(self, heart_rate, audio_status):
        """Draw information text (simplified - just colored rectangles for now)"""
        # Draw heart rate indicator (red rectangle in top-left)
        gl.glColor3f(1.0, 0.0, 0.0)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(10, self.height - 30)
        gl.glVertex2f(100, self.height - 30)
        gl.glVertex2f(100, self.height - 10)
        gl.glVertex2f(10, self.height - 10)
        gl.glEnd()

        # Draw audio status indicator (green/red rectangle)
        if audio_status:
            gl.glColor3f(0.0, 1.0, 0.0)  # Green for audio on
        else:
            gl.glColor3f(0.5, 0.5, 0.5)  # Gray for audio off

        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(110, self.height - 30)
        gl.glVertex2f(200, self.height - 30)
        gl.glVertex2f(200, self.height - 10)
        gl.glVertex2f(110, self.height - 10)
        gl.glEnd()

    def render(self, ecg_data, heart_rate, audio_status=True):
        """Render complete ECG display"""
        # Clear screen
        gl.glClearColor(*self.bg_color, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # Draw grid
        self.draw_grid()

        # Draw ECG waveform
        self.draw_ecg_waveform(ecg_data)

        # Draw info indicators
        self.draw_info_text(heart_rate, audio_status)

    def resize(self, width, height):
        """Handle window resize"""
        self.width = width
        self.height = height

        gl.glViewport(0, 0, width, height)

        # Update projection matrix
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, width, 0, height, -1, 1)

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
