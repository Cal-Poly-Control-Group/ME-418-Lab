"""Lab 6B starter code: closed-loop inverted pendulum position control."""

import sys
import cqueue
import utime
import pyb
import encoder
import motor
import controller
from utils import PERIOD_US


# -----------------------------------------------------------------------------
# Hardware and controller timing — provided code; do not modify.
# -----------------------------------------------------------------------------

driver = motor.MotorDriver()
enc = encoder.Encoder(4, pyb.Pin.cpu.B6, pyb.Pin.cpu.B7)

DELTA_T_S = PERIOD_US / 1e6
MAX_RECORDED_POINTS = 600

print("READY LAB6B_SERIAL_V1")


# Keep waiting for commands until the board is stopped or reset.
while True:
    line = sys.stdin.readline().strip()

    if line == "":
        continue

    print("ACK")
    parts = line.split()

    if parts[0].upper() == "RUN" and len(parts) == 10:
        # ---------------------------------------------------------------------
        # Read experiment parameters — provided code; do not modify.
        # ---------------------------------------------------------------------

        pulse_width = float(parts[1])
        kp = float(parts[2])
        ki = float(parts[3])
        kd = float(parts[4])
        setpoint_rad = float(parts[5])
        test_time_s = float(parts[6])
        output_limit_percent = float(parts[7])
        encoder_init = float(parts[8])
        switch_angle = float(parts[9])

        print("OK")

        # ---------------------------------------------------------------------
        # Set up this experiment.
        # ---------------------------------------------------------------------

        # TODO 1: Create a SwitchedController named switched_controller using the received gains, output
        # limit, the provided DELTA_T_S, and the received setpoint_rad.

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
        # Closed-loop experiment.
        # ---------------------------------------------------------------------

        # TODO 2: Manually switch the controller mode to 1 (PID) using
        # the set_mode method. This is only used when testing PID control on its own.
                
        # TODO 3: Set encoder position to encoder_init. Notice set_position
        # method takes counts, not radians (see enc.rad_to_counts).
        
        # TODO 4: After testing PID control alone, switch the controller mode back to 0 (pulse)
        # using the set_mode method. This will be used to initialize the controller for the
        # swing-up phase.

        while utime.ticks_diff(utime.ticks_us(), start_time_us) <= test_time_us:
            if utime.ticks_diff(utime.ticks_us(), next_time_us) >= 0:
                next_time_us = utime.ticks_add(next_time_us, PERIOD_US)

                time_s = update_count * DELTA_T_S
                position_rad = enc.get_position_rad()
                
                # TODO 5: Implement switching logic to switch controller mode from 0
                # to 1 when position is within switch_angle radians of the setpoint.
                    
                # TODO 6: Print mode of switched_controller to test switching logic.

                # Calculate voltage percentage from controller and send to motor A.
                output_percent = switched_controller.run(position_rad)
                driver.motorA.set_voltage_percent(output_percent)

                if update_count % record_every == 0:
                    # Data collection - provided code; do not modify.
                    p_action, i_action, d_action = (
                        switched_controller.controller_1.get_PID_actions()
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
            "ERR usage: RUN "
            "<pulse_width> <kp> <ki> <kd> <setpoint_rad> <test_time_s> <output_limit> <encoder_init> <switch_angle>"
        )

    print("END")
