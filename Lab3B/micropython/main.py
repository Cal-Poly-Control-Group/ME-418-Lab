import array
import utime
import pyb
import encoder
import motor
import controller

###############################################################################
# 1. PC -> MICROCONTROLLER COMMUNICATION (PARAMETER VALUES).
# This code reads values from the serial port for gains, velocity to step to,
# and total time to run the test for. No need to modify anything.
while True:
    try:
        kp = float(input("kp: [voltage percent per rad/s of error]: "))
        ki = float(input("ki: [voltage percent per rad of integral]: "))
        sp = float(input("Velocity setpoint to step to [rad/s]: "))
        out_max = float(input("Maximum motor voltage [percent]: "))
        t_total = float(input("Total test time [ms]: "))
    except ValueError:
        print("Invalid input")
        continue
    else:
        break

###############################################################################
# 2. OBJECT/VARIABLE SETUP
# This code sets up motor driver and encoder objects (same as lab 1A).
driver = motor.MotorDriver()
driver.motorA.enable()

encoder = encoder.Encoder(4, pyb.Pin.cpu.B6, pyb.Pin.cpu.B7)
encoder.zero()

# This code creates arrays for time, velocity data, and control command data.
# Units should be microseconds, rad/s, and percent voltage
time_array = array.array('f')
vel_array = array.array('f')
percent_array = array.array('f')
p_array = array.array('f')
i_array = array.array('f')

# This sets up variables used to run the timed loop at 500Hz. Units are
# microseconds for all variables ending in _us
period_us = 2000
test_time_us =  int(t_total * 1000)
start_time_us = utime.ticks_us()
next_time_us = start_time_us
delta_t = period_us / 1e6 # convert to seconds

# This determines how often to collect data. The desired number of data
# points for a graph is about 500-1000. The variable 'every' controls how
# many controller runs happen for each data point, for example, data is
# collected every 5 runs, 10 runs, etc. This is necessary because
# Collecting too much data can cause the microcontroller to run out of memory.
every = test_time_us // (period_us * 500)
every = 1 if every == 0 else every
n_runs = 0

###############################################################################
# WRITE YOUR CODE HERE to create the PI controller object. Use the parameters
# collected from the serial port in the above section.

# Set the controller gains (may need to change object name)
# con.set_gains(kp, ki)

###############################################################################
# 3. CLOSED LOOP STEP RESPONSE
# WRITE YOUR CODE HERE to set the velocity setpoint to the value read from the
# serial port.


# The next 3 lines are responsible for running the timed loop.
while utime.ticks_diff(utime.ticks_us(), start_time_us) <= test_time_us:
    if utime.ticks_diff(utime.ticks_us(), next_time_us) >= 0:
        next_time_us = utime.ticks_add(next_time_us, period_us)
        # Any code written here will be run at 500Hz maximum.
        # Read the current encoder velocity in rad/s.
        vel = encoder.get_velocity_rad()
        
        # WRITE YOUR CODE HERE to to run the controller, storing the percent
        # voltage in a variable, so it can be added to the data later.

        
        # WRITE YOUR CODE HERE to set the voltage percent on the motor.

        
        # This if-statement checks if it is time to collect data.
        if n_runs % every == 0:
            # WRITE YOUR CODE HERE to gather the controller actions from the
            # get_PI_components method of the PIController.

            
            # Store the time for this run in the time array.
            time_array.append(delta_t * n_runs)
            # WRITE YOUR CODE HERE to append the values to the other arrays.
            vel_array.append(vel)


        # Increment the counter for number of runs.
        n_runs += 1
    
# Stop the motor.
driver.motorA.set_voltage_percent(0)
##############################################################################

# 3. MICROCONTROLLER -> PC COMMUNICATION (TEST DATA).
# This code prints the data to the computer.
for i in range(len(time_array)):
    print(time_array[i], vel_array[i], percent_array[i], p_array[i], i_array[i],
          sep=',')
print('END')
