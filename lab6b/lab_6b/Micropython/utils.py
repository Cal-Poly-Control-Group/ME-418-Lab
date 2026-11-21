"""Feedforward pulse controller and Thonny Shell motor test for Lab 6B."""

# Shared sampling period for the hardware test and main.py (about 150 Hz).
PERIOD_US = 6667


class FeedforwardPulse:
    """Return an open-loop pulse at a fixed sampling interval."""

    def __init__(self, pulse_width, delta_t):
        self.pulse_width = pulse_width
        self.t = 0
        # TODO 1: Store a pulse amplitude of 100 percent and the sample period.

    def run(self, x=0):
        """Advance the pulse clock and return the motor command in percent.

        x is accepted for compatibility with the PID controller interface.
        """
        # TODO 2: Advance the clock and output the pulse until its width expires.


def test_motor_pulse(pulse_width=0.05):
    """Apply a pulse of the requested width in seconds to motor A."""
    import motor
    import utime

    delta_t = PERIOD_US / 1e6
    pulse = FeedforwardPulse(pulse_width, delta_t)
    max_updates = int(pulse_width / delta_t) + 1
    driver = motor.MotorDriver()
    motor_a = driver.motorA

    motor_a.set_voltage_percent(0)
    motor_a.enable()
    for _ in range(max_updates):
        output = pulse.run()
        if output == 0:
            break
        motor_a.set_voltage_percent(output)
        utime.sleep_us(PERIOD_US)
    motor_a.disable()
