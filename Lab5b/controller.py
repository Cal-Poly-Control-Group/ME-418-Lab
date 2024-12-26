# Defines a new class named PIDController
class PIDController:
    ''' A class for a proportional-integral-derivative (PID) controller.
        
        Attributes:
            kp:       Proportional gain
            ki:       Integral gain.
            kd:       Derivative gain.
            out_max:  Maximum magnitude of output, for positive and negative.
                      If this is exceeded, saturation will be applied.
            delta_t:  The period which the controller is run at.
            sp:       Controller setpoint.
            
    '''
    def __init__(self, kp, ki, kd, out_max, delta_t, sp):       
        # Use these variables for the controller actions, so that
        # get_PID_actions works properly.
        self._i_action = 0
        self._p_action = 0
        self._d_action = 0
        
        # This is important for good calculation of the derivative. The error
        # should be the setpoint for the first run, since the pendulum starts
        # from zero.
        self.last_error = sp
        
        # WRITE YOUR CODE HERE to complete the constructor (initialize gains,
        # delta_t, out_max using self., and make a variable to store integral)
        self.delta_t = delta_t
        self._integral = 0
        
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.out_max = out_max
    
    # WRITE YOUR CODE HERE to define the method run which will
    # take in the velocity of the motor and return the percent
    # voltage to set the motor to.
    def run(self, x):
        ''' Runs the PID controller once.

        The time interval used for the integral calculation is set as delta_t.
        Make sure to call this method at that period for the proper results.
        
        Args:
            x: The current value of the variable of the system which is being
            controlled. Usually represented by the symbol c.
            
        Returns:
            The control command which will attempt to drive the system to the
            setpoint. Usually represented by the symbol u.    
        '''
        # Delete 'pass' placeholder after writing this function.
        pass
    
    def get_PID_actions(self):
        ''' Gets the current PID actions of the controller.

        Keep in mind that these values do not saturate, but the total controller
        output does.
        
        Returns:
            A tuple (p_action, i_action, d_action), where each action is the
            component of the output which is caused by the P, I, or D term.
        '''
        return self._p_action, self._i_action, self._d_action
    
    def set_setpoint(self, sp):
        self.sp = sp


# Controller test. Run this file using the green run button to test that the
# PI controller calculations work properly.
if __name__ == '__main__':
    from matplotlib import pyplot as plt
    import numpy as np
    con = PIDController(1, 1, 1, 100, 0.005, 0)
    
    p_actions = []
    i_actions = []
    d_actions = []
    ts =  np.arange(0, 1, 0.005)
    noise = 2*np.pi/4000 * np.sin(150 * ts)
    sps = np.linspace(0, 1, len(ts))
    
    for i, t in enumerate(ts):
        con.set_setpoint(sps[i] + noise[i])
        con.run(0)
        p, i, d = con.get_PID_actions()
        p_actions.append(p)
        i_actions.append(i)
        d_actions.append(d)
    
    plt.subplot(311)
    plt.plot(ts, p_actions)
    plt.ylabel("P action")
    plt.subplot(312)
    plt.plot(ts, i_actions)
    plt.ylabel("I action")
    plt.subplot(313)
    plt.plot(ts, d_actions)
    plt.ylabel("D action")
    plt.xlabel("Time")
    plt.show()
