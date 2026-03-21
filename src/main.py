import matplotlib
matplotlib.use('TkAgg')  # Set backend before importing pyplot
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from solver import solve_lpp
from plotter import plot_graph

constraints_ui = []

# Modern color scheme
PRIMARY_COLOR = "#2563eb"
SECONDARY_COLOR = "#64748b"
SUCCESS_COLOR = "#059669"
ERROR_COLOR = "#dc2626"
BACKGROUND_COLOR = "#f8fafc"
SURFACE_COLOR = "#ffffff"
TEXT_COLOR = "#1e293b"
ACCENT_COLOR = "#3b82f6"

DEFAULT_FONT = ("Segoe UI", 10)
HEADER_FONT = ("Segoe UI", 20, "bold")
LABEL_FONT = ("Segoe UI", 11, "bold")
BUTTON_FONT = ("Segoe UI", 10, "bold")

# Style configuration
def configure_styles():
    style = ttk.Style()

    # Button styles
    style.configure("Primary.TButton",
                   background=PRIMARY_COLOR,
                   foreground="#000000",  # Changed to black
                   font=BUTTON_FONT,
                   padding=(5, 2),  # Made smaller
                   relief="flat")
    style.map("Primary.TButton",
             background=[("active", "#1d4ed8"), ("pressed", "#1e40af")],
             foreground=[("active", "#000000"), ("pressed", "#000000")])

    style.configure("Secondary.TButton",
                   background=SECONDARY_COLOR,
                   foreground="white",
                   font=BUTTON_FONT,
                   padding=(8, 4),
                   relief="flat")
    style.map("Secondary.TButton",
             background=[("active", "#475569"), ("pressed", "#334155")])

    style.configure("Danger.TButton",
                   background=ERROR_COLOR,
                   foreground="white",
                   font=BUTTON_FONT,
                   padding=(6, 3),
                   relief="flat")
    style.map("Danger.TButton",
             background=[("active", "#b91c1c"), ("pressed", "#991b1b")])

    # Label styles
    style.configure("Header.TLabel",
                   background=BACKGROUND_COLOR,
                   foreground=TEXT_COLOR,
                   font=HEADER_FONT)

    style.configure("Subheader.TLabel",
                   background=SURFACE_COLOR,
                   foreground=TEXT_COLOR,
                   font=LABEL_FONT)

    # Frame styles
    style.configure("Card.TFrame",
                   background=SURFACE_COLOR,
                   relief="solid",
                   borderwidth=1)

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
        a, x_label, plus_label, b, y_label, sign_var, sign_menu, c, delete_btn = item
        row = i + 2  # Start from row 2 since rows 0-1 have title and description

        a.grid(row=row, column=1, padx=3, pady=3, sticky="ew")
        x_label.grid(row=row, column=2, padx=(0, 3), pady=3)
        plus_label.grid(row=row, column=3, padx=3, pady=3)
        b.grid(row=row, column=4, padx=3, pady=3, sticky="ew")
        y_label.grid(row=row, column=5, padx=(0, 3), pady=3)
        sign_menu.grid(row=row, column=6, padx=3, pady=3, sticky="ew")
        c.grid(row=row, column=7, padx=3, pady=3, sticky="ew")
        delete_btn.grid(row=row, column=8, padx=3, pady=3)

    # Position add button after all constraints
    add_btn.grid(row=len(constraints_ui)+2, column=0, columnspan=9, pady=(15, 10), padx=10, sticky="ew")

# ---------- Add Constraint ----------

def add_constraint():
    a = tk.Entry(constraints_frame, width=8, font=DEFAULT_FONT,
                relief="groove", bd=2, bg="white", highlightthickness=1, highlightcolor=PRIMARY_COLOR)
    x_label = tk.Label(constraints_frame, text="x", font=LABEL_FONT,
                      bg=SURFACE_COLOR, fg=TEXT_COLOR)
    plus_label = tk.Label(constraints_frame, text="+", font=LABEL_FONT,
                         bg=SURFACE_COLOR, fg=TEXT_COLOR)
    b = tk.Entry(constraints_frame, width=8, font=DEFAULT_FONT,
                relief="groove", bd=2, bg="white", highlightthickness=1, highlightcolor=PRIMARY_COLOR)
    y_label = tk.Label(constraints_frame, text="y", font=LABEL_FONT,
                      bg=SURFACE_COLOR, fg=TEXT_COLOR)

    sign_var = tk.StringVar(value="≤")
    sign_menu = tk.OptionMenu(constraints_frame, sign_var, "≤", "≥", "<", ">")
    sign_menu.config(font=DEFAULT_FONT, bg="white", relief="groove", bd=2,
                    highlightbackground=PRIMARY_COLOR, highlightthickness=1, width=3)

    c = tk.Entry(constraints_frame, width=8, font=DEFAULT_FONT,
                relief="groove", bd=2, bg="white", highlightthickness=1, highlightcolor=PRIMARY_COLOR)

    delete_btn = tk.Button(constraints_frame, text="🗑️", bg=ERROR_COLOR, fg="white",
                          font=BUTTON_FONT, relief="flat", bd=0, padx=8, pady=2,
                          command=lambda: remove_constraint(a))
    delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#b91c1c"))
    delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg=ERROR_COLOR))

    constraints_ui.append((a, x_label, plus_label, b, y_label, sign_var, sign_menu, c, delete_btn))
    refresh_layout()

# ---------- Remove ----------

def remove_constraint(entry_ref):
    global constraints_ui
    updated = []

    for item in constraints_ui:
        a, x_label, plus_label, b, y_label, sign_var, sign_menu, c, delete_btn = item
        if a is entry_ref:
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

        for i, (a_e, x_label, plus_label, b_e, y_label, sign_v, sign_menu, c_e, delete_btn) in enumerate(constraints_ui, start=1):
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
            error_message = "No feasible solution found.\n\nThis means the constraints are too restrictive or inconsistent."
            result_label.config(text=f"❌ {error_message}", fg=ERROR_COLOR)
            status_label.config(text="No solution found", foreground=ERROR_COLOR)
            return

        # Plot graph and get corner points in embedded frame
        global graph_canvas
        if graph_canvas is not None:
            graph_canvas.get_tk_widget().destroy()
            plt.close('all')  # Close any existing matplotlib figures

        fig, corner_points = plot_graph(constraints, sol_point)
        graph_canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        graph_canvas.draw()
        graph_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Build details text area content
        corner_text = "\n".join([f"({round(x, 3)}, {round(y, 3)})" for x, y in sorted(corner_points)])

        # As 'point of intersection', report all corner intersection points
        intersection_text = corner_text if corner_text else "None"

        # Edge lines (the constraints) as displayed
        edge_text = "\n".join([f"Constraint {i}: {a}x + {b}y ≤ {c}" for i, (a, b, c) in enumerate(constraints, 1)])

        # Analyze which constraints bound the feasible region
        binding_constraints = set()

        bounded_by_axes = set()

        for x, y in corner_points:
            # Check if point is on x-axis (y ≈ 0)
            if abs(y) < 1e-6:
                bounded_by_axes.add("x-axis (y ≥ 0)")

            # Check if point is on y-axis (x ≈ 0)
            if abs(x) < 1e-6:
                bounded_by_axes.add("y-axis (x ≥ 0)")

            # Check which constraints are binding at this point
            for i, (a, b, c) in enumerate(constraints, 1):
                if abs(a * x + b * y - c) < 1e-6:  # Point lies on constraint
                    binding_constraints.add(f"Constraint {i}: {a}x + {b}y ≤ {c}")

        # Format corner points
        corner_text = "\n".join([f"({round(x, 3)}, {round(y, 3)})" for x, y in sorted(corner_points)])

        # Format binding constraints
        constraints_text = "\n".join(sorted(binding_constraints)) if binding_constraints else "None"
        axes_text = "\n".join(sorted(bounded_by_axes)) if bounded_by_axes else "None"

        # Prepare details text (below graph)
        details_data = (
            f"Corner Points:\n{corner_text or 'None'}\n\n"
            f"Optimal Point:\n({round(sol_point[0], 3)}, {round(sol_point[1], 3)})\n\n"
            f"Intersection Points (same as corner points):\n{intersection_text}\n\n"
            f"Edge Lines (Constraints):\n{edge_text}\n\n"
            f"Binding Constraints:\n{constraints_text}\n\n"
            f"Bounded by Axes:\n{axes_text}"
        )

        details_text.config(state="normal")
        details_text.delete("1.0", "end")
        details_text.insert("end", details_data)
        details_text.config(state="disabled")

        # Update result summary label
        result_label.config(
            text=f"✅ Optimal Solution Found! | Point: ({round(sol_point[0], 3)}, {round(sol_point[1], 3)}) | Z = {round(sol_val, 3)}",
            fg=SUCCESS_COLOR
        )
        status_label.config(text="Solution found successfully", foreground=SUCCESS_COLOR)

    except ValueError as e:
        error_message = f"Input Error:\n\n{str(e)}\n\nPlease check your inputs and try again."
        result_label.config(text=f"❌ {error_message}", fg=ERROR_COLOR)
        status_label.config(text="Input validation failed", foreground=ERROR_COLOR)
    except Exception as e:
        error_message = f"Unexpected Error:\n\n{str(e)}\n\nPlease report this issue."
        result_label.config(text=f"❌ {error_message}", fg=ERROR_COLOR)
        status_label.config(text="An error occurred", foreground=ERROR_COLOR)

# ---------- UI ----------

root = tk.Tk()
root.title("LPP Graphical Method Solver")
root.configure(bg=BACKGROUND_COLOR)
root.geometry("1400x800")
root.minsize(800, 600)  # Set minimum window size for responsiveness

# Configure grid for main window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Configure styles
configure_styles()

# Main container
main_frame = ttk.Frame(root, style="Card.TFrame")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

# Header section
header_frame = ttk.Frame(main_frame, style="Card.TFrame")
header_frame.pack(fill="x", pady=(0, 20))

header = ttk.Label(header_frame, text="Linear Programming Problem Solver",
                  style="Header.TLabel", anchor="center")
header.pack(pady=15)

# Content frame with responsive layout
content_frame = ttk.Frame(main_frame, style="Card.TFrame")
content_frame.pack(fill="both", expand=True)

# Configure grid weights for responsive panels
content_frame.grid_rowconfigure(0, weight=1)
content_frame.grid_columnconfigure(0, weight=1)
content_frame.grid_columnconfigure(1, weight=1)

# Left panel - Input with scrolling
left_panel = ttk.Frame(content_frame, style="Card.TFrame")
left_panel.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
left_panel.grid_rowconfigure(0, weight=1)  # Constraints canvas expands
left_panel.grid_rowconfigure(1, weight=0)  # Objective frame does not expand
left_panel.grid_columnconfigure(0, weight=1)
left_panel.grid_columnconfigure(1, weight=0)

# Create a scrollable frame for constraints
constraints_canvas = tk.Canvas(left_panel, bg=SURFACE_COLOR, highlightthickness=0, height=200)
scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=constraints_canvas.yview)
constraints_frame = ttk.Frame(constraints_canvas, style="Card.TFrame")

constraints_frame.bind(
    "<Configure>",
    lambda e: constraints_canvas.configure(scrollregion=constraints_canvas.bbox("all"))
)

constraints_canvas.create_window((0, 0), window=constraints_frame, anchor="nw", tags="frame")
constraints_canvas.configure(yscrollcommand=scrollbar.set)

# Grid scrollable frame in left_panel
constraints_canvas.grid(row=0, column=0, sticky="nsew", pady=(0, 15), padx=15)
scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 15))

# Enable mousewheel scrolling
def _on_mousewheel(event):
    constraints_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
constraints_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Use grid layout for constraints_frame
constraints_frame.grid_columnconfigure(0, weight=1)
constraints_frame.grid_columnconfigure(1, weight=0)
constraints_frame.grid_columnconfigure(2, weight=0)
constraints_frame.grid_columnconfigure(3, weight=0)
constraints_frame.grid_columnconfigure(4, weight=0)
constraints_frame.grid_columnconfigure(5, weight=0)
constraints_frame.grid_columnconfigure(6, weight=0)
constraints_frame.grid_columnconfigure(7, weight=0)
constraints_frame.grid_columnconfigure(8, weight=0)

constraint_title = ttk.Label(constraints_frame, text="Constraints",
                            style="Subheader.TLabel")
constraint_title.grid(row=0, column=0, columnspan=8, sticky="w", pady=(10, 5), padx=10)

constraint_desc = ttk.Label(constraints_frame,
                           text="Add inequalities in the form: ax + by ≤ c",
                           font=("Segoe UI", 9), foreground=SECONDARY_COLOR,
                           background=SURFACE_COLOR)
constraint_desc.grid(row=1, column=0, columnspan=8, sticky="w", pady=(0, 10), padx=10)

add_btn = ttk.Button(constraints_frame, text="Add Constraint",
                    style="Primary.TButton", command=add_constraint)
# add_btn will be positioned by refresh_layout

# Objective frame
objective_frame = ttk.Frame(left_panel, style="Card.TFrame")
objective_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(15, 0), padx=15, ipadx=10, ipady=10)

objective_title = ttk.Label(objective_frame, text="Objective Function",
                           style="Subheader.TLabel")
objective_title.pack(anchor="w", pady=(15, 5))

objective_desc = ttk.Label(objective_frame,
                          text="Maximize or minimize: Z = px + qy",
                          font=("Segoe UI", 9), foreground=SECONDARY_COLOR,
                          background=SURFACE_COLOR)
objective_desc.pack(anchor="w", pady=(0, 10))

obj_input_frame = ttk.Frame(objective_frame, style="Card.TFrame")
obj_input_frame.pack(fill="x", pady=(0, 10))

ttk.Label(obj_input_frame, text="Z =", font=LABEL_FONT,
         background=SURFACE_COLOR).grid(row=0, column=0, padx=(0, 5), pady=5)
entry_p = tk.Entry(obj_input_frame, width=8, font=DEFAULT_FONT,
                  relief="groove", bd=2, bg="white", highlightthickness=1, highlightcolor=PRIMARY_COLOR)
entry_p.grid(row=0, column=1, padx=5, pady=5)
ttk.Label(obj_input_frame, text="x +", font=LABEL_FONT,
         background=SURFACE_COLOR).grid(row=0, column=2, padx=5, pady=5)
entry_q = tk.Entry(obj_input_frame, width=8, font=DEFAULT_FONT,
                  relief="groove", bd=2, bg="white", highlightthickness=1, highlightcolor=PRIMARY_COLOR)
entry_q.grid(row=0, column=3, padx=5, pady=5)
ttk.Label(obj_input_frame, text="y", font=LABEL_FONT,
         background=SURFACE_COLOR).grid(row=0, column=4, padx=(5, 15), pady=5)

# Radio buttons
radio_frame = ttk.Frame(obj_input_frame, style="Card.TFrame")
radio_frame.grid(row=0, column=5, padx=(0, 10))

var_max = tk.BooleanVar(value=True)
max_radio = tk.Radiobutton(radio_frame, text="Maximize", variable=var_max,
                          value=True, font=DEFAULT_FONT, bg=SURFACE_COLOR,
                          activebackground=SURFACE_COLOR, selectcolor=PRIMARY_COLOR)
min_radio = tk.Radiobutton(radio_frame, text="Minimize", variable=var_max,
                          value=False, font=DEFAULT_FONT, bg=SURFACE_COLOR,
                          activebackground=SURFACE_COLOR, selectcolor=PRIMARY_COLOR)
max_radio.pack(side="left", padx=(0, 10))
min_radio.pack(side="left")

# Solve button
solve_btn = ttk.Button(objective_frame, text="Solve Problem",
                      style="Primary.TButton", command=run_solver)
solve_btn.pack(fill="x", pady=(10, 15))

# Right panel - Results and Graph
right_panel = ttk.Frame(content_frame, style="Card.TFrame")
right_panel.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
right_panel.grid_rowconfigure(2, weight=1)  # Graph takes up most space
right_panel.grid_rowconfigure(3, weight=0)  # Details text
right_panel.grid_columnconfigure(0, weight=1)

results_title = ttk.Label(right_panel, text="Results",
                         style="Subheader.TLabel")
results_title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))

# Status bar moved to after results title
status_label = ttk.Label(right_panel, text="Ready to solve LPP",
                        font=("Segoe UI", 9), foreground=SECONDARY_COLOR,
                        background=SURFACE_COLOR)
status_label.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 10))

# Graph container (embedded matplotlib) - takes up most of the space
graph_frame = ttk.Frame(right_panel, style="Card.TFrame")
graph_frame.grid(row=2, column=0, padx=15, pady=(0, 10), sticky="nsew")

# Placeholder for the embedded chart
graph_canvas = None

# Details panel below graph (with scrolling if needed)
details_frame = ttk.Frame(right_panel, style="Card.TFrame")
details_frame.grid(row=3, column=0, padx=15, pady=(0, 10), sticky="ew")

details_text = tk.Text(details_frame, height=8, wrap="word", font=("Segoe UI", 9),
                        bg=SURFACE_COLOR, fg=TEXT_COLOR, bd=1, relief="groove")
details_text.pack(fill="both", expand=True)
details_text.config(state="disabled")

result_label = tk.Label(right_panel, text="Enter constraints and objective function,\nthen click 'Solve Problem' to see results.",
                       font=("Segoe UI", 10), bg=SURFACE_COLOR, fg=TEXT_COLOR,
                       justify="left", anchor="w", wraplength=400)
result_label.grid(row=4, column=0, sticky="nsew", padx=15, pady=(0, 15))

# Preset default constraints
add_constraint()
add_constraint()

print("LPP Graphical Method Solver starting...")
root.mainloop()