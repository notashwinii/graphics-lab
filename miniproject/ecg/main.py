import glfw
import OpenGL.GL as gl
import time
import sys
from data import ECGDataGenerator
from render import ECGRenderer
from audio.heartbeat import HeartbeatAudio


class ECGVisualizerApp:
    def __init__(self, width=1200, height=600):
        """Initialize ECG visualizer application"""
        self.width = width
        self.height = height
        self.window = None

        # Initialize components
        self.ecg_generator = ECGDataGenerator(sample_rate=250, heart_rate=72)
        self.heartbeat_audio = HeartbeatAudio()

        # Timing
        self.last_time = time.time()
        self.frame_count = 0
        self.fps = 0

        # State
        self.audio_enabled = True

    def init_glfw(self):
        """Initialize GLFW and create window"""
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        # Use compatibility profile for better compatibility
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.SAMPLES, 4)

        # Create window
        self.window = glfw.create_window(
            self.width, self.height,
            "Real-time ECG Visualizer",
            None, None
        )

        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")

        # Set callbacks
        glfw.set_framebuffer_size_callback(self.window, self.framebuffer_size_callback)
        glfw.set_key_callback(self.window, self.key_callback)

        # Make context current
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # Enable vsync

        # Print OpenGL info
        print(f"OpenGL Version: {gl.glGetString(gl.GL_VERSION).decode()}")
        print(f"OpenGL Vendor: {gl.glGetString(gl.GL_VENDOR).decode()}")

        # Initialize renderer
        self.renderer = ECGRenderer(self.width, self.height)

        # Start audio
        if self.audio_enabled:
            self.heartbeat_audio.start_heartbeat(72)

        print("ECG Visualizer initialized successfully!")
        print("Controls:")
        print("  ESC   - Exit")
        print("  R     - Reset ECG")
        print("  SPACE - Toggle audio")
        print("  UP    - Increase heart rate")
        print("  DOWN  - Decrease heart rate")

    def framebuffer_size_callback(self, window, width, height):
        """Handle window resize"""
        self.width = width
        self.height = height
        self.renderer.resize(width, height)

    def key_callback(self, window, key, scancode, action, mods):
        """Handle keyboard input"""
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)
            elif key == glfw.KEY_R:
                current_hr = self.ecg_generator.heart_rate
                self.ecg_generator = ECGDataGenerator(sample_rate=250, heart_rate=current_hr)
                print(f"ECG reset (HR: {current_hr} BPM)")
            elif key == glfw.KEY_SPACE:
                if self.audio_enabled:
                    self.heartbeat_audio.stop_heartbeat()
                    self.audio_enabled = False
                    print("Audio OFF")
                else:
                    self.heartbeat_audio.start_heartbeat(self.ecg_generator.heart_rate)
                    self.audio_enabled = True
                    print("Audio ON")
            elif key == glfw.KEY_UP:
                new_hr = min(200, self.ecg_generator.heart_rate + 5)
                self.ecg_generator.heart_rate = new_hr
                if self.audio_enabled:
                    self.heartbeat_audio.update_bpm(new_hr)
                print(f"Heart rate: {new_hr} BPM")
            elif key == glfw.KEY_DOWN:
                new_hr = max(30, self.ecg_generator.heart_rate - 5)
                self.ecg_generator.heart_rate = new_hr
                if self.audio_enabled:
                    self.heartbeat_audio.update_bpm(new_hr)
                print(f"Heart rate: {new_hr} BPM")

    def update_fps(self):
        """Update FPS counter"""
        current_time = time.time()
        self.frame_count += 1

        if current_time - self.last_time >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.last_time = current_time

            heart_rate = self.ecg_generator.calculate_heart_rate()
            audio_status = "ON" if self.audio_enabled else "OFF"
            title = f"ECG Visualizer - HR: {heart_rate} BPM - Audio: {audio_status} - FPS: {self.fps}"
            glfw.set_window_title(self.window, title)

    def run(self):
        """Main application loop"""
        try:
            self.init_glfw()

            while not glfw.window_should_close(self.window):
                glfw.poll_events()

                # Update ECG data
                self.ecg_generator.update()

                # Get display data
                ecg_data = self.ecg_generator.get_display_data()
                heart_rate = self.ecg_generator.calculate_heart_rate()

                # Render frame
                self.renderer.render(ecg_data, heart_rate, self.audio_enabled)

                # Swap buffers
                glfw.swap_buffers(self.window)

                # Update FPS
                self.update_fps()

                # Control frame rate
                time.sleep(1.0 / 60.0)

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return 1
        finally:
            self.cleanup()

        return 0

    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'heartbeat_audio'):
            self.heartbeat_audio.stop_heartbeat()
        if self.window:
            glfw.destroy_window(self.window)
        glfw.terminate()
        print("Application terminated")


def main():
    """Entry point"""
    app = ECGVisualizerApp(width=1200, height=600)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
