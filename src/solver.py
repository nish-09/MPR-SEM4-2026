import numpy as np

def solve_lpp(constraints, objective, maximize=True):
    """
    constraints: list of tuples [(a1, b1, c1), (a2, b2, c2), ...] representing a1*x + b1*y <= c1
    objective: tuple (p, q) representing Z = p*x + q*y
    maximize: True if maximization problem
    """
    
    # Extract lines for intersection calculation
    lines = []
    for a, b, c in constraints:
        if b != 0:
            # y = (c - a*x)/b
            lines.append(lambda x, a=a, b=b, c=c: (c - a*x)/b)
        else:
            # Vertical line x = c/a
            lines.append(lambda x, a=a, c=c: None)  # Will handle separately

    # Find feasible region points (all intersections)
    points = []
    for i in range(len(constraints)):
        a1, b1, c1 = constraints[i]
        for j in range(i+1, len(constraints)):
            a2, b2, c2 = constraints[j]
            det = a1*b2 - a2*b1
            if det != 0:
                x = (c1*b2 - c2*b1)/det
                y = (a1*c2 - a2*c1)/det
                if x >= 0 and y >= 0:  # Non-negative
                    # Check all constraints
                    valid = True
                    for a, b, c in constraints:
                        if a*x + b*y > c + 1e-5:
                            valid = False
                            break
                    if valid:
                        points.append((x, y))

    # Evaluate objective function
    best_val = None
    best_point = None
    for x, y in points:
        val = objective[0]*x + objective[1]*y
        if best_val is None or (maximize and val > best_val) or (not maximize and val < best_val):
            best_val = val
            best_point = (x, y)
    
    return best_point, best_val