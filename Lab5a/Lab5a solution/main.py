from sweep_utils import sweep_gen
import motor
import encoder
import pyb
import utime

# This code creates motor driver and encoder objects (same as lab 1A)
driver = motor.MotorDriver()
driver.motorA.enable()
enc = encoder.Encoder(4, pyb.Pin.cpu.B6, pyb.Pin.cpu.B7)
enc.zero()

# The amplitude of the sine sweep. The units are voltage percent. We want to
# use 100% of the power supply voltage at the peaks of the sweep wave.
amplitude = 100

# Collects all the parameters of the sine sweep, either from user input
# or from a jupyter notebook.
while True:
    try:
        f_start = float(input("Start (lowest) Frequency [Hz]: "))
        f_end = float(input("End (highest) Frequency [Hz]: "))
        interval = float(input("Sweep Time [s]: "))
        points = float(input("Total number of sweep points: "))
    except ValueError:
        print("Invalid input")
        continue
    else:
        break

# Calculates the period, in microseconds, to run the main loop at.
period_us = int(interval / points * 1e6)

# Used to keep the main loop running at the right period
next_time_us = utime.ticks_us() + period_us

# Main loop. t and percent are the outputs of the sine sweep generator.
profile = sweep_gen(amplitude, f_start, f_end, interval, points)
for t, percent in profile:
    # WRITE YOUR CODE HERE to set the percent voltage on the motor
    driver.motorA.set_voltage_percent(percent)

    # WRITE YOUR CODE HERE to record the position of the encoder
    position = enc.get_position_rad()
    
    # WRITE YOUR CODE HERE to print the time, percent voltage set on the motor,
    # and position of the encoder as comma-seperated-values.
    print(t, percent, position, sep=',')
    
    # Loop timing, DO NOT write code past this point in the for loop
    # Wait until it is time to run the next point. pass means do nothing.
    while utime.ticks_diff(utime.ticks_us(), next_time_us) < 0:
        pass
    # Calculate the next time to run the loop
    next_time_us = utime.ticks_add(next_time_us, period_us)

# Shut off the motor
driver.motorA.disable()
# Marker for data end, detected by Jupyter Notebook
print('END')