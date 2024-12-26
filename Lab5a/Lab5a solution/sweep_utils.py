import math       
def sweep_gen(amplitude, f_1, f_2, interval, n_steps):
    ''' Generate a sine sweep. Each run through the loop yields a value to
    be sent to the input of the system. The frequency increases linearly.
    See: https://en.wikipedia.org/wiki/Chirp
    
    Args:
        amplitude: The amplitude of all the waves in the generated sweep.
        f_1:   The lowest frequency to use in the sweep.
        f_2:     The highest frequency to use in the sweep.
        interval:  The amount of time that the sweep should take.
        n_steps:   The total amount of data points to generate for the sweep.
        
        
    Returns:
        Tuples of of time and the value of the sweep function.
        This is a generator, so the tuples are yielded one at a time.
        
        
    Typical Usage Example:
        from sweep_utils import sweep_gen
        for t, val in sweep_gen(100, 1, 10, 1, 100):
            # Print time and value as csv for later plotting
            print(t, val, sep=',')
    '''
    for i in range(n_steps):
        # WRITE YOUR CODE HERE to find the time for this step.
        t = interval * i / n_steps
        # WRITE YOUR CODE HERE to calculate the phase of the sweep.
        # (the input to the sine function).
        phi = 2 * math.pi * (f_1 * t + (f_2 - f_1) * t ** 2 / 2 / interval)
        # WRITE YOUR CODE HERE to calculate the value of the sweep input.
        # Store the result in the sweep variable.
        sweep = amplitude * math.sin(phi)
        # Yield the tuple of time and the sweep value.
        yield (t, sweep)

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    times = []
    vals = []
    for t, val in sweep_gen(100, 1, 10, 1, 300):
        times.append(t)
        vals.append(val)
    plt.plot(times, vals)
    plt.show()
    