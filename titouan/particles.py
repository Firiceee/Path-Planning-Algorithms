import numpy as np

from environment import Environment

class Particles:
    positions  : np.array # (num_iteration, n, 2)
    velocities : np.array
    colided : np.array
    iteration_count = 0
    environment : Environment
    global_best : np.array # shape : (1, 2)
    local_best : np.array # shape : (n, 2)

    def __init__(self, n, c1, c2, w, nb_iteration, environment):
        self.n, self.c1, self.c2, self.w = n, c1, c2, w
        self.positions = np.zeros((nb_iteration, n, 2))

        self.local_best = np.zeros((n, 2))
        self.global_best = np.zeros((1, 2))

        self.velocities = np.random.uniform(0, 1, (nb_iteration, n, 2))
        self.colided = np.zeros((n, 1)).astype(bool)
        self.environment = environment


    def iterate(self):
        r1 = np.random.uniform(0, 1, (self.n ,1))
        r2 = np.random.uniform(0, 1, (self.n ,1))

        # Update position of every particle
        self.velocities[self.iteration_count+1] = (self.w * self.velocities[self.iteration_count]
            + self.c1 * r1 * (self.local_best - self.positions[self.iteration_count])
            + self.c2 * r2 * (self.global_best - self.positions[self.iteration_count])
            )
        self.positions[self.iteration_count + 1] += self.velocities[self.iteration_count + 1]

        # Check which particles have colided
        for i in range(self.n):
            if not self.colided[i] and self.environment.vertex_is_colliding(self.positions[self.iteration_count][i], self.positions[self.iteration_count+1][i]):
                # An uncolided particle has colided on the last iteration.
                self.colided[i][0] = True

        # Reset to last known position the particles who have colided.
        self.velocities[self.iteration_count+1] = self.colided * self.velocities[self.iteration_count] + (1 - self.colided) * self.velocities[self.iteration_count + 1]
        self.positions[self.iteration_count+1] = self.colided * self.positions[self.iteration_count] + (1 - self.colided) * self.positions[self.iteration_count + 1]

        # Compute the new local best and new global best
        last_pos_distances = np.sum(np.square(self.positions[self.iteration_count+1]  - self.environment.topright), axis=1)
        if np.min(last_pos_distances) < np.sum(np.square(self.global_best - self.environment.topright)):
            self.global_best = self.positions[self.iteration_count + 1][np.argmin(last_pos_distances)]
        for i in range(self.n):
            if last_pos_distances[i] < np.sum(np.square(self.local_best[i] - self.environment.topright)):
                self.local_best[i] = self.positions[self.iteration_count + 1][i]
        
        self.iteration_count += 1


if __name__ == "main":
    env = Environment(scenario=0)
    print(env.topright)
    num_it = 10
    particles = Particles(100, 1, 2, 3, 0.4, num_it, env)
    print(f"{particles.positions=}")
    print(f"{particles.global_best=}")
    print(f"{particles.local_best=}")
    for i in range(num_it-1):
        particles.iterate()
    print(f"{particles.positions}")
    print(f"{particles.colided}")
    print(f"{particles.global_best=}")
    print(f"{particles.local_best=}")
        
    