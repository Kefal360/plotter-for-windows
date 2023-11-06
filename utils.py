import numpy as np
import sys
#sys.path.insert(1, 'C:\\Users\\sam11\\Desktop\\proj\\PyQt-Plotter-Dialog\\parser')
from expr_parser import ValueType
#from types import ValueType

def size(x: ValueType) -> int:
    if isinstance(x, np.ndarray):
        return x.size
    else:
        return 1