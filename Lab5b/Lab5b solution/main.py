import cqueue
import utime
import pyb
import encoder
import motor
import controller
###############################################################################
# 1. PC -> MICROCONTROLLER COMMUNICATION (PARAMETER VALUES).
# This code reads values from the serial port for gains, position to step to,
# and total time to run the test for. No need to modify anything.
while True:
    try:
        kp = float(input("kp: [voltage percent per rad of error]: "))
        ki = float(input("ki: [voltage percent per rad-s of integral]: "))
        kd = float(input("kd: [voltage percent per rad/s of derivative]: "))
        sp = float(input("Position setpoint to step to [rad]: "))
        out_max = float(input("Maximum motor voltage [percent]: "))
        t_step = float(input("Total test time [ms]: "))
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

# This code creates queues for time, position data, and control command data.
# Units should be microseconds, rad/s, and percent voltage
time_queue = cqueue.FloatQueue(1000)
pos_queue = cqueue.FloatQueue(1000)
percent_queue = cqueue.FloatQueue(1000)
p_queue = cqueue.FloatQueue(1000)
i_queue = cqueue.FloatQueue(1000)
d_queue = cqueue.FloatQueue(1000)

# This sets up variables used to run the timed loop at 250Hz. Units are
# microseconds for all variables ending in _us
period_us = 5000
test_time_us =  int(t_step * 1000)
start_time_us = utime.ticks_us()
next_time_us = start_time_us
delta_t = period_us / 1e6 # convert microseconds to seconds

# This determines how often to collect data. The desired number of data
# points for a graph is about 500-1000. The variable 'every' controls how
# many controller runs happen for each data point, for example, data is
# collected every 5 runs, 10 runs, etc.
every = test_time_us // (period_us * 500)
every = 1 if every == 0 else every
n_runs = 0

###############################################################################
# WRITE YOUR CODE HERE to create the PI controller object. Use the parameters
# collected from the serial port in the above section.
controller = controller.PIDController(kp, ki, kd, out_max, delta_t, sp);

###############################################################################
# 3. CLOSED LOOP STEP RESPONSE
# WRITE YOUR CODE HERE to set the position setpoint to the value read from the
# serial port.
controller.set_setpoint(sp)

# The next 3 lines are responsible for running the timed loop.
while utime.ticks_diff(utime.ticks_us(), start_time_us) <= test_time_us:
    if utime.ticks_diff(utime.ticks_us(), next_time_us) >= 0:
        next_time_us = utime.ticks_add(next_time_us, period_us)
        # Any code written here will be run at 250Hz maximum.
        # Read the current time in microseconds,
        # and the current position in rad/s
        t = n_runs * delta_t
        pos = encoder.get_position_rad()
        # Run the controller and set the resulting voltage percent on the motor.
        percent = controller.run(pos)
        driver.motorA.set_voltage_percent(percent)
        
        if n_runs % every == 0:
            # Data collection 
            p_part, i_part, d_part = controller.get_PID_actions()
            # This stores the data in the queues
            time_queue.put(t)
            pos_queue.put(pos)
            percent_queue.put(percent)
            p_queue.put(p_part)
            i_queue.put(i_part)
            d_queue.put(d_part)

        n_runs += 1
    
# Stop the motor
driver.motorA.disable()
# Print the data as CSV
while time_queue.any():
    print(time_queue.get(), pos_queue.get(), percent_queue.get(),
    p_queue.get(), i_queue.get(), d_queue.get(), sep=',')
print('END')