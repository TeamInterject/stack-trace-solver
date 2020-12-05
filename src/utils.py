import numpy as np
from pathlib import Path

def chunks(l, n):
    return [list(array) for array in np.array_split(l, n)]

def extract_filename(path):
    return Path(path).stem