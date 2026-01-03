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

    def simulate_and_show(self, colided_num : int, uncolided_num : int):
        """
        Does the PSO simulation.

        :param colided_num: Will display at most this amount of colided particles trace.
        :param uncolided_num: Same, but for uncolided particles.
        """
        for i in range(self.num_iterations - 1):
            particles.iterate()

        fig, ax = self.environment.show(self.epsilon, show=False)
        top_right_dist = np.sqrt(np.square(particles.positions[:, :, 0] - self.environment.topright[0]) + np.square(particles.positions[:, :, 1] - self.environment.topright[1]))
        
        colided_count = 0
        uncolided_count = 0
        for i in range(self.particles.n):
            index = int(particles.colided_at[i][0])
            index = index if particles.colided[i] else self.num_iterations - 1 

            notreached_end = np.min(top_right_dist[:index, i]) > self.epsilon
            if (notreached_end and colided_count == colided_num) or (not notreached_end and uncolided_count == uncolided_num):
                continue

            if notreached_end:
                colided_count+=1
            else:
                uncolided_count += 1
                
            first_part = particles.positions[:index+ (1 if notreached_end else 0), i]
            color = "red" if notreached_end else "green"
            #color = "red" if particles.colided[i] == 1 else "green"
            ax.plot(first_part[:, 0], first_part[:, 1], '-o', color=color,linewidth=0.6, markersize=2)
        plt.show()
    

print("hey")
num_it = 100
env = Environment(scenario=3)
#print(env._is_point_in_rectangles([177, 77]))
particles = Particles(100, c1=1.8, c2=1.8, w=0.8,nb_iteration= num_it,environment= env)
sim = PsoSim(env, particles, num_it)
sim.simulate_and_show(5, 5)


# (177, 77) in but says not in
# (85, 106) not in but says it is in