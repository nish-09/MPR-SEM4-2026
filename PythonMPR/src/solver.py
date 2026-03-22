def solve_lpp(constraints, objective, maximize=True):
    """
    constraints: list of tuples [(a1, b1, c1, type1), (a2, b2, c2, type2), ...]
    where type is 1 for <= and -1 for >=
    objective: tuple (p, q) → Z = p*x + q*y
    maximize: True for maximization, False for minimization
    """

    points = []

    # Step 1: Add origin (0,0) if feasible
    valid_origin = True
    for a, b, c, typ in constraints:
        lhs = a*0 + b*0
        if typ == 1 and lhs > c:
            valid_origin = False
            break
        elif typ == -1 and lhs < c:
            valid_origin = False
            break
    if valid_origin:
        points.append((0, 0))

    # Step 2: Intersections with axes
    for a, b, c, typ in constraints:
        # x-intercept (y = 0)
        if a != 0:
            x = c / a if typ == 1 else c / a  # For >=, x-intercept is still c/a
            y = 0
            if x >= 0:
                valid = True
                for a1, b1, c1, typ1 in constraints:
                    lhs = a1*x + b1*y
                    if (typ1 == 1 and lhs > c1) or (typ1 == -1 and lhs < c1):
                        valid = False
                        break
                if valid:
                    points.append((x, y))

        # y-intercept (x = 0)
        if b != 0:
            x = 0
            y = c / b if typ == 1 else c / b
            if y >= 0:
                valid = True
                for a1, b1, c1, typ1 in constraints:
                    lhs = a1*x + b1*y
                    if (typ1 == 1 and lhs > c1) or (typ1 == -1 and lhs < c1):
                        valid = False
                        break
                if valid:
                    points.append((x, y))

    # Step 3: Intersections between lines
    n = len(constraints)
    for i in range(n):
        a1, b1, c1, typ1 = constraints[i]
        for j in range(i + 1, n):
            a2, b2, c2, typ2 = constraints[j]

            det = a1*b2 - a2*b1
            if det != 0:
                x = (c1*b2 - c2*b1) / det
                y = (a1*c2 - a2*c1) / det

                if x >= 0 and y >= 0:
                    valid = True
                    for a, b, c, typ in constraints:
                        lhs = a*x + b*y
                        if (typ == 1 and lhs > c) or (typ == -1 and lhs < c):
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

    # Check for unbounded
    if best_point is not None:
        x, y = best_point
        unbounded = False
        
        # Check if can increase x
        if x == 0 and objective[0] > 0:
            has_x_upper_limit = False
            for a, b, c, typ in constraints:
                if abs(a) > 1e-12:
                    if typ == 1 and a > 0:  # a*x <= c, limits x from above
                        has_x_upper_limit = True
                    elif typ == -1 and a < 0:  # -a*x <= -c, i.e. x >= c/(-a), limits x from below
                        has_x_upper_limit = True  # since x >= something, but for increasing x, if it's binding, may not
            # Actually, for x=0, if p>0, and no a>0 for <= (x<=), then can increase x
            has_x_limit = False
            for a, b, c, typ in constraints:
                if abs(a) > 1e-12 and typ == 1 and a > 0:
                    has_x_limit = True
            if not has_x_limit:
                unbounded = True
        
        # Check if can increase y
        if y == 0 and objective[1] > 0:
            has_y_limit = False
            for a, b, c, typ in constraints:
                if abs(b) > 1e-12 and typ == 1 and b > 0:
                    has_y_limit = True
            if not has_y_limit:
                unbounded = True
        
        if unbounded:
            return None, None

    return best_point, best_val