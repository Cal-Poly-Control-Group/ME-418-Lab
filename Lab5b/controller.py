"""PID controller class for Lab 5B."""


class PIDController:
    """A proportional-integral-derivative controller."""

    def __init__(self, kp, ki, kd, out_max, delta_t):
        # Use these variables for the controller actions so that
        # get_PID_actions() works properly.
        self._p_action = 0.0
        self._i_action = 0.0
        self._d_action = 0.0

        # The fixed period and accumulated error are set up for you.
        self.delta_t = delta_t
        self._integral = 0.0

        # TODO 1: Store the three gains and output limit as instance
        # attributes.

    def run(self, error, error_rate):
        """Run the PID calculation once and return voltage percentage.

        Args:
            error: Current position error in radians.
            error_rate: Current rate of position error in radians per second.
        """

        # TODO 2: Add the current rectangular area to the accumulated error.


        # TODO 3: Calculate and store the P, I, and D actions.


        # TODO 4: Add the three actions to obtain the controller output.


        # TODO 5: Limit the output to the range [-out_max, out_max].


        # TODO 6: Return the limited output.


    def get_PID_actions(self):
        """Return the current P, I, and D actions before output saturation."""

        return self._p_action, self._i_action, self._d_action


# Run this file with the Local Python 3 interpreter to test the controller.
# PROVIDED TEST CODE — DO NOT MODIFY BELOW THIS LINE.
if __name__ == "__main__":
    import numpy as np
    from matplotlib import pyplot as plt

    delta_t = 0.005
    con = PIDController(1, 1, 1, 100, delta_t)

    p_actions = []
    i_actions = []
    d_actions = []
    times_s = np.arange(0, 1, delta_t)
    errors = np.linspace(0, 1, len(times_s))
    errors += 2 * np.pi / 4000 * np.sin(150 * times_s)

    last_error = errors[0]

    for error in errors:
        error_rate = (error - last_error) / delta_t
        last_error = error
        con.run(error, error_rate)
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
