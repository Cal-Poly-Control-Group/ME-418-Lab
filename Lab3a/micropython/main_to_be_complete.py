"""Lab 3A starter code: simple text-based serial communication.

Upload this file to the Nucleo board as main.py. The program stays active,
processes one command at a time, and then waits for the next command.
"""

import sys
import utime
import pyb


# pyb.LED(1) is the green LED on the Nucleo board.
# pyb.Switch() reads the blue user button.
led = pyb.LED(1)
button = pyb.Switch()

# Tell the PC that main.py has started and is ready for one command.
print("READY LAB3A_SERIAL_V1")

# Keep waiting for commands until the board is stopped or reset.
while True:
    # readline() waits for one line from the PC or the Thonny shell.
    line = sys.stdin.readline()

    # strip() removes the Enter key characters at the end of the line.
    line = line.strip()

    # Ignore empty lines without sending a response.
    if line == "":
        continue

    # ACK means a complete command line was received.
    print("ACK")

    # split() separates a command such as "LED BLINK 5 2000" into words.
    parts = line.split()

    # upper() lets the user type "led on", "LED ON", or "Led On".
    command = parts[0].upper()

    if command == "LED":
        if len(parts) < 2:
            print("ERR LED command requires an action")

        else:
            # The second word tells us which LED action to run.
            action = parts[1].upper()

            if action == "ON":
                # TODO 1: Turn the LED on.
                # Then print OK so the PC knows the command worked.
                # Replace this pass with your code.
                pass

            elif action == "OFF":
                # TODO 2: Turn the LED off.
                # Then print OK.
                # Replace this pass with your code.
                pass

            elif action == "BLINK":
                if len(parts) != 4:
                    print("ERR usage: LED BLINK n dt_ms")

                else:
                    # TODO 3: Convert parts[2] and parts[3] to integers.
                    # parts[2] is the number of blinks.
                    # parts[3] is the delay time in milliseconds.
                    count = 0
                    delay_ms = 0

                    # TODO 4: Blink the LED count times.
                    # First turn the LED off so the starting state is known.
                    # For each blink, toggle the LED, wait delay_ms,
                    # toggle it again, and wait delay_ms again.
                    # After the loop, print OK.
                    # Replace this pass with your code.
                    pass

            else:
                print("ERR unknown LED action")

    elif command == "BUTTON?":
        # TODO 5: Read the blue user button.
        # First print OK.
        # Then print DATA BUTTON followed by 0 or 1.
        # Replace this pass with your code.
        pass

    else:
        print("ERR unknown command")

    # END marks the end of this command response for the PC.
    print("END")
