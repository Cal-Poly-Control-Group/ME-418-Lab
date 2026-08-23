"""Utilities for generating the Lab 5A linear sine sweep."""

import math


def sweep_gen(amplitude, f_start_hz, f_end_hz, sweep_time_s, number_of_points):
    """Yield time and sine-sweep values one sample at a time.

    The instantaneous frequency increases linearly from f_start_hz to
    f_end_hz during sweep_time_s.

    Args:
        amplitude: Peak amplitude of the generated sweep.
        f_start_hz: Starting frequency in Hz.
        f_end_hz: Ending frequency in Hz.
        sweep_time_s: Total sweep time in seconds.
        number_of_points: Total number of samples in the sweep.

    Yields:
        Tuples containing time in seconds and the corresponding sweep value.
    """

    for index in range(number_of_points):
        # TODO 1: Calculate the time for this sample and store it in time_s.


        # TODO 2: Calculate the sine-wave phase in radians and store it in
        # phase_rad. Use the linear-frequency sweep equation from the manual.


        # TODO 3: Calculate the sweep value and store it in sweep_value.


        yield time_s, sweep_value


# Run this file with Local Python 3 to check the completed generator.
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    times = []
    values = []

    for time_s, sweep_value in sweep_gen(100, 1, 10, 2, 300):
        times.append(time_s)
        values.append(sweep_value)

    plt.plot(times, values)
    plt.xlabel("Time [s]")
    plt.ylabel("Sweep value")
    plt.title("Sine Sweep: 1–10 Hz")
    plt.tight_layout()
    plt.show()
