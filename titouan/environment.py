import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.pyplot import figure

class Environment:
    rectangles : list[list[float]]
    topright : tuple[float]
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
            self.topright = (lines[0], lines[1])
            self.us = (lines[2], lines[3])
            self.ud = (lines[4], lines[5])
            self.ustwo = (lines[6], lines[7])
            self.udtwo = (lines[8], lines[9])
            self.R = lines[10]
            
            while True:
                rectangle = f.readline()
                if rectangle == "": # EOF
                    return
                self.rectangles.append([float(i.strip()) for i in rectangle.split(" ") if i != ""])
    
    def show(self):
        """
        Draw a matplotlib plot representing the environment.
        """
        fig, ax = plt.subplots()
        for i in self.rectangles:
            ax.add_patch(Rectangle((i[0], i[1]), i[2], i[3]))
        plt.xlim(0, self.topright[0])
        plt.ylim(0, self.topright[1])
        plt.show()

    @staticmethod
    def show_many(envs, titles : list[str], num_col = 3):
        """
        Display mutliple environments on the same matplot lib plot.
        """
        n = len(envs)
        num_rows = math.ceil(n / num_col)
        fig, ax = plt.subplots(num_rows, num_col,figsize=(10, 7), dpi = 75)
        fig.tight_layout()
        
        for x in range(num_rows):
            for y in range(num_col):
                print(x, y)
                i = num_col * x + y
                if i >= n:
                    break
                
                for rect in envs[i].rectangles:
                    print("adding rect")
                    ax[x, y].add_patch(Rectangle((rect[0], rect[1]), rect[2], rect[3], color= "black"))
                    ax[x, y].set_title(titles[i])    
                    
                    ax[x, y].set_xlim(0, envs[i].topright[0])
                    ax[x, y].set_ylim(0, envs[i].topright[1])   
        
        plt.show()


env = Environment(scenario=4)
Environment.show_many(envs = [Environment(scenario=i) for i in range(5)], titles = [f"Scenario {i}" for i in range(5)])