import matplotlib.pyplot as plt


def plot_graph(constraints, solution_point):
    if not constraints:
        raise ValueError("No constraints to plot")

    x_vals = [i * 0.1 for i in range(0, 200)]
    plt.figure(figsize=(6, 6))

    y_all = []

    for a, b, c in constraints:
        if abs(b) > 1e-12:
            y_vals = [(c - a * x) / b for x in x_vals]
            y_all.append(y_vals)
            plt.plot(x_vals, y_vals, lw=1.5, label=f'{a}x + {b}y ≤ {c}')
        elif abs(a) > 1e-12:
            x_line = c / a
            plt.axvline(x=x_line, lw=1.5, label=f'{a}x ≤ {c}')

    if y_all:
        y_min = [min(line[i] for line in y_all) for i in range(len(x_vals))]
        plt.fill_between(x_vals, [0] * len(x_vals), y_min, where=[y >= 0 for y in y_min], alpha=0.25)

    corner_points = set()
    n = len(constraints)

    for i in range(n):
        a1, b1, c1 = constraints[i]
        for j in range(i + 1, n):
            a2, b2, c2 = constraints[j]
            det = a1 * b2 - a2 * b1
            if abs(det) < 1e-12:
                continue

            x = (c1 * b2 - c2 * b1) / det
            y = (a1 * c2 - a2 * c1) / det

            if x >= -1e-9 and y >= -1e-9 and all(a * x + b * y <= c + 1e-9 for a, b, c in constraints):
                corner_points.add((x, y))

    for a, b, c in constraints:
        if abs(a) > 1e-12:
            x = c / a
            if x >= -1e-9 and all(a1 * x + b1 * 0 <= c1 + 1e-9 for a1, b1, c1 in constraints):
                corner_points.add((x, 0))

        if abs(b) > 1e-12:
            y = c / b
            if y >= -1e-9 and all(a1 * 0 + b1 * y <= c1 + 1e-9 for a1, b1, c1 in constraints):
                corner_points.add((0, y))

    if all(a * 0 + b * 0 <= c + 1e-9 for a, b, c in constraints):
        corner_points.add((0, 0))

    corner_points = sorted(corner_points)

    for x, y in corner_points:
        plt.plot(x, y, 'go')
        plt.text(x, y, f'({round(x, 2)}, {round(y, 2)})', fontsize=8, color='green')

    if solution_point:
        plt.plot(solution_point[0], solution_point[1], 'ro', markersize=10, label='Optimal Solution')

    all_x = [p[0] for p in corner_points] + [0]
    all_y = [p[1] for p in corner_points] + [0]

    max_x = max(all_x + [10])
    max_y = max(all_y + [10])

    plt.xlim(0, max_x + 5)
    plt.ylim(0, max_y + 5)

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Graphical Method - Feasible Region')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()