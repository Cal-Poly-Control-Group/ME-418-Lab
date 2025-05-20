from serial import Serial
import numpy as np
from matplotlib import pyplot as plt
import time
from serial.serialutil import SerialException

def plot_step(kp, ki, step_vel, filename):
    ''' Plot the step response

    Gives a subplot for the velocity vs time, and for the controller outputs
    vs time. Also places the gains on the plot title.

    Args:
        kp:         Proportional Gain
        ki:         Integral Gain
        step_vel:   Velocity to step to
    '''
    # Import the data from the file
    data = np.genfromtxt(filename, delimiter=',')
    times = data[:,0]
    velocities = data[:,1]
    percents = data[:,2]
    p_percents = data[:,3]
    i_percents = data[:,4]

    # Make a figure and set the size to 6x6 in
    fig = plt.figure()
    plt.rcParams['figure.figsize'] = (6, 6)

    # Plot the step response of position vs time on the top half
    plt.subplot(211)
    plt.plot(times, velocities)
    plt.hlines(step_vel, times[1], times[-1], colors='k', linestyles='dashed')
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [rad/s]")
    plt.title(f'Step Response: K_P = {kp}, K_I = {ki}')

    # Plot the proportional and integral components on the bottom half
    plt.subplot(212)
    plt.plot(times, p_percents, '--')
    plt.plot(times, i_percents, '--')
    plt.plot(times, percents)
    plt.ylim(-110, 110)
    plt.xlabel("Time [s]")
    plt.ylabel("Voltage percent")
    plt.title("Controller Output")
    plt.legend(['P Part', 'I Part', 'Total'])
    plt.tight_layout()

def run_step(kp, ki, step_vel, t_step, filename, out_max=100):
    # Parameter validation
    if not isinstance(kp, (int, float)) or not isinstance(ki, (int, float)):
        raise ValueError("Kp and Ki must be numbers")
    if not isinstance(step_vel, (int, float)):
        raise ValueError("Step velocity must be a number")
    if not isinstance(t_step, (int, float)) or t_step <= 0:
        raise ValueError("Test duration must be a positive number")
    if not isinstance(out_max, (int, float)) or out_max <= 0 or out_max > 100:
        raise ValueError("Maximum output must be a number between 0 and 100")

    # On this line, give the name of the serial port which the Nucleo
    # is connected to, as a string. This should be something like
    # 'COMx' for Windows and
    # '/dev/tty.usbmodemXXXX' for Mac.
    # See the bottom right corner of Thonny for the correct COM port to use.
    serport = 'COM16'
    
    try:
        print(f"Connecting to microcontroller port {serport}...")
        # Open the serial port, and give it the name ser.
        with Serial(serport, baudrate=115200, timeout=5) as ser:
            print("Connection successful! Restarting microcontroller...")
            # Restart the microcontroller
            ser.write(b'\x02\x04')
            print("Sending control parameters...")
            # Write the parameters to the microcontroller
            try:
                print(f"Sending Kp = {kp}")
                ser.write((str(kp) + '\r\n').encode())
                print(f"Sending Ki = {ki}")
                ser.write((str(ki) + '\r\n').encode())
                print(f"Sending target velocity = {step_vel} rad/s")
                ser.write((str(step_vel) + '\r\n').encode())
                print(f"Sending maximum output = {out_max}%")
                ser.write((str(out_max) + '\r\n').encode())
                print(f"Sending test duration = {t_step} ms")
                ser.write((str(t_step) + '\r\n').encode())
            except Exception as e:
                print(f"Error sending parameters: {str(e)}")
                raise

            print("Starting data collection...")
            # Open the data file for writing, and give it the name datafile
            try:
                with open(filename, 'w') as datafile:
                    data_points = 0
                    start_time = time.time()
                    while True:
                        # Add timeout check
                        if time.time() - start_time > 30:  # 30 seconds timeout
                            raise TimeoutError("Data collection timed out after 30 seconds")
                            
                        # Read the current line and decode from bytes to a string
                        line = ser.readline().decode()
                        # If the line starts with END, then we know the data is complete
                        if line[:3] == 'END':
                            print(f"Data collection complete! Collected {data_points} data points")
                            break
                        # If the line has a comma, it is a line of CSV data.
                        elif ',' in line:
                            datafile.write(line.strip() + '\n')
                            data_points += 1
                            if data_points % 100 == 0:
                                print(f"Collected {data_points} data points...")
                        # Check for error messages from microcontroller
                        elif "ERROR" in line:
                            raise RuntimeError(f"Microcontroller reported error: {line.strip()}")
            except Exception as e:
                print(f"Error during data collection: {str(e)}")
                raise

        print("Generating response plot...")
        try:
            plot_step(kp, ki, step_vel, filename)
            print("Done!")
        except Exception as e:
            print(f"Error generating plot: {str(e)}")
            raise

    except SerialException as e:
        print(f"Serial port error: {str(e)}")
        print("Please check if:")
        print("1. The microcontroller is properly connected")
        print("2. The correct port is selected")
        print("3. No other program is using the port")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise 