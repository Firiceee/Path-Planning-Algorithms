import numpy as np

class Particles:
    positions = []
    velocities = []
    colided : np.array

    def __init__(self, n, s, c1, c2, w):
        self.n, self.s, self.c1, self.c2, self.w = n, s, c1, c2, w
        self.positions.append(np.zeros((n, 2)))
        self.velocities.append(np.zeros((n,2)))
        self.colided = np.zeros(n).astype(bool)
        