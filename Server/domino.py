import numpy as np

class Domino:
    def __init__(self, values:list):
        self.values = np.array(values)
        
    def sum_vals(self):
        return int(self.values[0]) + int(self.values[1])
    