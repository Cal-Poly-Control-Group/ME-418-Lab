def trapz_profile_length(omega_ss, t_acc, t_ss, t_stop, delta_t):
    t_total = 2 * t_acc + t_ss + t_stop
    return int(t_total // delta_t) + 2

def trapz_profile_gen(omega_ss, t_acc, t_ss, t_stop, delta_t):
    # t_acc, t_ss and t_stop must be a multiple of delta_t.
    for i in range(trapz_profile_length(
        omega_ss, t_acc, t_ss, t_stop, delta_t)):
        # WRITE YOUR CODE HERE to calculate t and omega, and generate the
        # required profile
        
        yield t, omega

if __name__ == '__main__':
    import numpy as np
    from matplotlib import pyplot as plt
    
    profile = np.array(list(trapz_profile_gen(5, 1, 1, 1, 0.2)))
    ts = profile[:,0]
    omegas = profile[:,1]
    
    plt.plot(ts, omegas, '.')
    plt.show()
