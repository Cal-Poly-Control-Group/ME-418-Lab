"""Lab 4A starter code: open-loop motor step-response test."""

import sys       # receive commands from the PC
import cqueue    # store test data in queues
import utime     # timing functions
import pyb       # Nucleo board functions
import encoder   # quadrature encoder module
import motor     # motor-driver module


# -----------------------------------------------------------------------------
# Hardware initialization
# Complete this section before running an experiment.
# -----------------------------------------------------------------------------

# TODO 1: Create a motor-driver object and enable motor A.
# See the example in motor.py.


print("MOTOR INITIALIZED")

# TODO 2: Create the encoder object and zero the encoder.
# See the example in encoder.py.


print("ENCODER INITIALIZED")


# -----------------------------------------------------------------------------
# Provided constants and serial interface — do not modify this section.
# -----------------------------------------------------------------------------

SAMPLING_PERIOD_US = 2000       # 500 Hz sampling rate
TEST_TIME_US = 1_500_000        # 1.5 s test duration
DATA_POINTS = TEST_TIME_US // SAMPLING_PERIOD_US

print("READY LAB4A_SERIAL_V1")


# Keep waiting for commands until the board is stopped or reset.
while True:
    line = sys.stdin.readline().strip()

    if line == "":
        continue

    print("ACK")
    parts = line.split()

    if (
        parts[0].upper() == "RUN_STEP"
        and len(parts) == 2
        and parts[1].isdigit()
        and 1 <= int(parts[1]) <= 100
    ):
        step_percent = int(parts[1])
        print("OK")

        # ---------------------------------------------------------------------
        # Set up this experiment — provided code; do not modify.
        # ---------------------------------------------------------------------

        time_queue = cqueue.IntQueue(DATA_POINTS)
        velocity_queue = cqueue.FloatQueue(DATA_POINTS)

        driver.motorA.enable()
        enc.zero()

        start_time = utime.ticks_us()
        next_sampling_time = utime.ticks_add(
            start_time, SAMPLING_PERIOD_US
        )

        # ---------------------------------------------------------------------
        # Step-response experiment
        # ---------------------------------------------------------------------

        # Apply the step input received from Jupyter — provided code;
        # do not modify.
        driver.motorA.set_voltage_percent(step_percent)

        while utime.ticks_diff(
            utime.ticks_us(), start_time
        ) <= TEST_TIME_US:
            # TODO 3: Read the current time using utime.ticks_us().


            # TODO 4: Use utime.ticks_diff() in an if statement to determine
            # whether the next sampling time has been reached.

                # Inside the if statement:
                # TODO 5: Update next_sampling_time using utime.ticks_add().


                # TODO 6: Read the motor velocity in rad/s.


                # TODO 7: Store the current time and velocity in the queues.


            pass  # Delete after adding your code to the timed loop.

        # TODO 8: Set the motor voltage to 0%, then disable motor A.


        # ---------------------------------------------------------------------
        # Send the data to the PC — provided code; do not modify.
        # ---------------------------------------------------------------------

        while time_queue.any():
            elapsed_time_s = (
                utime.ticks_diff(time_queue.get(), start_time) / 1e6
            )
            print(
                "DATA",
                elapsed_time_s,
                velocity_queue.get(),
                sep=",",
            )
            utime.sleep_ms(1)

    else:
        print("ERR usage: RUN_STEP <integer percent from 1 to 100>")

    print("END")
