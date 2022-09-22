import numpy as np

def decay(half_life, n_0, max_half_lives):
    """Returns the quantity of nuclei according to the element half-life"""
    t = np.linspace(0, half_life * max_half_lives, num=500)
    n = n_0 * np.exp(-(np.log(2)/half_life*t))
    return t, n