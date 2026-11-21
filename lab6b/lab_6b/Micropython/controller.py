from filters import FirstOrderLowPass
from utils import FeedforwardPulse


# Starting cutoff from the Lab 6A filtered PD example, in hertz.
FILTER_CUTOFF_HZ = 20


class PIDController:
    """A proportional-integral-derivative controller."""

    def __init__(self, kp, ki, kd, out_max, delta_t, setpoint_rad):
        # Use these variables for the controller actions so that
        # get_PID_actions() works properly.
        self._p_action = 0.0
        self._i_action = 0.0
        self._d_action = 0.0

        self.delta_t = delta_t
        self.setpoint_rad = setpoint_rad
        self._integral = 0.0
        self._last_error = None
        self._derivative_filter = FirstOrderLowPass(FILTER_CUTOFF_HZ, delta_t)

        # Store the three gains and output limit as instance
        # attributes.
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.out_max = out_max

    def _update_derivative(self, error):
        """Update the filtered error rate from one position sample."""
        error_rate = 0.0
        if self._last_error is not None:
            error_rate = (error - self._last_error) / self.delta_t
        self._last_error = error
        return self._derivative_filter.filter(error_rate)

    def run(self, position_rad):
        """Calculate the voltage percentage from the measured position in radians."""

        # Calculate the position error as the setpoint minus the
        # measured position. Add its rectangular area to the accumulated error.
        error = self.setpoint_rad - position_rad
        self._integral += error * self.delta_t

        filtered_error_rate = self._update_derivative(error)

        # Calculate and store the P, I, and D actions.
        self._p_action = self.kp * error
        self._i_action = self.ki * self._integral
        self._d_action = self.kd * filtered_error_rate
        

        # Add the three actions to obtain the controller output.
        output = self._p_action + self._i_action + self._d_action

        # Limit the output to the range [-out_max, out_max].
        if output < -self.out_max:
            output = -self.out_max
        elif output > self.out_max:
            output = self.out_max

        # Return the limited output.
        return output


    def get_PID_actions(self):
        """Return the current P, I, and D actions before output saturation."""

        return self._p_action, self._i_action, self._d_action

# Defines a new class named SwitchedController
class SwitchedController:
    ''' A class for a switched controller (pulse then PID for Lab 6b).
        
        Attributes:
            pulse_width:       Pulse width.
            kp:                Proportional gain
            ki:                Integral gain.
            kd:                Derivative gain.
            delta_t:           The period which the controller is run at.
            setpoint_rad:      Controller setpoint.
            mode:              Mode of two-stage switched controller (0 or 1)
            
    '''
    def __init__(self, pulse_width, kp, ki, kd, out_max, delta_t, setpoint_rad):
        self.controller_0 = FeedforwardPulse(pulse_width, delta_t)
        self.controller_1 = PIDController(kp, ki, kd, out_max, delta_t, setpoint_rad)
        self.mode = 0         # mode 0 or 1
            
    def run(self, x=0):
        ''' Runs the switched controller once.
        
        Args:
            x: The current value of the variable of the system which is being
            controlled.
            
        Returns:
            The control command which will attempt to drive the system to the
            setpoint. Usually represented by the symbol u.  
        '''
        
        if self.mode == 0:
            # Keep the derivative current while the pulse drives the motor.
            self.controller_1._update_derivative(self.controller_1.setpoint_rad - x)
            u = self.controller_0.run(x)
        else:
            u = self.controller_1.run(x)
        
        return u
    
    def set_mode(self, mode):
        self.mode = mode
    
    def set_setpoint(self, setpoint_rad):
        self.setpoint_rad = setpoint_rad