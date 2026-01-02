import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.pyplot import figure
import numpy as np

class Environment:
    rectangles : np.array # shape : (m, 4) where m is the number of rectangles.
    topright : np.array
    us : tuple[float]
    ud : tuple[float]
    ustwo : tuple[float]
    udtwo : tuple[float]
    R : float

    def __init__(self, path : str = None, scenario : int = None):
        """
        Load an environment from a file.
        
        :param path: Relative path to the file.
        :param scenario: Number associated with a scenario in /scenarios. If `scenario` is suplied, `path` is ignored.
        """
        self.rectangles = []
        if scenario != None:
            path = f'../scenarios/scenario{scenario}.txt'
        with open(path, 'r') as f:
            head = [f.readline() for i in range(11)]
            lines = [float(i.strip().upper()) for i in head]
            print("lines")
            print(lines)
            self.topright = np.array([lines[0], lines[1]])
            self.us = (lines[2], lines[3])
            self.ud = (lines[4], lines[5])
            self.ustwo = (lines[6], lines[7])
            self.udtwo = (lines[8], lines[9])
            self.R = lines[10]
            
            rectangles = []
            while True:
                rectangle = f.readline()
                if rectangle == "": # EOF            
                    self.rectangles = np.array(rectangles)
                    return
                rectangles.append([float(i.strip()) for i in rectangle.split(" ") if i != ""])
    def show(self, epsilon = None, show=True):
        """
        Draw a matplotlib plot representing the environment.

        :param epsilon: If supplied, draws a circle centered on `topright` of radius `epsilon`.
        """
        fig, ax = plt.subplots()
        for i in self.rectangles:
            ax.add_patch(Rectangle((i[0], i[1]), i[2], i[3]))
        if epsilon:
            circle = plt.Circle(self.topright, epsilon, fill = False, color = "red")
            ax.add_artist(circle)
        plt.xlim(0, self.topright[0])
        plt.ylim(0, self.topright[1])
        if show:
            plt.show()
        return fig,ax

    @staticmethod
    def show_many(envs, titles : list[str], num_col = 3, show=True):
        """
        Display mutliple environments on the same matplot lib plot.

        :param envs: List of environment to draw.
        :param titles: Titles for each environment. Length must be greater than the length of env.
        :param num_col: When displaying multiple environment, they are grid arranged. This parameter
        determines the width of the grid.

        :returns: (fig, ax) tuple
        """
        n = len(envs)
        num_rows = math.ceil(n / num_col)
        fig, ax = plt.subplots(num_rows, num_col,figsize=(10, 7), dpi = 75)
        fig.tight_layout()
        
        for x in range(num_rows):
            for y in range(num_col):
                i = num_col * x + y
                if i >= n:
                    break
                
                for rect in envs[i].rectangles:
                    print("adding rect")
                    ax[x, y].add_patch(Rectangle((rect[0], rect[1]), rect[2], rect[3], color= "black"))
                    ax[x, y].set_title(titles[i])    
                    
                    ax[x, y].set_xlim(0, envs[i].topright[0])
                    ax[x, y].set_ylim(0, envs[i].topright[1])   
        if show:
            plt.show()
        return fig, ax
    
    def _is_point_in_rectangles(self, point):
        """
        Returns True if the given point is inside a rectangle in the environment.
        """
        for rect in self.rectangles:
            if rect[0] <= point[0] <= rect[0] + rect[2] and rect[1] <= point[1] <= rect[1] + rect[3]:
                return True
        return False
    
    def _is_point_in_map(self, point):
        return ( self.topright[0] >= point[0] >= 0 and self.topright[1] >= point[1] >= 0)
    
    
    def vertex_is_colliding(self, point1, point2):
        """
        Returns True if the vertex (point1, point2) passes inside a rectangle in the environment.

        :param point1: np.array shape : (2, )
        :param point1: np.array shape : (2, )
        """
        if self._is_point_in_rectangles(point1) or self._is_point_in_rectangles(point2):
            print("in rectangle")
            return True
        
        if not (self._is_point_in_map(point1) and self._is_point_in_map(point2)):
            return True
        
        for rect in self.rectangles:
            a = [rect[0], rect[0], rect[0] + rect[2], rect[0] + rect[2]]
            b = [rect[1], rect[1], rect[1] + rect[3], rect[1] + rect[3]]
            lx = [rect[2], 0, -rect[2], 0]
            ly = [0, rect[3], 0, -rect[3]]
            for i in range(4):
                cuts_through_side = False
                if lx[i] == 0: # Vertical side
                    if point1[0] == point2[0]: # x1 = x2, vertical line.
                        cuts_through_side = point1[0] == a[i] # correct x coordinate
                        if (point1[1] <= b[i] and point2[1] <= b[i]) or (point1[1] >= b[i] + ly[i] and point2[1] >= b[i] + ly[i]):
                            cuts_through_side = False
                    else:
                        # Computes the intersections point
                        t = (a[i] - point1[0]) / (point2[0] - point1[0])
                        alpha = ((1-t) * point1[1] + t * point2[1] - b[i]) / ly[i]
                        if 0 <= t <= 1 and 0 <= alpha <= 1:
                            print("lx")
                            print(i)
                            print(t, alpha)
                            print(rect)
                            print(f"{a[i], b[i], lx[i], ly[i]=}")
                            cuts_through_side = True
                else:
                    # ly[i] == 0, horizontal side
                    if point1[1] == point2[1]: # y1 = y2, horizontal line.
                        cuts_through_side = point1[1] == b[i] # correct y coordinate
                        if (point1[0] <= a[i] and point2[0] <= a[i]) or (point1[0] >= a[i] + lx[i] and point2[0] >= a[i] + lx[i]):
                            cuts_through_side = False
                    else:                        
                        # Computes the intersections point
                        t = (b[i] - point1[1]) / (point2[1] - point1[1])
                        alpha = ((1-t) * point1[0] + t * point2[0] - a[i]) / lx[i]
                        if 0 <= t <= 1 and 0 <= alpha <= 1:
                            cuts_through_side = True
                
                if cuts_through_side:
                    print(point1, point2)
                    print("cutting through side")
                    return True
                
        print("no colision")
        return False

        
def run_tests():
    env = Environment(path="/Users/titouan/Desktop/Code/Python/Path-Planning-Algorithms/scenarios/scenario_test.txt")
    tests = [
        {
            "desc": "Basic: No Collision (Far away)",
            "path": [[(0.0, 0.0), (1.0, 1.0)]],
            "expect": False
        },
        {
            "desc": "Basic: Simple Intersection",
            "path": [[(1.0, 4.0), (7.0, 4.0)]],
            "expect": True
        },
        {
            "desc": "Horizontal Aligned (Ghost Floor)",
            # Line is at y=4 (middle of box) but to the right (x=8 to 10)
            "path": [[(8.0, 4.0), (10.0, 4.0)]],
            "expect": False
        },
        {
            "desc": " Vertical Aligned (Laser Pointer)",
            # Line is at x=4 (middle of box) but above (y=8 to 10)
            "path": [[(4.0, 8.0), (4.0, 10.0)]],
            "expect": False
        },
        {
            "desc": "Sloped Pointing At Wall",
            # Points at (2,2) but stops at (1,1)
            "path": [[(0.0, 0.0), (1.0, 1.0)]],
            "expect": False
        },
        {
            "desc": "Edge Case: Exact Corner Touch",
            "path": [[(0.0, 0.0), (2.0, 2.0)]],
            "expect": True
        },
        {
            "desc": "Complex: Long diagonal crossing entire box",
            "path": [[(0.0, 0.0), (10.0, 10.0)]],
            "expect": True
        }
    ]

    print(f"{'TEST CASE':<50} | {'RESULT':<6}")
    print("-" * 60)
    
    all_passed = True
    for t in tests:
        result = env.vertex_is_colliding(t['path'][0][0], t['path'][0][1])
        status = "PASS" if result == t['expect'] else "FAIL"
        if status == "FAIL": all_passed = False
        print(f"{t['desc']:<50} | {status} (Got {result})")
    
    print("-" * 60)
    if all_passed:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")


if __name__ == "main":
    run_tests()


#env = Environment(scenario=4)
#Environment.show_many(envs = [Environment(scenario=i) for i in range(5)], titles = [f"Scenario {i}" for i in range(5)])