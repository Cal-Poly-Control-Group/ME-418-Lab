"""Lab 6A starter code: closed-loop pendulum position control."""

import sys
import cqueue
import utime
import pyb
import encoder
import motor
import controller


# -----------------------------------------------------------------------------
# Hardware and controller timing — provided code; do not modify.
# -----------------------------------------------------------------------------

driver = motor.MotorDriver()
enc = encoder.Encoder(4, pyb.Pin.cpu.B6, pyb.Pin.cpu.B7)

# The controller runs at approximately 150 Hz. Keep this period fixed.
PERIOD_US = 6667
DELTA_T_S = PERIOD_US / 1e6
MAX_RECORDED_POINTS = 600

print("READY LAB6A_SERIAL_V1")


# Keep waiting for commands until the board is stopped or reset.
while True:
    line = sys.stdin.readline().strip()

    if line == "":
        continue

    print("ACK")
    parts = line.split()

    if parts[0].upper() == "RUN_PID" and len(parts) == 7:
        # ---------------------------------------------------------------------
        # Read experiment parameters — provided code; do not modify.
        # ---------------------------------------------------------------------

        kp = float(parts[1])
        ki = float(parts[2])
        kd = float(parts[3])
        setpoint_rad = float(parts[4])
        test_time_s = float(parts[5])
        output_limit_percent = float(parts[6])

        print("OK")

        # ---------------------------------------------------------------------
        # Set up this experiment.
        # ---------------------------------------------------------------------

        # TODO 1: Create a PIDController using the received gains, output
        # limit, the provided DELTA_T_S, and the received setpoint_rad.


        # Skip filtering during the initial P and PD tests. After saving an
        # unfiltered PD response in Section 6A.3.3, go to Section 6A.3.4
        # (PD Control with First-Order Low-Pass Filtering) and complete the
        # FILTERED PD MODIFICATION comments in controller.py.

        test_time_us = int(test_time_s * 1e6)
        total_updates = int(test_time_s / DELTA_T_S) + 1
        record_every = (
            total_updates + MAX_RECORDED_POINTS - 1
        ) // MAX_RECORDED_POINTS
        record_every = 1 if record_every == 0 else record_every

        time_queue = cqueue.FloatQueue(MAX_RECORDED_POINTS + 2)
        position_queue = cqueue.FloatQueue(MAX_RECORDED_POINTS + 2)
        output_queue = cqueue.FloatQueue(MAX_RECORDED_POINTS + 2)
        p_queue = cqueue.FloatQueue(MAX_RECORDED_POINTS + 2)
        i_queue = cqueue.FloatQueue(MAX_RECORDED_POINTS + 2)
        d_queue = cqueue.FloatQueue(MAX_RECORDED_POINTS + 2)

        driver.motorA.set_voltage_percent(0)
        driver.motorA.enable()
        enc.zero()

        start_time_us = utime.ticks_us()
        next_time_us = start_time_us
        update_count = 0

        # ---------------------------------------------------------------------
        # Closed-loop step-response experiment.
        # ---------------------------------------------------------------------

        while utime.ticks_diff(utime.ticks_us(), start_time_us) <= test_time_us:
            if utime.ticks_diff(utime.ticks_us(), next_time_us) >= 0:
                next_time_us = utime.ticks_add(next_time_us, PERIOD_US)

                time_s = update_count * DELTA_T_S
                position_rad = enc.get_position_rad()

                # TODO 2: Pass position_rad to pid_controller.run() and
                # store the returned voltage percentage in output_percent.


                # TODO 3: Apply output_percent to motor A.


                if update_count % record_every == 0:
                    # Data collection - provided code; do not modify.
                    p_action, i_action, d_action = (
                        pid_controller.get_PID_actions()
                    )

                    time_queue.put(time_s)
                    position_queue.put(position_rad)
                    output_queue.put(output_percent)
                    p_queue.put(p_action)
                    i_queue.put(i_action)
                    d_queue.put(d_action)


                update_count += 1

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
                position_queue.get(),
                output_queue.get(),
                p_queue.get(),
                i_queue.get(),
                d_queue.get(),
                sep=",",
            )
            utime.sleep_ms(1)

    else:
        print(
            "ERR usage: RUN_PID "
            "<kp> <ki> <kd> <setpoint_rad> <test_time_s> <output_limit>"
        )

    print("END")
