"""Contains classes for a motor driver and motors.

This module contains two classes, MotorDriver and Motor. These can be used
together to control DC motors through the IHM04A1 driver board attached to the
Nucleo. MotorDriver contains pin and timer assignments based on the connections
of the driver board. Motor is a general class which provides a method for
setting the percent cycle of a bidirectional DC motor, given two PWM channels.
Included in MotorDriver are two Motor objects for the motor connections
A and B, as labeled on the board.

Typical usage example:
    # Create a MotorDriver object
    driver = motor.MotorDriver()
    # Enable motor A
    driver.motorA.enable()
    # Set the voltage on motor A
    driver.motorA.set_voltage_percent(100)
"""

import pyb
import time


class MotorDriver:
    """Driver for the IHM04A1 DC motor driver Nucleo expansion board.

    This class contains pin assignments based on the connections made on
    the driver board. Timers 3 and 5, on channels 1 and 2, are available on
    these pins, so are used to generate PWM signals. 2 Motor objects are
    created, corresponding with the A and B motor connections.

    Attributes:
        motorA: 
            Motor object for the motor connected to the A terminals on the
            driver boad. See Motor class in same file for details.
        motorB:
            Motor object for the motor connected to the B terminals.
    """

    def __init__(self):
        # Pins
        ena_pin = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.OUT_PP)
        in1a_pin = pyb.Pin.cpu.B4
        in2a_pin = pyb.Pin.cpu.B5
        enb_pin = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)
        in1b_pin = pyb.Pin.cpu.A0
        in2b_pin = pyb.Pin.cpu.A1

        # Timers for connection to input pins, 20kHz to make inaudible
        timer_a = pyb.Timer(3, freq=20000)
        timer_b = pyb.Timer(5, freq=20000)

        # Timer channel objects connected to input pins
        in1a_channel = timer_a.channel(1, pyb.Timer.PWM, pin=in1a_pin)
        in2a_channel = timer_a.channel(2, pyb.Timer.PWM, pin=in2a_pin)
        in1b_channel = timer_b.channel(1, pyb.Timer.PWM, pin=in1b_pin)
        in2b_channel = timer_b.channel(2, pyb.Timer.PWM, pin=in2b_pin)

        self.motorA = Motor(in1a_channel, in2a_channel, ena_pin)
        self.motorB = Motor(in1b_channel, in2b_channel, enb_pin)

    # Disables both motors


class Motor:
    """Driver for DC motors controlled by PWM, with an enable pin.
    """

    def __init__(self, in1_channel, in2_channel, en_pin):
        """Initializes a motor given 2 PWM channels and an enable pin

        Args:
            in1_channel:
                1st PWM channel to use, for forward driving
            in2_channel:
                2nd PWM channel to use, for backward driving
            en_pin:
                Logic pin used to enable or disable the motor
        """
        self._in1_channel = in1_channel
        self._in2_channel = in2_channel
        self._en_pin = en_pin

    def set_voltage_percent(self, percent):
        """Set the PWM duty cycle applied to the motor.

        The average applied voltage to the motor will be the specified percent
        of the voltage of the motor driver power supply.

        Args:
            percent:
                The percent duty cycle to apply to the motor. This is positive
                for forward driving and negative for backward driving."""
        if 0 < percent <= 100:  # Forward
            self._in1_channel.pulse_width_percent(percent)
            self._in2_channel.pulse_width_percent(0)
        elif -100 <= percent < 0:  # Reverse
            self._in1_channel.pulse_width_percent(0)
            self._in2_channel.pulse_width_percent(-percent)
        elif percent == 0: # Stop
            self._in1_channel.pulse_width_percent(0)
            self._in2_channel.pulse_width_percent(0)
        else:
            raise ValueError("Invalid percentage {}%".format(percent))

    def enable(self):
        """Enables the motor.
        """
        self._en_pin.high()

    def disable(self):
        """Disables the motor.
        """
        self.set_voltage_percent(0)
        self._en_pin.low()