### 3)

For the particles we will define the class `particles` storing and updating the particle positions during their lifetime. The class will contain the following fields :
 - positions : `list(np.array(n, 2))` : The ($x$,$y$) positions of every particle up until step $k$.
 - velocities : `list(np.array(n, 2))` : The ($v_x$,$v_y$) velocity of every particle up until step $k$.
 - colided : `np.array(n)` : A list of boolean indicating whether the path at index $i$ has collided during any of the past $k$ steps.
 - hyperparameters : $s$,$c_1$,$c_2$,$w$

We will use the fitness function : quadratic distance to the arrival point.