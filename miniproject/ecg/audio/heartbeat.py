import pygame
import numpy as np
import threading
import time


class HeartbeatAudio:
    def __init__(self, sample_rate=22050):
        """Initialize pygame mixer for heartbeat sounds"""
        try:
            pygame.mixer.pre_init(frequency=sample_rate, size=-16, channels=1, buffer=512)
            pygame.mixer.init()

            self.sample_rate = sample_rate
            self.is_playing = False
            self.current_bpm = 72
            self.audio_thread = None

            # Generate heartbeat sound
            self.heartbeat_sound = self.generate_heartbeat_sound()
            print("Audio system initialized successfully")

        except Exception as e:
            print(f"Audio initialization failed: {e}")
            self.heartbeat_sound = None

    def generate_heartbeat_sound(self):
        """Generate synthetic heartbeat sound"""
        try:
            duration = 0.6  # seconds
            samples = int(self.sample_rate * duration)

            sound_data = np.zeros(samples)

            # Lub sound (first heart sound)
            lub_start = int(0.05 * self.sample_rate)
            lub_duration = int(0.12 * self.sample_rate)
            lub_freq = 50  # Hz

            for i in range(lub_duration):
                t = i / self.sample_rate
                envelope = np.exp(-t * 10)
                sound_data[lub_start + i] = envelope * np.sin(2 * np.pi * lub_freq * t) * 0.3

            # Dub sound (second heart sound)
            dub_start = int(0.25 * self.sample_rate)
            dub_duration = int(0.08 * self.sample_rate)
            dub_freq = 100  # Hz

            for i in range(dub_duration):
                t = i / self.sample_rate
                envelope = np.exp(-t * 15)
                sound_data[dub_start + i] = envelope * np.sin(2 * np.pi * dub_freq * t) * 0.2

            # Convert to pygame sound
            sound_data = (sound_data * 32767).astype(np.int16)
            return pygame.sndarray.make_sound(sound_data)

        except Exception as e:
            print(f"Sound generation failed: {e}")
            return None

    def play_heartbeat_loop(self):
        """Play heartbeat sounds in a loop"""
        while self.is_playing and self.heartbeat_sound:
            try:
                self.heartbeat_sound.play()
                beat_interval = 60.0 / self.current_bpm
                time.sleep(beat_interval)
            except Exception as e:
                print(f"Audio playback error: {e}")
                break

    def start_heartbeat(self, bpm=72):
        """Start playing heartbeat sounds"""
        if not self.heartbeat_sound:
            return

        self.current_bpm = bpm
        if not self.is_playing:
            self.is_playing = True
            self.audio_thread = threading.Thread(target=self.play_heartbeat_loop)
            self.audio_thread.daemon = True
            self.audio_thread.start()

    def stop_heartbeat(self):
        """Stop playing heartbeat sounds"""
        self.is_playing = False
        if self.audio_thread:
            self.audio_thread.join(timeout=1.0)

    def update_bpm(self, new_bpm):
        """Update heartbeat rate"""
        self.current_bpm = max(30, min(200, new_bpm))
