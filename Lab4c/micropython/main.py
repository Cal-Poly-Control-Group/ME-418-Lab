"""Lab 4C starter code: trapezoidal velocity-profile tracking."""

import sys
import cqueue
import motor
import encoder
import pyb
import utime
import controller
from profile import trapz_profile_gen, trapz_profile_length


# -----------------------------------------------------------------------------
# Hardware and controller constants — provided code; do not modify.
# -----------------------------------------------------------------------------

driver = motor.MotorDriver()
enc = encoder.Encoder(4, pyb.Pin.cpu.B6, pyb.Pin.cpu.B7)

PERIOD_US = 2000
DELTA_T_S = PERIOD_US / 1e6
OUTPUT_LIMIT_PERCENT = 100

print("READY LAB4C_SERIAL_V1")


# Keep waiting for commands until the board is stopped or reset.
while True:
    line = sys.stdin.readline().strip()

    if line == "":
        continue

    print("ACK")
    parts = line.split()

    if parts[0].upper() == "RUN_PROFILE" and len(parts) == 7:
        # ---------------------------------------------------------------------
        # Read experiment parameters — provided code; do not modify.
        # ---------------------------------------------------------------------

        omega_ss_rad_s = float(parts[1])
        steady_time_s = float(parts[2])
        acceleration_time_s = float(parts[3])
        stop_time_s = float(parts[4])
        kp = float(parts[5])
        ki = float(parts[6])

        print("OK")

        # ---------------------------------------------------------------------
        # Set up this experiment — provided code; do not modify.
        # ---------------------------------------------------------------------

        data_points = trapz_profile_length(
            omega_ss_rad_s,
            acceleration_time_s,
            steady_time_s,
            stop_time_s,
            DELTA_T_S,
        )

        time_queue = cqueue.FloatQueue(data_points)
        setpoint_queue = cqueue.FloatQueue(data_points)
        velocity_queue = cqueue.FloatQueue(data_points)

        con = controller.PIController(
            kp,
            ki,
            OUTPUT_LIMIT_PERCENT,
            DELTA_T_S,
            0,
        )

        driver.motorA.enable()
        enc.zero()

        next_time_us = utime.ticks_add(utime.ticks_us(), PERIOD_US)

        profile = trapz_profile_gen(
            omega_ss_rad_s,
            acceleration_time_s,
            steady_time_s,
            stop_time_s,
            DELTA_T_S,
        )

        # ---------------------------------------------------------------------
        # Profile-tracking experiment.
        # ---------------------------------------------------------------------

        for time_s, setpoint_rad_s in profile:
            velocity_rad_s = enc.get_velocity_rad()

            # TODO 1: Update the controller setpoint using setpoint_rad_s.


            # TODO 2: Run the controller using velocity_rad_s and store the
            # returned motor-voltage percentage.


            # TODO 3: Apply the controller output to motor A.


            # TODO 4: Store time_s, setpoint_rad_s, and velocity_rad_s in
            # their provided queues.


            # Maintain the 500 Hz controller period — provided code;
            # do not modify.
            while utime.ticks_diff(utime.ticks_us(), next_time_us) < 0:
                pass

            next_time_us = utime.ticks_add(next_time_us, PERIOD_US)

        # Stop the motor after every experiment — provided code; do not modify.
        driver.motorA.set_voltage_percent(0)
        driver.motorA.disable()

        # ---------------------------------------------------------------------
        # Send data to the PC — provided code; do not modify.
        # ---------------------------------------------------------------------

        while time_queue.any():
            print(
                "DATA",
                time_queue.get(),
                setpoint_queue.get(),
                velocity_queue.get(),
                sep=",",
            )
            utime.sleep_ms(1)

    else:
        print(
            "ERR usage: RUN_PROFILE "
            "<omega_ss> <steady_time> <acceleration_time> "
            "<stop_time> <kp> <ki>"
        )

    print("END")
