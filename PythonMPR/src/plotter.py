import matplotlib
matplotlib.use('TkAgg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


def plot_graph(constraints, solution_point):
    if not constraints:
        raise ValueError("No constraints to plot")

    # Calculate dynamic range based on constraint values
    max_val = 10  # minimum range

    for a, b, c, typ in constraints:
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

    # Determine valid x-range based on vertical constraints
    x_min = 0
    x_max = plot_range
    
    vertical_constraints = []
    sloped_constraints = []
    
    for a, b, c, typ in constraints:
        if abs(b) < 1e-12 and abs(a) > 1e-12:  # vertical line
            vertical_constraints.append((a, c, typ))
        else:
            sloped_constraints.append((a, b, c, typ))
    
    for a, c, typ in vertical_constraints:
        x_bound = c / a
        if typ == 1:  # a*x <= c, so x <= c/a
            x_max = min(x_max, x_bound)
        else:  # a*x >= c, so x >= c/a
            x_min = max(x_min, x_bound)
    
    # Ensure valid range
    if x_min >= x_max:
        x_min = 0
        x_max = plot_range
    
    # Generate x_vals within valid range
    x_vals = [x_min + i * ((x_max - x_min) / num_points) for i in range(0, num_points + 1)]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    y_all = []
    
    # Plot constraints with numbered labels
    for i, (a, b, c, typ) in enumerate(constraints, 1):
        sign_str = "≤" if typ == 1 else "≥"
        if abs(b) > 1e-12:
            y_vals = [(c - a * x) / b for x in x_vals]
            y_all.append((y_vals, typ))
            ax.plot(x_vals, y_vals, lw=1.5, label=f'Constraint {i}: {a}x + {b}y {sign_str} {c}')
        elif abs(a) > 1e-12:
            x_line = c / a
            ax.axvline(x=x_line, lw=1.5, label=f'Constraint {i}: {a}x {sign_str} {c}')
    
    # For filling the feasible region, for each x, determine y bounds from all constraints
    y_lower = []
    y_upper = []
    for x in x_vals:
        lower_bound = 0.0
        upper_bound = plot_range

        for a, b, c, typ in constraints:
            # vertical constraints handled by x-range above
            if abs(b) < 1e-12:
                continue

            y_line = (c - a * x) / b

            if b > 0:
                if typ == 1:
                    # a x + b y <= c -> y <= y_line
                    upper_bound = min(upper_bound, y_line)
                else:
                    # a x + b y >= c -> y >= y_line
                    lower_bound = max(lower_bound, y_line)
            else:  # b < 0
                if typ == 1:
                    # a x + b y <= c -> y >= y_line (flip direction)
                    lower_bound = max(lower_bound, y_line)
                else:
                    # a x + b y >= c -> y <= y_line
                    upper_bound = min(upper_bound, y_line)

        y_lower.append(max(0.0, lower_bound))
        y_upper.append(min(plot_range, upper_bound))

    # Only fill where region is non-empty
    valid_mask = [y_u >= y_l for y_l, y_u in zip(y_lower, y_upper)]
    if any(valid_mask):
        ax.fill_between(x_vals, y_lower, y_upper, where=valid_mask, alpha=0.25)

    corner_points = set()
    n = len(constraints)

    for i in range(n):
        a1, b1, c1, typ1 = constraints[i]
        for j in range(i + 1, n):
            a2, b2, c2, typ2 = constraints[j]
            det = a1 * b2 - a2 * b1
            if abs(det) < 1e-12:
                continue

            x = (c1 * b2 - c2 * b1) / det
            y = (a1 * c2 - a2 * c1) / det

            if x >= -1e-9 and y >= -1e-9:
                valid = True
                for a, b, c, typ in constraints:
                    lhs = a * x + b * y
                    if (typ == 1 and lhs > c + 1e-9) or (typ == -1 and lhs < c - 1e-9):
                        valid = False
                        break
                if valid:
                    corner_points.add((x, y))

    for a, b, c, typ in constraints:
        if abs(a) > 1e-12:
            x = c / a
            if x >= -1e-9:
                valid = True
                for a1, b1, c1, typ1 in constraints:
                    lhs = a1 * x + b1 * 0
                    if (typ1 == 1 and lhs > c1 + 1e-9) or (typ1 == -1 and lhs < c1 - 1e-9):
                        valid = False
                        break
                if valid:
                    corner_points.add((x, 0))

        if abs(b) > 1e-12:
            y = c / b
            if y >= -1e-9:
                valid = True
                for a1, b1, c1, typ1 in constraints:
                    lhs = a1 * 0 + b1 * y
                    if (typ1 == 1 and lhs > c1 + 1e-9) or (typ1 == -1 and lhs < c1 - 1e-9):
                        valid = False
                        break
                if valid:
                    corner_points.add((0, y))

    valid_origin = True
    for a, b, c, typ in constraints:
        lhs = a * 0 + b * 0
        if (typ == 1 and lhs > c + 1e-9) or (typ == -1 and lhs < c - 1e-9):
            valid_origin = False
            break
    if valid_origin:
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

    # Fixed bounds 0..7 per user request
    xlim_max = 7
    ylim_max = 7
    ax.set_xlim(0, xlim_max)
    ax.set_ylim(0, ylim_max)

    # Enforce 1 unit = 1 unit in both dimensions (square scaling)
    ax.set_aspect('equal', adjustable='box')

    # Use integer ticks at 1-unit increments
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))

    # Dark theme styling for plot elements
    ax.set_facecolor('#0f172a')
    fig.patch.set_facecolor('#0f172a')
    ax.spines['bottom'].set_color('#e2e8f0')
    ax.spines['top'].set_color('#e2e8f0')
    ax.spines['left'].set_color('#e2e8f0')
    ax.spines['right'].set_color('#e2e8f0')
    ax.tick_params(colors='#e2e8f0', which='both')
    ax.xaxis.label.set_color('#e2e8f0')
    ax.yaxis.label.set_color('#e2e8f0')
    ax.title.set_color('#e2e8f0')
    ax.grid(True, linestyle='--', alpha=0.5, color='#334155')

    legend = ax.legend()
    if legend:
        for text in legend.get_texts():
            text.set_color('#e2e8f0')
        legend.get_frame().set_facecolor('#1e293b')
        legend.get_frame().set_edgecolor('#334155')

    # Reduce extra whitespace around plot to minimize margin
    fig.tight_layout(pad=0.5)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)

    return fig, corner_points
def plot_empty_graph():
    fig, ax = plt.subplots(figsize=(8, 6))

    # Same limits as your main graph
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 7)

    # Square scaling
    ax.set_aspect('equal', adjustable='box')

    # Integer ticks
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))

    # Dark theme styling (same as your graph)
    ax.set_facecolor('#0f172a')
    fig.patch.set_facecolor('#0f172a')

    ax.spines['bottom'].set_color('#e2e8f0')
    ax.spines['top'].set_color('#e2e8f0')
    ax.spines['left'].set_color('#e2e8f0')
    ax.spines['right'].set_color('#e2e8f0')

    ax.tick_params(colors='#e2e8f0', which='both')
    ax.xaxis.label.set_color('#e2e8f0')
    ax.yaxis.label.set_color('#e2e8f0')

    ax.grid(True, linestyle='--', alpha=0.5, color='#334155')

    # Optional message (UI polish)
    ax.text(3.5, 3.5, "Click 'Solve Problem' to plot graph",
            color='#64748b', ha='center', va='center', fontsize=12)

    fig.tight_layout(pad=0.5)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.95, bottom=0.05)

    return fig