def solve_lpp(constraints, objective, maximize=True):
    """
    constraints: list of tuples [(a1, b1, c1), (a2, b2, c2), ...]
    objective: tuple (p, q) → Z = p*x + q*y
    maximize: True for maximization, False for minimization
    """

    points = []

    # Step 1: Add origin (0,0) if feasible
    valid_origin = True
    for a, b, c in constraints:
        if a*0 + b*0 > c:
            valid_origin = False
            break
    if valid_origin:
        points.append((0, 0))

    # Step 2: Intersections with axes
    for a, b, c in constraints:
        # x-intercept (y = 0)
        if a != 0:
            x = c / a
            y = 0
            if x >= 0:
                valid = True
                for a1, b1, c1 in constraints:
                    if a1*x + b1*y > c1:
                        valid = False
                        break
                if valid:
                    points.append((x, y))

        # y-intercept (x = 0)
        if b != 0:
            x = 0
            y = c / b
            if y >= 0:
                valid = True
                for a1, b1, c1 in constraints:
                    if a1*x + b1*y > c1:
                        valid = False
                        break
                if valid:
                    points.append((x, y))

    # Step 3: Intersections between lines
    n = len(constraints)
    for i in range(n):
        a1, b1, c1 = constraints[i]
        for j in range(i + 1, n):
            a2, b2, c2 = constraints[j]

            det = a1*b2 - a2*b1
            if det != 0:
                x = (c1*b2 - c2*b1) / det
                y = (a1*c2 - a2*c1) / det

                if x >= 0 and y >= 0:
                    valid = True
                    for a, b, c in constraints:
                        if a*x + b*y > c:
                            valid = False
                            break
                    if valid:
                        points.append((x, y))

    # Step 4: Evaluate objective function
    best_point = None
    best_val = None

    if not points:
        return None, None

    for x, y in points:
        val = objective[0]*x + objective[1]*y

        if best_val is None:
            best_val = val
            best_point = (x, y)
        else:
            if maximize and val > best_val:
                best_val = val
                best_point = (x, y)
            elif not maximize and val < best_val:
                best_val = val
                best_point = (x, y)

    return best_point, best_val