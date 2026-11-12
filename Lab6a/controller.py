"""PID controller class for Lab 6A."""


class PIDController:
    """A proportional-integral-derivative controller."""

    def __init__(self, kp, ki, kd, out_max, delta_t, setpoint_rad):
        # Use these variables for the controller actions so that
        # get_PID_actions() works properly.
        self._p_action = 0.0
        self._i_action = 0.0
        self._d_action = 0.0

        # The encoder starts at zero, so the initial error is the setpoint.
        self.delta_t = delta_t
        self.setpoint_rad = setpoint_rad
        self._integral = 0.0
        self._last_error = setpoint_rad

        # TODO 1: Store the three gains and output limit as instance
        # attributes.

        # FILTERED PD MODIFICATION (Section 6A.3.4, PD Control with
        # First-Order Low-Pass Filtering): Skip this during the P and unfiltered
        # PD tests. After saving your unfiltered PD response in Section 6A.3.3,
        # import FirstOrderLowPass from filters at the top of this file and
        # create one filter per controller here using the cutoff and delta_t.

    def run(self, position_rad):
        """Calculate the voltage percentage from the measured position in radians."""

        # TODO 2: Calculate the position error as the setpoint minus the
        # measured position. Add its rectangular area to the accumulated error.


        # TODO 3: Calculate error_rate using the current error, _last_error,
        # and delta_t. Save the current error in _last_error for the next call.

        # FILTERED PD MODIFICATION (Section 6A.3.4): After adding the filter
        # in the constructor, pass error_rate to its filter() method once per
        # update. Use the returned rate for D and keep using error for P and I.

        # TODO 4: Calculate and store the P, I, and D actions.


        # TODO 5: Add the three actions to obtain the controller output.


        # TODO 6: Limit the output to the range [-out_max, out_max].


        # TODO 7: Return the limited output.


    def get_PID_actions(self):
        """Return the current P, I, and D actions before output saturation."""

        return self._p_action, self._i_action, self._d_action


# Run this file with the Local Python 3 interpreter to test the controller.
# PROVIDED TEST CODE — DO NOT MODIFY BELOW THIS LINE.
if __name__ == "__main__":
    import numpy as np
    from matplotlib import pyplot as plt

    delta_t = 0.005
    con = PIDController(1, 1, 1, 100, delta_t, setpoint_rad=0.0)

    p_actions = []
    i_actions = []
    d_actions = []
    times_s = np.arange(0, 1, delta_t)
    positions_rad = np.linspace(0, -1, len(times_s))
    positions_rad -= 2 * np.pi / 4000 * np.sin(150 * times_s)

    for position_rad in positions_rad:
        con.run(position_rad)
        p_action, i_action, d_action = con.get_PID_actions()
        p_actions.append(p_action)
        i_actions.append(i_action)
        d_actions.append(d_action)

    fig, axes = plt.subplots(3, 1, sharex=True)
    axes[0].plot(times_s, p_actions)
    axes[0].set_ylabel("P action")
    axes[1].plot(times_s, i_actions)
    axes[1].set_ylabel("I action")
    axes[2].plot(times_s, d_actions)
    axes[2].set_ylabel("D action")
    axes[2].set_xlabel("Time [s]")
    fig.tight_layout()
    plt.show()
