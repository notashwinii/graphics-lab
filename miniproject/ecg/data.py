import numpy as np
import time
from collections import deque
import math


class ECGDataGenerator:
    def __init__(self, sample_rate=250, heart_rate=72):
        """Initialize ECG data generator"""
        self.sample_rate = sample_rate
        self.heart_rate = heart_rate
        self.flatline = False
        self.audio_on = True
        self.current_waveform = []  # Holds samples for the current lub-dub
        self.waveform_index = 0
        self.display_length = sample_rate  # Number of points to display (e.g., 1 second)

    def on_beat(self, bpm):
        """Call this when a new audio beat occurs. Generates a full beat's worth of samples at the current BPM."""
        beat_duration = 60.0 / bpm
        num_samples = int(self.sample_rate * beat_duration)
        self.current_waveform = [self.generate_ecg_sample(i / self.sample_rate, bpm) for i in range(num_samples)]
        self.waveform_index = 0
        self.last_bpm = bpm

    def generate_ecg_sample(self, t, bpm=None):
        """Generate a highly realistic ECG waveform (P, Q, R, S, T waves) for a single beat, with a prominent R wave and smaller P/T waves."""
        if self.flatline or not self.audio_on:
            return 0.0
        if bpm is None:
            bpm = self.heart_rate
        beat_duration = 60.0 / bpm
        beat_time = t % beat_duration
        beat_phase = beat_time / beat_duration

        ecg_value = 0.0

        # P wave (smaller bump)
        if 0.08 <= beat_phase <= 0.18:
            p_center = 0.13
            p_width = 0.025
            p_amplitude = 0.36  # doubled again
            p_pos = (beat_phase - p_center) / p_width
            ecg_value += p_amplitude * math.exp(-0.5 * p_pos**2)

        # Q wave (deeper negative before spike)
        if 0.20 <= beat_phase <= 0.23:
            q_center = 0.215
            q_width = 0.008
            q_amplitude = -0.72  # doubled again
            q_pos = (beat_phase - q_center) / q_width
            ecg_value += q_amplitude * math.exp(-0.5 * q_pos**2)

        # R wave (taller spike)
        if 0.23 <= beat_phase <= 0.27:
            r_center = 0.25
            r_width = 0.012
            r_amplitude = 4.8  # doubled again
            r_pos = (beat_phase - r_center) / r_width
            ecg_value += r_amplitude * math.exp(-0.5 * r_pos**2)

        # S wave (deeper negative after spike)
        if 0.27 <= beat_phase <= 0.30:
            s_center = 0.285
            s_width = 0.01
            s_amplitude = -1.2  # doubled again
            s_pos = (beat_phase - s_center) / s_width
            ecg_value += s_amplitude * math.exp(-0.5 * s_pos**2)

        # T wave (smaller broad bump after spike)
        if 0.38 <= beat_phase <= 0.48:
            t_center = 0.43
            t_width = 0.03
            t_amplitude = 0.52  # doubled again
            t_pos = (beat_phase - t_center) / t_width
            ecg_value += t_amplitude * math.exp(-0.5 * t_pos**2)

        # Add a little noise for realism
        noise = np.random.normal(0, 0.01)
        return ecg_value + noise

    def next_sample(self):
        """Return the next sample: waveform if drawing, else flatline."""
        if self.flatline or not self.audio_on:
            return 0.0
        if self.waveform_index < len(self.current_waveform):
            val = self.current_waveform[self.waveform_index]
            self.waveform_index += 1
            return val
        else:
            return 0.0

    def get_display_data(self):
        """Get the current display data for the renderer: the current waveform (if drawing), padded with flatline."""
        data = []
        for i in range(self.display_length):
            if i < self.waveform_index and i < len(self.current_waveform):
                data.append(self.current_waveform[i])
            else:
                data.append(0.0)
        return data

    def calculate_heart_rate(self):
        """Return the most recent BPM (from the last beat or audio heartbeat)."""
        return getattr(self, 'last_bpm', self.heart_rate)

    def generate_samples(self, num_samples, fps=60):
        """On each frame, output one sample: from the beat queue if available, else flat (0.0)."""
        for _ in range(int(num_samples)):
            if self.flatline or not self.audio_on:
                self.ecg_buffer.append(0.0)
            elif self.beat_queue and self.beat_queue[0]:
                self.ecg_buffer.append(self.beat_queue[0].pop(0))
                if not self.beat_queue[0]:
                    self.beat_queue.pop(0)
            else:
                self.ecg_buffer.append(0.0)

    def set_timing(self, last_beat_time, bpm, audio_on):
        self.last_beat_time = last_beat_time
        self.current_bpm = bpm
        self.audio_on = audio_on
        self.flatline = not audio_on
