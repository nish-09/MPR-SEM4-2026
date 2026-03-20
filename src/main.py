import tkinter as tk
from solver import solve_lpp
from plotter import plot_graph

constraints_ui = []

DEFAULT_FONT = ("Segoe UI", 11)

# ---------- Helper ----------
def get_float(entry, name):
    val = entry.get().strip()
    if val == "":
        raise ValueError(f"{name} cannot be empty")
    try:
        return float(val)
    except ValueError:
        raise ValueError(f"{name} must be a valid number")

# ---------- Layout ----------

def refresh_layout():
    for i, item in enumerate(constraints_ui):
        a, b, sign_var, c, delete_btn, plus_label, y_label, sign_menu = item
        row = i + 1

        a.grid(row=row, column=1, padx=3, pady=2)
        plus_label.grid(row=row, column=2, padx=3, pady=2)
        b.grid(row=row, column=3, padx=3, pady=2)
        y_label.grid(row=row, column=4, padx=3, pady=2)
        sign_menu.grid(row=row, column=5, padx=3, pady=2)
        c.grid(row=row, column=6, padx=3, pady=2)
        delete_btn.grid(row=row, column=7, padx=3, pady=2)

    add_btn.grid(row=len(constraints_ui)+1, column=0, columnspan=8, pady=(10, 0), sticky="ew")

# ---------- Add Constraint ----------

def add_constraint():
    a = tk.Entry(constraints_frame, width=6, font=DEFAULT_FONT)
    plus_label = tk.Label(constraints_frame, text="x +", font=DEFAULT_FONT)
    b = tk.Entry(constraints_frame, width=6, font=DEFAULT_FONT)
    y_label = tk.Label(constraints_frame, text="y", font=DEFAULT_FONT)

    sign_var = tk.StringVar(value="≤")
    sign_menu = tk.OptionMenu(constraints_frame, sign_var, "<", "≤", ">", "≥")
    sign_menu.config(font=DEFAULT_FONT)

    c = tk.Entry(constraints_frame, width=6, font=DEFAULT_FONT)

    delete_btn = tk.Button(constraints_frame, text="X", bg="red", fg="white", font=DEFAULT_FONT,
                           command=lambda: remove_constraint(a))

    constraints_ui.append((a, b, sign_var, c, delete_btn, plus_label, y_label, sign_menu))
    refresh_layout()

# ---------- Remove ----------

def remove_constraint(entry_ref):
    global constraints_ui
    updated = []

    for item in constraints_ui:
        if item[0] is entry_ref:
            for widget in item:
                if hasattr(widget, "destroy"):
                    widget.destroy()
        else:
            updated.append(item)

    constraints_ui = updated
    refresh_layout()

# ---------- Solve ----------

def run_solver():
    try:
        if not constraints_ui:
            raise ValueError("At least one constraint is required")

        constraints = []

        for i, (a_e, b_e, sign_v, c_e, *_ ) in enumerate(constraints_ui, start=1):
            a = get_float(a_e, f"a{i}")
            b = get_float(b_e, f"b{i}")
            c = get_float(c_e, f"c{i}")
            sign = sign_v.get()

            if a == 0 and b == 0:
                raise ValueError(f"Constraint {i} has a=b=0, invalid")

            # Normalize to <= form for solver and plotter
            if sign in ("≤", "<=", "<"):
                constraints.append((a, b, c))
            elif sign in ("≥", ">=", ">"):
                constraints.append((-a, -b, -c))
            else:
                raise ValueError(f"Constraint {i} has unknown sign '{sign}'")

        p = get_float(entry_p, "p")
        q = get_float(entry_q, "q")

        sol_point, sol_val = solve_lpp(constraints, (p, q), var_max.get())

        if sol_point is None:
            result_label.config(text="No feasible solution found", fg="red")
            return

        result_label.config(
            text=f"x={round(sol_point[0],2)}, y={round(sol_point[1],2)} | Z={round(sol_val,2)}",
            fg="green"
        )

        plot_graph(constraints, sol_point)

    except ValueError as e:
        result_label.config(text=f"Input error: {e}", fg="red")
    except Exception as e:
        result_label.config(text=f"Unexpected error: {e}", fg="red")

# ---------- UI ----------

root = tk.Tk()
root.title("Graphical Method LPP Solver")
root.configure(bg="#f8f9fb")
root.geometry("1100x620")

header = tk.Label(root, text="Graphical Method Solver", font=("Segoe UI", 18, "bold"), bg="#f8f9fb")
header.grid(row=0, column=0, columnspan=2, pady=10)

# Constraint frame
constraints_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove", padx=10, pady=10)
constraints_frame.grid(row=1, column=0, padx=12, pady=8, sticky="nsew")

constraint_header = tk.Label(constraints_frame, text="Constraint format: a x + b y [sign] c", font=("Segoe UI", 12, "bold"), bg="#ffffff")
constraint_header.grid(row=0, column=0, columnspan=8, pady=(0, 6), sticky="w")

add_btn = tk.Button(constraints_frame, text="Add Constraint", font=DEFAULT_FONT, command=add_constraint, bg="#1f77b4", fg="white")

# Objective frame
objective_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove", padx=10, pady=10)
objective_frame.grid(row=2, column=0, padx=12, pady=8, sticky="nsew")

objective_label = tk.Label(objective_frame, text="Z = p*x + q*y", font=DEFAULT_FONT, bg="#ffffff")
objective_label.grid(row=0, column=0, columnspan=4, pady=(0,8))

entry_p = tk.Entry(objective_frame, width=8, font=DEFAULT_FONT)
entry_p.grid(row=1, column=0, padx=6)

entry_q = tk.Entry(objective_frame, width=8, font=DEFAULT_FONT)
entry_q.grid(row=1, column=1, padx=6)

var_max = tk.BooleanVar(value=True)
max_radio = tk.Radiobutton(objective_frame, text="Max", variable=var_max, value=True, font=DEFAULT_FONT, bg="#ffffff")
min_radio = tk.Radiobutton(objective_frame, text="Min", variable=var_max, value=False, font=DEFAULT_FONT, bg="#ffffff")
max_radio.grid(row=1, column=2, padx=8)
min_radio.grid(row=1, column=3, padx=8)

solve_btn = tk.Button(objective_frame, text="Solve", command=run_solver, bg="#007acc", fg="white", font=("Segoe UI", 12, "bold"))
solve_btn.grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")

result_label = tk.Label(root, text="", font=("Segoe UI", 12, "bold"), bg="#f8f9fb")
result_label.grid(row=3, column=0, columnspan=2, pady=8)

# preset default constraints
add_constraint()
add_constraint()

root.mainloop()