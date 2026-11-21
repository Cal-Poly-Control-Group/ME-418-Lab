"""Provided first-order digital low-pass filter for Lab 6A."""

import math


class FirstOrderLowPass:
    """Implement the first-order low-pass update derived in Lab 5B."""

    def __init__(self, cutoff_hz, delta_t, initial_value=0.0):
        time_constant_s = 1.0 / (2.0 * math.pi * cutoff_hz)
        self._coefficient = delta_t / (time_constant_s + delta_t)
        self._output = initial_value

    def filter(self, measured_value):
        """Run one iterative filter update and return the filtered value."""

        self._output += self._coefficient * (
            measured_value - self._output
        )
        return self._output
