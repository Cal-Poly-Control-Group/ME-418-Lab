"""Driver for reading from quadrature encoders

Typical usage example:
    # Create encoder object
    enc = encoder.Encoder(4, pyb.Pin.cpu.B6, pyb.Pin.cpu.B7
    # Zero out encoder
    enc.zero()
    # Store the position of the encoder (must call often)
    pos = enc.get_position()
"""

import math
import utime
import pyb

PERIOD = 2 ** 16 # Maximum for the 16-bit timer
CPR = 256

class Encoder:
    """Driver for reading from quadrature encoders
    """
    def __init__(self, timer_number, ch_a_pin, ch_b_pin):
        """"Initializes an Encoder using a timer and two pins

        See the datasheet for the microcontroller to identify which pin and
        timer combinations are possible.

        Args:
            timer_number: The ID number of the timer which is to be used
            ch_a_pin: The Pin name that the A channel of the encoder is
                      connected to. Example: pyb.Pin.cpu.B7
            ch_b_pin: The Pin name that the B channel is connected to.
        """
        self._timer = pyb.Timer(timer_number, period=PERIOD - 1, prescaler=0)
        self._timer.channel(1, pyb.Timer.ENC_AB, pin=ch_a_pin)
        self._timer.channel(2, pyb.Timer.ENC_AB, pin=ch_b_pin)
        self._position = 0
        self._count = 0
        self._last_count = 0
        self.delta = 0
        self._time = utime.ticks_us()
        self._last_time = self._time
        
    def update(self):
        """Updates the variables necessary to track position and velocity.

        Must be called often to maintain accuracy. The encoder must be updated
        at least as often as it counts half the timer's period. Otherwise the
        timer can overflow or underflow. Some timers are 16-bits, and some are
        32-bits. PERIOD is set to the maximum for a 16-bit timer by default, so
        this should work with all timers. This corresponds with 32768 counts
        maximum before update() must be called again.
            
        The last position and last time are also stored, which is necessary
        to read velocity estimates from the encoder.
            
        The methods get_position() and get_velocity() will both call this
        method, but if these are not called often enough on their own,
        this method should be called as often as described above.
        """
        self._last_count = self._count
        self._count = self._timer.counter()
        self._last_time = self._time
        self._time = utime.ticks_us()
        
        delta_pos = self._count - self._last_count
        delta_t = self._time - self._last_time

        if delta_pos > PERIOD // 2: # Underflow
            delta_pos -= PERIOD
        elif delta_pos < -PERIOD // 2: # Overflow
            delta_pos += PERIOD

        self._last_position = self._position
        self._position += delta_pos
        self._velocity = delta_pos / delta_t * 1e6 # microseconds to seconds
    
    def get_position(self):
        """Updates the encoder and returns its position, in counts.
        
        Returns:
            The encoder position, in counts. See the encoder specifications for
            the number of counts per revolution. For quadrature encoders, there
            are 4 counts per quadrature cycle.
        """
        self.update()
        return self._position
    
    def set_position(self, new_position):
        """"Sets a new position of the encoder.
        
        This can be useful for synchronizing the encoder with something else.
        This will also reset the last positions and times used to calculate
        velocity, to avoid reporting incorrect velocities.
        Args:
            new_position: What the position of the encoder should change to.
        """
        self._position = new_position
        self._last_position = new_position
        self._time = utime.ticks_us()
        self._last_time = self._time
        
    def zero(self):
        """Sets the position of the encoder to zero.

        This is usually used right before beginning a process with the encoder.
        This will also reset the last positions and times used to calculate
        velocity, to avoid reporting incorrect velocities.
        """
        self._position = 0
        self._last_position = 0
        self._time = utime.ticks_us()
        self._last_time = self._time
        
    def get_velocity(self):
        """Updates the encoder and returns its velocity, in counts per second.
        
        If the encoder has moved since the last time update() was called, then
        the velocity estimate differ from expcted as this returns the average
        velocity over the span of time between update() calls.
        
        Returns:
            The encoder velocity, in counts per second.
        """
        self.update()
        return self._velocity
    
    def counts_to_rad(self, counts):
        return counts * 2 * math.pi / (CPR * 4)
    
    def get_position_rad(self):
        return self.counts_to_rad(self.get_position())
    
    def get_velocity_rad(self):
        return self.counts_to_rad(self.get_velocity())