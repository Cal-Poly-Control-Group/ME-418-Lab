"""Lab 5A starter code: sine-sweep frequency-response experiment."""

import sys
import motor
import encoder
import pyb
import utime
from sweep_utils import sweep_gen


# -----------------------------------------------------------------------------
# Hardware initialization — provided code; do not modify.
# -----------------------------------------------------------------------------

driver = motor.MotorDriver()
enc = encoder.Encoder(4, pyb.Pin.cpu.B6, pyb.Pin.cpu.B7)

print("READY LAB5A_SERIAL_V1")


# Keep waiting for commands until the board is stopped or reset.
while True:
    line = sys.stdin.readline().strip()

    if line == "":
        continue

    print("ACK")
    parts = line.split()

    if parts[0].upper() == "RUN_SWEEP" and len(parts) == 6:
        # ---------------------------------------------------------------------
        # Read experiment parameters — provided code; do not modify.
        # ---------------------------------------------------------------------

        amplitude_percent = float(parts[1])
        f_start_hz = float(parts[2])
        f_end_hz = float(parts[3])
        sweep_time_s = float(parts[4])
        sample_rate_hz = float(parts[5])

        number_of_points = int(sweep_time_s * sample_rate_hz)
        period_us = int(1e6 / sample_rate_hz)

        print("OK")

        # ---------------------------------------------------------------------
        # Set up this experiment — provided code; do not modify.
        # ---------------------------------------------------------------------

        driver.motorA.set_voltage_percent(0)
        driver.motorA.enable()
        enc.zero()

        next_time_us = utime.ticks_add(utime.ticks_us(), period_us)

        sweep_profile = sweep_gen(
            amplitude_percent,
            f_start_hz,
            f_end_hz,
            sweep_time_s,
            number_of_points,
        )

        # ---------------------------------------------------------------------
        # Sine-sweep experiment.
        # ---------------------------------------------------------------------

        for time_s, voltage_percent in sweep_profile:
            # TODO 1: Apply voltage_percent to motor A.


            # TODO 2: Read the encoder position in radians and store it in
            # position_rad.


            # Send this sample to the PC — provided code; do not modify.
            print("DATA", time_s, voltage_percent, position_rad, sep=",")

            # Maintain the requested sample rate — provided code; do not modify.
            while utime.ticks_diff(utime.ticks_us(), next_time_us) < 0:
                pass

            next_time_us = utime.ticks_add(next_time_us, period_us)

        # Stop the motor after every experiment — provided code; do not modify.
        driver.motorA.set_voltage_percent(0)
        driver.motorA.disable()

    else:
        print(
            "ERR usage: RUN_SWEEP "
            "<amplitude> <f_start> <f_end> <sweep_time> <sample_rate>"
        )

    print("END")
