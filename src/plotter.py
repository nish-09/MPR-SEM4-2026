import matplotlib.pyplot as plt
import numpy as np

def plot_graph(constraints, solution_point):
    x_vals = np.linspace(0, 20, 400)
    
    plt.figure(figsize=(6,6))
    
    # Plot all constraint lines
    for a, b, c in constraints:
        if b != 0:
            y_vals = (c - a*x_vals)/b
            plt.plot(x_vals, y_vals, label=f'{a}x + {b}y <= {c}')
        else:
            x_line = c / a
            plt.axvline(x=x_line, label=f'{a}x <= {c}')
    
    # Highlight solution point
    if solution_point:
        plt.plot(solution_point[0], solution_point[1], 'ro', label='Optimal Solution')
    
    plt.xlim(0, max(20, solution_point[0]+5))
    plt.ylim(0, max(20, solution_point[1]+5))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Graphical Method Feasible Region')
    plt.grid(True)
    plt.legend()
    plt.show()
