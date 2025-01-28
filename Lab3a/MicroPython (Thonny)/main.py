import cqueue   # data storage in a queue (from Dr. Ridgely)
import utime    # time related functions
import pyb      # functions related to the Nucleo board
import encoder  # quadrature encoder module
import motor    # motor, motor driver module

# -----------------------------------------------------------
# Initialization
# In this segment, you shall initialze the motor, encoder,
# and constants in the program. Then you shall create queues
# to store the time and velocity test data.
# -----------------------------------------------------------

# WRITE YOUR CODE HERE to create a motor object and enable the motor
# driver on motor A (see motor.py comments)

print('MOTOR INITIALIZED.') 

# 2. WRITE YOUR CODE HERE to creaze the encoder object and zero the encoder.
# (see encoder.py comments)


print('ENCODER INITIALIZED.')

# Constants relating to the timing of the test.
SAMPLING_PERIOD_US = 2000 # The sampling period, in microseconds. 
TEST_TIME_US =  1500_000 # The total time of the test, in microseconds.
DATA_POINTS = TEST_TIME_US // SAMPLING_PERIOD_US

# WRITE YOUR CODE HERE to create queues to store data. The time queue is done
# for you. The velocity queue needs to be a FloatQueue.
time_queue = cqueue.IntQueue(DATA_POINTS)


# -----------------------------------------------------------
# Main loop
# In this segment, you shall complete the code for step response
# test. In the main loop, the program will sample motor velocity 
# periodically, storing it as well as the associated time into the 
# data queues declared previously.
# -----------------------------------------------------------

# 1. WRITE YOUR CODE HERE to turn the motor on.


# These variables are used to run the timed loop. The loop should run at the 
# sampling period above and for the total test time above.
start_time = utime.ticks_us()
next_sampling_time = utime.ticks_add(start_time, SAMPLING_PERIOD_US)
current_time = start_time

# 2. Main Loop (timed)
# Runs while current time - start time <= total time
while utime.ticks_diff(utime.ticks_us(), start_time) <= TEST_TIME_US:
    # WRITE YOUR CODE HERE to read the time, using utime.ticks_us().


    # Use a "if" statement to maintain the constant sampling rate. You will
    # need to compare the time difference between current_time and
    # next_sampling_time using the "utime.ticks_diff" function.
    # If the difference is positive, then enough time has passed and data
    # should be collected.
    # WRITE YOUR CODE HERE to maintain sampling rate with an if-statement.

        # INSIDE OF THE IF STATEMENT
        # WRITE YOUR CODE HERE to update the next sampling time.


        # WRITE YOUR CODE HERE to read the motor velocity, using the encoder.


        # WRITE YOUR CODE HERE to put the data in the queues.
        # Example: time_queue.put(current_time)

    pass # Placeholder for empty while loop. Delete after adding your code.


# -----------------------------------------------------------
# Finishing
# In this part, you shall turn the motor off and transfer 
# data to the computer.
# -----------------------------------------------------------

# 3. WRITE YOUR CODE HERE to turn the motor off.

# 4. UNCOMMENT THE CODE BELOW to print the data.
# Be careful with indentation. You may need to replace the variables
# "time_queue" and "velocity_queue" with whatever you called those.

# while time_queue.any():
#    print(utime.ticks_diff(time_queue.get(), start_time) / 1e6,
#          velocity_queue.get(), sep=',')
#    utime.sleep_ms(1) # constant printing can cause errors in Thonny
# print('END')