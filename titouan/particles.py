import numpy as np

class Particles:
    positions = np.array([])
    velocities = np.array([])
    colided : np.array

    def __init__(self, n, s, c1, c2, w):
        self.n, self.s, self.c1, self.c2, self.w = n, s, c1, c2, w
        self.positions = np.append(self.positions,np.zeros((n, 2)))
        self.velocities = np.append(self.velocities,np.zeros((n, 2)))
        self.colided = np.zeros(n).astype(bool)

particles = Particles(100, 1, 2, 3, 4)
print(particles.positions.shape)
print(particles.positions)
    
    