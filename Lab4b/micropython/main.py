"""Lab 4B starter code: closed-loop PI-controller experiment."""

import sys
import cqueue
import utime
import pyb
import encoder
import motor
import controller


# -----------------------------------------------------------------------------
# Hardware initialization — provided code; do not modify.
# -----------------------------------------------------------------------------

driver = motor.MotorDriver()
enc = encoder.Encoder(4, pyb.Pin.cpu.B6, pyb.Pin.cpu.B7)

PERIOD_US = 2000
DELTA_T_S = PERIOD_US / 1e6
QUEUE_CAPACITY = 1000

print("READY LAB4B_SERIAL_V1")


# Keep waiting for commands until the board is stopped or reset.
while True:
    line = sys.stdin.readline().strip()

    if line == "":
        continue

    print("ACK")
    parts = line.split()

    if parts[0].upper() == "RUN_CONTROLLER" and len(parts) == 6:
        # ---------------------------------------------------------------------
        # Read experiment parameters — provided code; do not modify.
        # ---------------------------------------------------------------------

        kp = float(parts[1])
        ki = float(parts[2])
        setpoint_rad_s = float(parts[3])
        output_limit_percent = float(parts[4])
        test_time_ms = float(parts[5])

        print("OK")

        # ---------------------------------------------------------------------
        # Set up this experiment — provided code; do not modify.
        # ---------------------------------------------------------------------

        test_time_us = int(test_time_ms * 1000)

        time_queue = cqueue.FloatQueue(QUEUE_CAPACITY)
        velocity_queue = cqueue.FloatQueue(QUEUE_CAPACITY)
        output_queue = cqueue.FloatQueue(QUEUE_CAPACITY)
        p_queue = cqueue.FloatQueue(QUEUE_CAPACITY)
        i_queue = cqueue.FloatQueue(QUEUE_CAPACITY)

        # Store approximately 500 points, even during a longer experiment.
        store_every = test_time_us // (PERIOD_US * 500)
        if store_every < 1:
            store_every = 1

        driver.motorA.enable()
        enc.zero()

        # ---------------------------------------------------------------------
        # Configure the PI controller.
        # ---------------------------------------------------------------------

        # TODO 1: Create a PIController object. Initialize its gains and
        # setpoint to zero. Use output_limit_percent and DELTA_T_S for the
        # output limit and controller period.


        # TODO 2: Set the proportional and integral gains using kp and ki.


        # TODO 3: Set the velocity setpoint using setpoint_rad_s.


        # ---------------------------------------------------------------------
        # Closed-loop step-response experiment.
        # ---------------------------------------------------------------------

        start_time_us = utime.ticks_us()
        next_time_us = start_time_us
        n_runs = 0

        while utime.ticks_diff(
            utime.ticks_us(), start_time_us
        ) <= test_time_us:
            current_time_us = utime.ticks_us()

            if utime.ticks_diff(current_time_us, next_time_us) >= 0:
                next_time_us = utime.ticks_add(next_time_us, PERIOD_US)

                velocity_rad_s = enc.get_velocity_rad()

                # TODO 4: Run the controller using the measured velocity and
                # store the returned voltage percentage.


                # TODO 5: Apply the controller output to motor A.


                if n_runs % store_every == 0:
                    # TODO 6: Get the proportional and integral actions from
                    # the controller.


                    time_queue.put(DELTA_T_S * n_runs)
                    velocity_queue.put(velocity_rad_s)

                    # TODO 7: Store the total, proportional, and integral
                    # controller outputs in their queues.


                n_runs += 1

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
                velocity_queue.get(),
                output_queue.get(),
                p_queue.get(),
                i_queue.get(),
                sep=",",
            )
            utime.sleep_ms(1)

    else:
        print(
            "ERR usage: RUN_CONTROLLER "
            "<kp> <ki> <setpoint> <output_limit> <test_time_ms>"
        )

    print("END")
