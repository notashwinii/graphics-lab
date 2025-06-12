import numpy as np
import time
from collections import deque
import math


class ECGDataGenerator:
    def __init__(self, sample_rate=250, heart_rate=72):
        """Initialize ECG data generator"""
        self.sample_rate = sample_rate
        self.heart_rate = heart_rate
        self.beat_duration = 60.0 / heart_rate
        self.current_time = 0.0
        self.time_step = 1.0 / sample_rate

        # Buffer for display data (10 seconds)
        self.buffer_size = sample_rate * 10
        self.ecg_buffer = deque(maxlen=self.buffer_size)

        # Initialize with baseline
        for _ in range(self.buffer_size):
            self.ecg_buffer.append(0.0)

    def generate_ecg_sample(self, t):
        """Generate realistic ECG waveform"""
        # Calculate position within heartbeat cycle
        beat_time = t % self.beat_duration
        beat_phase = beat_time / self.beat_duration

        ecg_value = 0.0

        # P wave (8-18% of cycle)
        if 0.08 <= beat_phase <= 0.18:
            p_center = 0.13
            p_width = 0.04
            p_amplitude = 0.2
            p_pos = (beat_phase - p_center) / p_width
            ecg_value += p_amplitude * math.exp(-0.5 * p_pos**2)

        # QRS complex (35-45% of cycle)
        elif 0.35 <= beat_phase <= 0.45:
            qrs_center = 0.4

            # Q wave (negative deflection)
            if 0.35 <= beat_phase <= 0.38:
                q_amplitude = -0.15
                q_width = 0.015
                q_pos = (beat_phase - 0.365) / q_width
                ecg_value += q_amplitude * math.exp(-0.5 * q_pos**2)

            # R wave (large positive spike)
            elif 0.38 <= beat_phase <= 0.42:
                r_amplitude = 1.2
                r_width = 0.02
                r_pos = (beat_phase - qrs_center) / r_width
                ecg_value += r_amplitude * math.exp(-0.5 * r_pos**2)

            # S wave (negative after R)
            else:
                s_amplitude = -0.3
                s_width = 0.015
                s_pos = (beat_phase - 0.43) / s_width
                ecg_value += s_amplitude * math.exp(-0.5 * s_pos**2)

        # T wave (65-85% of cycle)
        elif 0.65 <= beat_phase <= 0.85:
            t_center = 0.75
            t_width = 0.08
            t_amplitude = 0.25
            t_pos = (beat_phase - t_center) / t_width
            ecg_value += t_amplitude * math.exp(-0.5 * t_pos**2)

        # Add realistic noise
        noise = np.random.normal(0, 0.015)
        return ecg_value + noise

    def update(self):
        """Generate next ECG sample"""
        new_sample = self.generate_ecg_sample(self.current_time)
        self.ecg_buffer.append(new_sample)
        self.current_time += self.time_step
        return new_sample

    def get_display_data(self):
        """Get ECG data for display"""
        return list(self.ecg_buffer)

    def calculate_heart_rate(self):
        """Calculate heart rate from R-wave detection"""
        data = list(self.ecg_buffer)[-self.sample_rate * 3:]  # Last 3 seconds

        if len(data) < self.sample_rate:
            return self.heart_rate

        # Simple R-wave detection
        peaks = []
        threshold = 0.6
        min_distance = int(0.4 * self.sample_rate)  # Min 0.4s between beats

        for i in range(2, len(data) - 2):
            if (data[i] > threshold and
                data[i] > data[i - 1] and data[i] > data[i + 1] and
                    data[i] > data[i - 2] and data[i] > data[i + 2]):

                if not peaks or i - peaks[-1] >= min_distance:
                    peaks.append(i)

        if len(peaks) >= 2:
            intervals = [peaks[i + 1] - peaks[i] for i in range(len(peaks) - 1)]
            avg_interval = np.mean(intervals) / self.sample_rate
            calculated_hr = 60.0 / avg_interval if avg_interval > 0 else self.heart_rate
            return int(np.clip(calculated_hr, 30, 200))

        return self.heart_rate
