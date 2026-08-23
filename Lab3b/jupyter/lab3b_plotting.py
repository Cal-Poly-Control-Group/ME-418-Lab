"""Provided plotting and continuous-simulation helpers for ME 418 Lab 3B.

Students do not need to modify this file. The notebook keeps the required
engineering calculations visible while this module handles implementation
details that are not part of the assignment.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def _first_order_magnitude(f_hz, fc_hz):
    """Return the magnitude ratio of a first-order low-pass filter."""
    f_hz = np.asarray(f_hz, dtype=float)
    return 1.0 / np.sqrt(1.0 + (f_hz / fc_hz) ** 2)


def _apply_continuous_lowpass(x, t_s, fc_hz):
    """Simulate the continuous first-order transfer function."""
    tau_s = 1.0 / (2.0 * np.pi * fc_hz)
    system = signal.TransferFunction([1.0], [tau_s, 1.0])
    # scipy.signal uses a scaled internal state for this transfer function,
    # so X0 = y(0)*tau initializes the filter output at the first sample.
    _, y, _ = signal.lsim(system, U=x, T=t_s, X0=float(x[0]) * tau_s)
    return y


def _amplitude_spectrum(x, fs_hz):
    """Return positive frequencies and their approximate amplitudes."""
    x = np.asarray(x)
    n = len(x)
    window = np.hanning(n)
    coherent_gain = np.mean(window)
    spectrum = np.fft.rfft((x - np.mean(x)) * window)
    amplitude = 2.0 * np.abs(spectrum) / (n * coherent_gain)
    amplitude[0] *= 0.5
    frequency = np.fft.rfftfreq(n, d=1.0 / fs_hz)
    return frequency, amplitude


def plot_measurement_and_spectrum(
    t_s, x_reference, x_measured, fs_hz, time_limit_s=8.5, frequency_limit_hz=30.0
):
    """Plot the reference and measured signals in time and frequency."""
    fig, axes = plt.subplots(2, 1, figsize=(10, 7))

    time_mask = t_s <= time_limit_s
    axes[0].plot(t_s[time_mask], x_reference[time_mask],
                 label="Reference signal", linewidth=2)
    axes[0].plot(t_s[time_mask], x_measured[time_mask],
                 label="Measured", alpha=0.75)
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Signal amplitude (V)")
    axes[0].set_title("Reference and noisy electrical signals")
    axes[0].legend()

    f_reference, a_reference = _amplitude_spectrum(x_reference, fs_hz)
    f_measured, a_measured = _amplitude_spectrum(x_measured, fs_hz)
    frequency_mask = f_measured <= frequency_limit_hz
    axes[1].plot(f_reference[frequency_mask], a_reference[frequency_mask],
                 label="Reference", linewidth=2)
    axes[1].plot(f_measured[frequency_mask], a_measured[frequency_mask],
                 label="Measured", alpha=0.8)
    axes[1].set_xlabel("Frequency (Hz)")
    axes[1].set_ylabel("Approximate amplitude (V)")
    axes[1].set_title("Amplitude spectrum")
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def plot_first_order_frequency_response(
    fc_hz, signal_bandwidth_hz, interference_frequency_hz
):
    """Plot a first-order low-pass magnitude response in decibels."""
    frequency_hz = np.linspace(0.0, 30.0, 600)
    magnitude = _first_order_magnitude(frequency_hz, fc_hz)
    magnitude_db = 20.0 * np.log10(magnitude)
    interference_db = 20.0 * np.log10(
        _first_order_magnitude(interference_frequency_hz, fc_hz)
    )

    plt.figure(figsize=(9, 4.8))
    plt.plot(frequency_hz, magnitude_db, linewidth=2)
    plt.axvspan(0.0, signal_bandwidth_hz, color="tab:green", alpha=0.15,
                label=f"Useful signal: 0--{signal_bandwidth_hz:g} Hz")
    plt.axvline(fc_hz, color="tab:red", linestyle="--",
                label=f"fc = {fc_hz:g} Hz")
    plt.plot(interference_frequency_hz, interference_db, "o", color="tab:orange",
             label=f"{interference_frequency_hz:g} Hz periodic interference")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.title("First-order low-pass frequency response")
    plt.xlim(0.0, 30.0)
    plt.ylim(-18.0, 1.0)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_candidate_frequency_responses(
    candidate_fc_hz,
    signal_frequency_hz,
    interference_frequency_hz,
    min_signal_ratio,
    max_interference_ratio,
):
    """Compare candidate low-pass responses against two design requirements."""
    frequency_hz = np.linspace(0.0, 30.0, 800)
    signal_limit_db = 20.0 * np.log10(min_signal_ratio)
    interference_limit_db = 20.0 * np.log10(max_interference_ratio)

    fig, axis = plt.subplots(figsize=(10, 5.5))

    for fc_hz in candidate_fc_hz:
        magnitude = _first_order_magnitude(frequency_hz, fc_hz)
        magnitude_db = 20.0 * np.log10(magnitude)
        line, = axis.plot(
            frequency_hz,
            magnitude_db,
            linewidth=2,
            label=rf"$f_c={fc_hz:g}$ Hz",
        )
        color = line.get_color()
        marker_frequencies = np.array(
            [signal_frequency_hz, interference_frequency_hz]
        )
        marker_db = 20.0 * np.log10(
            _first_order_magnitude(marker_frequencies, fc_hz)
        )
        axis.plot(
            marker_frequencies,
            marker_db,
            "o",
            color=color,
            markersize=6,
        )

    axis.axvline(
        signal_frequency_hz,
        color="0.35",
        linestyle=":",
        linewidth=1.3,
    )
    axis.axvline(
        interference_frequency_hz,
        color="0.35",
        linestyle=":",
        linewidth=1.3,
    )
    axis.plot(
        signal_frequency_hz,
        signal_limit_db,
        marker="v",
        color="black",
        markersize=8,
        linestyle="None",
        label=(
            rf"At {signal_frequency_hz:g} Hz: magnitude must be "
            rf"$\geq {min_signal_ratio:.2f}$ ({signal_limit_db:.1f} dB)"
        ),
    )
    axis.plot(
        interference_frequency_hz,
        interference_limit_db,
        marker="^",
        color="black",
        markersize=8,
        linestyle="None",
        label=(
            rf"At {interference_frequency_hz:g} Hz: magnitude must be "
            rf"$\leq {max_interference_ratio:.2f}$ "
            rf"({interference_limit_db:.1f} dB)"
        ),
    )

    axis.annotate(
        "candidate point must lie above this marker",
        xy=(signal_frequency_hz, signal_limit_db),
        xytext=(3.7, -4.8),
        arrowprops={"arrowstyle": "->", "color": "0.3"},
        fontsize=9,
    )
    axis.annotate(
        "candidate point must lie below this marker",
        xy=(interference_frequency_hz, interference_limit_db),
        xytext=(12.0, -17.0),
        arrowprops={"arrowstyle": "->", "color": "0.3"},
        fontsize=9,
    )

    axis.set_xlabel("Frequency (Hz)")
    axis.set_ylabel("Magnitude (dB)")
    axis.set_title("Candidate first-order low-pass filters")
    axis.set_xlim(0.0, 30.0)
    axis.set_ylim(-25.0, 1.0)
    axis.legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    plt.show()


def plot_continuous_filter_candidates(
    t_s, x_reference, x_measured, candidate_fc_hz, time_limit_s=8.5
):
    """Compare continuous low-pass outputs for several cutoff frequencies."""
    fig, axes = plt.subplots(
        len(candidate_fc_hz), 1, figsize=(10, 9), sharex=True
    )
    time_mask = t_s <= time_limit_s

    for axis, fc_hz in zip(axes, candidate_fc_hz):
        y_continuous = _apply_continuous_lowpass(x_measured, t_s, fc_hz)
        axis.plot(t_s[time_mask], x_reference[time_mask],
                  label="Reference", linewidth=2)
        axis.plot(t_s[time_mask], x_measured[time_mask],
                  label="Measured", alpha=0.35)
        axis.plot(t_s[time_mask], y_continuous[time_mask],
                  label="Filtered", linewidth=1.7)
        axis.set_ylabel("Signal amplitude (V)")
        axis.set_title(f"Continuous filter: fc = {fc_hz:g} Hz")
        axis.legend(loc="upper right", ncol=3)

    axes[-1].set_xlabel("Time (s)")
    plt.tight_layout()
    plt.show()


def plot_filter_comparison(
    t_s, x_reference, x_measured, y_digital, fc_hz, time_limit_s=8.5
):
    """Compare the continuous simulation with the iterative digital filter."""
    y_continuous = _apply_continuous_lowpass(x_measured, t_s, fc_hz)
    time_mask = t_s <= time_limit_s
    plt.figure(figsize=(10, 5))
    plt.plot(t_s[time_mask], x_reference[time_mask],
             label="Reference", linewidth=2.2)
    plt.plot(t_s[time_mask], x_measured[time_mask],
             label="Measured", alpha=0.25)
    plt.plot(t_s[time_mask], y_continuous[time_mask],
             label="Continuous simulation", linewidth=1.8)
    plt.plot(t_s[time_mask], y_digital[time_mask], "--",
             label="Student digital filter", linewidth=1.6)
    plt.xlabel("Time (s)")
    plt.ylabel("Signal amplitude (V)")
    plt.title(f"Continuous and student digital filters, fc = {fc_hz:g} Hz")
    plt.legend(ncol=2)
    plt.tight_layout()
    plt.show()


def plot_step_responses(step_results):
    """Plot precomputed step responses and their 90-percent rise times."""
    plt.figure(figsize=(9, 4.8))
    for result in step_results:
        plt.plot(
            result["time_s"], result["output"],
            label=(
                f"fc={result['fc_hz']:g} Hz; "
                f"t90={result['t_90_s']:.3f} s"
            ),
        )

    reference = step_results[-1]
    plt.plot(reference["time_s"], reference["input"],
             color="black", linestyle=":", label="Unit-step input")
    plt.axhline(0.90, color="0.5", linestyle="--", label="90%")
    plt.xlim(0.0, 0.5)
    plt.ylim(-0.05, 1.05)
    plt.xlabel("Time (s)")
    plt.ylabel("Response")
    plt.title("Filter step response and delay")
    plt.legend()
    plt.tight_layout()
    plt.show()
