# Defines a new class named PIController
class PIController:
    ''' A class for a proportional-integral controller.
        
        Attributes:
            kp:       Proportional gain
            ki:       Integral gain.
            out_max:  Maximum magnitude of output, for positive and negative.
                      If this is exceeded, saturation will be applied.
            delta_t:  The period which the controller is run at.
            sp:       Controller setpoint.
            
    '''
    # Defines the class's constructor, which is run
    # when object of this class is created
    def __init__(self, kp, ki, out_max, delta_t, sp):
        # 'self' is a placeholder for an object of this class.
        # therefore, self.kp is a variable belonging to objects of the
        # PIController class
        # Set the PI gains. The other variables should be set the same way,
        # using the self keyword to make them part of the controller object.
        self.kp = kp
        self.ki = ki
        
        # Set the maximum value that can be output from the controller.
        self.out_max = out_max
        
        # Set the initial setpoint.
        self.sp = sp
        
        # Set the controller period delta_t
        self.delta_t = delta_t
        
        # Integral of error needed for computing the I term
        self._integral = 0
        
        # Variables used to represent controller actions
        self._i_action = 0
        self._p_action = 0
        
    
    def set_gains(self, kp, ki):
        ''' Sets the proportional and integral controller gains.

            Args:
                kp: proportional gain (%/(rad/s))
                ki: integral ((rad/s)*s)
        '''
        self.kp = kp
        self.ki = ki
    
    # WRITE YOUR CODE HERE to define set_setpoint. Follow the same pattern as
    # set_gains uses.
    def set_setpoint(self, sp):
        self.sp = sp

    
    # WRITE YOUR CODE HERE to define the method run which will
    # take in the velocity of the motor and return the percent
    # voltage to set the motor to.
    def run(self, x):
        ''' Runs the PI controller once.

        The time interval used for the integral calculation is set as delta_t.
        Make sure to call this method at that period for the proper results.
        
        Args:
            x: The current value of the variable of the system which is being
            controlled. Usually represented by the symbol c.
            
        Returns:
            The control command which will attempt to drive the system to the
            setpoint. Usually represented by the symbol u.
        '''
        # Compute the error as the setpoint minus the current value x
        error = self.sp - x
        
        # Add error * delta_t to the integral error variable self._integral
        self._integral += error * self.delta_t
        
        # Calculate the integral and proportional actions (mind the sign).
        self._i_action = self.ki * self._integral
        self._p_action = self.kp * error
        
        # Calculate the controller output (total action)
        output = self._i_action + self._p_action
        
        # Apply saturation to the controller output (out_max)
        if output > self.out_max:
            output = self.out_max
        if output <= -self.out_max:
            output = -self.out_max
        
        # Return the total controller action
        return output
    
    def get_PI_components(self):
        ''' Gets the current proportional and integral actions.

        Keep in mind that these values do not saturate, but the total
        controller output does.

        Returns:
            A tuple (p_action, i_action), where p_action is the component of
            the output from the proportional term, and i_action is the
            component of the output from the integral term.
            
        '''
        return self._p_action, self._i_action


# Controller test. Run this file using the green run button to test that the
# PI controller calculations work properly.
if __name__ == '__main__':
    con = PIController(0,0,100,1,5)
    con.set_setpoint(5)
    con.set_gains(1, 1)
    print("Expected result:\n(5, 5)\n(5, 10)\n(5, 15)\n(5, 20)\n(5, 25)")
    print("Actual result:")
    for i in range(5):
        con.run(0)
        print(con.get_PI_components())
    
    print("\nExpected result:\n(0, 25)\n(0, 25)\n(0, 25)\n(0, 25)\n(0, 25)")
    print("Actual result:")
    for i in range(5):
        con.run(5)
        print(con.get_PI_components())
    
    con.set_gains(100,0)
    print("\nExpected result:\n100")
    print("Actual result:")
    print(con.run(0))
    
    print("\nExpected result:\n-100")
    print("Actual result:")
    print(con.run(10))