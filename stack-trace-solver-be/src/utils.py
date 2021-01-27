import numpy as np

def chunks(l, n):
    return [list(array) for array in np.array_split(l, n)]