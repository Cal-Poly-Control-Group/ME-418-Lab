"""Provided first-order digital low-pass filter for Lab 5B."""

import math


class FirstOrderLowPass:
    """Implement the first-order low-pass update derived in Lab 3B."""

    def __init__(self, cutoff_hz, delta_t, initial_value=0.0):
        """Initialize the filter.

        Args:
            cutoff_hz: Filter cutoff frequency in hertz.
            delta_t: Fixed time between samples in seconds.
            initial_value: Filter output before the first update.
        """

        time_constant_s = 1.0 / (2.0 * math.pi * cutoff_hz)
        self._coefficient = delta_t / (time_constant_s + delta_t)
        self._output = initial_value

    def filter(self, measured_value):
        """Filter one new measurement and return the updated output."""

        self._output += self._coefficient * (
            measured_value - self._output
        )
        return self._output
