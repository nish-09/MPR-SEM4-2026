import matplotlib
matplotlib.use('TkAgg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt


def plot_graph(constraints, solution_point):
    if not constraints:
        raise ValueError("No constraints to plot")

    # Calculate dynamic range based on constraint values
    max_val = 10  # minimum range

    for a, b, c in constraints:
        # Consider intersection points with axes
        if abs(a) > 1e-12:
            x_intersect = abs(c / a)
            max_val = max(max_val, x_intersect)
        if abs(b) > 1e-12:
            y_intersect = abs(c / b)
            max_val = max(max_val, y_intersect)

    # Add some padding and ensure reasonable minimum
    plot_range = max(20, max_val * 1.5)
    num_points = max(200, int(plot_range * 10))  # Ensure good resolution

    x_vals = [i * (plot_range / num_points) for i in range(0, num_points + 1)]

    plt.figure(figsize=(8, 6))

    y_all = []

def plot_graph(constraints, solution_point):
    if not constraints:
        raise ValueError("No constraints to plot")

    # Calculate dynamic range based on constraint values
    max_val = 10  # minimum range

    for a, b, c in constraints:
        # Consider intersection points with axes
        if abs(a) > 1e-12:
            x_intersect = abs(c / a)
            max_val = max(max_val, x_intersect)
        if abs(b) > 1e-12:
            y_intersect = abs(c / b)
            max_val = max(max_val, y_intersect)

    # Add some padding and ensure reasonable minimum
    plot_range = max(20, max_val * 1.5)
    num_points = max(200, int(plot_range * 10))  # Ensure good resolution

    x_vals = [i * (plot_range / num_points) for i in range(0, num_points + 1)]

    fig, ax = plt.subplots(figsize=(8, 6))

    y_all = []

    # Plot constraints with numbered labels
    for i, (a, b, c) in enumerate(constraints, 1):
        if abs(b) > 1e-12:
            y_vals = [(c - a * x) / b for x in x_vals]
            y_all.append(y_vals)
            ax.plot(x_vals, y_vals, lw=1.5, label=f'Constraint {i}: {a}x + {b}y ≤ {c}')
        elif abs(a) > 1e-12:
            x_line = c / a
            ax.axvline(x=x_line, lw=1.5, label=f'Constraint {i}: {a}x ≤ {c}')

    if y_all:
        y_min = [min(line[i] for line in y_all) for i in range(len(x_vals))]
        ax.fill_between(x_vals, [0] * len(x_vals), y_min, where=[y >= 0 for y in y_min], alpha=0.25)

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

    if solution_point:
        all_x.append(solution_point[0])
        all_y.append(solution_point[1])

    # Calculate dynamic limits based on all points and plot_range
    max_x = max(all_x + [plot_range * 0.8])
    max_y = max(all_y + [plot_range * 0.8])

    # Determine a unified scale so the region appears large and consistent
    axis_max = max(max_x, max_y, 1)
    xlim_max = max(axis_max * 1.5, 10)
    ylim_max = max(axis_max * 1.5, 10)

    # For small-scale problems, enforce a bigger frame to avoid tiny charts
    xlim_max = max(xlim_max, 15)
    ylim_max = max(ylim_max, 15)

    ax.set_xlim(0, xlim_max)
    ax.set_ylim(0, ylim_max)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Graphical Method - Feasible Region')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    fig.tight_layout()

    return fig, corner_points