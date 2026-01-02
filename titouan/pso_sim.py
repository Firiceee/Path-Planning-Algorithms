import numpy as np
from environment import Environment
from particles import Particles
import matplotlib.pyplot as plt


class PsoSim():
    def __init__(self, environment : Environment, particles, num_iterations):
        self.environment = environment
        self.particles = particles
        self.num_iterations = num_iterations

        # Epsilon is the radius of the largest circle centered in env.topright that does not intersect with any obstacle.
        # Geometry shows that it is the distance with the nearest topright corner of the obstacles.
        rects = self.environment.rectangles
        top_right_dist = np.sqrt(np.square((rects[:,0] + rects[:,2] - environment.topright[0])) + np.square((rects[:,1] + rects[:,3] - environment.topright[1])))
        self.epsilon = np.min(top_right_dist)

    def simulate(self):
        for i in range(self.num_iterations - 1):
            particles.iterate()
        fig, ax = self.environment.show(self.epsilon, show=False)
        to_draw = [0, 1, 2, 3]
        for i in to_draw:
            first_part = particles.positions[:, i]
            ax.plot(first_part[:, 1], first_part[:, 0], '-o', color="red")
        plt.show()
    


num_it = 100
env = Environment(scenario=2)
particles = Particles(100, 2, 1, 0.8, num_it, env)
sim = PsoSim(env, particles, num_it)
sim.simulate()
