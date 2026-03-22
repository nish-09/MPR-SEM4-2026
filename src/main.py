from click import style
import matplotlib
matplotlib.use('TkAgg')  # Set backend before importing pyplot
import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from solver import solve_lpp
from plotter import plot_graph
import customtkinter as ctk

ctk.set_appearance_mode("blue")   # options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # optional: "blue", "green", "dark-blue"

constraints_ui = []

# Graph state for view controls
current_fig = None
current_zoom = 1.0
MIN_ZOOM = 0.3
MAX_ZOOM = 2.0

# Dark theme color scheme
PRIMARY_COLOR = "#14b8a6"      
SECONDARY_COLOR = "#475569"
SUCCESS_COLOR = "#4ade80"
ERROR_COLOR = "#f87171"
BACKGROUND_COLOR = "#020617"
SURFACE_COLOR = "#0f172a"
TEXT_COLOR = "#e2e8f0"
ACCENT_COLOR = "#22d3ee"
BORDER_COLOR = "#334155"  

DEFAULT_FONT = ("Segoe UI", 11)
HEADER_FONT = ("Acme", 26, "bold")
LABEL_FONT = ("Segoe UI", 11, "bold")
BUTTON_FONT = ("Segoe UI", 10, "bold")

# ========== REUSABLE BORDERED CONTAINER HELPER ==========
def create_bordered_container(parent, bg_color=SURFACE_COLOR, border_width=1, border_color=BORDER_COLOR, return_inner=False):
    """
    Create a bordered container using tk.Frame for reliable border rendering.
    
    Args:
        parent: Parent widget
        bg_color: Background color for the inner frame
        border_width: Border thickness in pixels
        border_color: Border color (hex or color name)
        return_inner: If True, returns (border_frame, inner_frame). If False, returns inner_frame only.
    
    Returns:
        inner_frame if return_inner=False, else (border_frame, inner_frame)
    """
    # Outer frame creates the border effect
    border_frame = tk.Frame(parent, bg=border_color, bd=0, highlightthickness=0)
    
    # Inner frame holds the content
    inner_frame = tk.Frame(border_frame, bg=bg_color, bd=0, highlightthickness=0)
    inner_frame.pack(fill="both", expand=True, padx=border_width, pady=border_width)
    
    if return_inner:
        return border_frame, inner_frame
    return inner_frame

# ========== TOOLBAR BUTTON WITH ACCENT BORDER ==========
def create_toolbar_button(parent, text, command, border_color=ACCENT_COLOR):
    """
    Create a toolbar button with custom colored border.
    
    Args:
        parent: Parent widget
        text: Button text
        command: Button command callback
        border_color: Border color (default: ACCENT_COLOR)
    
    Returns:
        Button widget
    """
    border_frame = tk.Frame(parent, bg=border_color, bd=0, highlightthickness=0)
    border_frame.pack(side="left", padx=5, pady=5)
    
    inner_frame = tk.Frame(border_frame, bg=SECONDARY_COLOR, bd=0, highlightthickness=0)
    inner_frame.pack(fill="both", padx=1, pady=1)
    
    btn = tk.Button(inner_frame, text=text, bg=SECONDARY_COLOR, fg=TEXT_COLOR,
                   font=BUTTON_FONT, relief="flat", bd=0, padx=8, pady=4,
                   command=command)
    btn.pack(fill="both", padx=2, pady=2)
    return btn

# Style configuration
def configure_styles():
    style = ttk.Style()

    style = ttk.Style()
    style.theme_use("clam")
    # Button styles
    style.configure("Primary.TButton",
                   background=PRIMARY_COLOR,
                   foreground="#ffffff",
                   font=BUTTON_FONT,
                   padding=(5, 2),  # Made smaller
                   relief="flat")
    style.map("Primary.TButton",
             background=[("active", "#2563eb"), ("pressed", "#1d4ed8")],
             foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])

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
             background=[("active", "#dc2626"), ("pressed", "#b91c1c")])

    style.configure("Success.TButton",
                   background=SUCCESS_COLOR,
                   foreground="white",
                   font=BUTTON_FONT,
                   padding=(5, 2),
                   relief="flat")
    style.map("Success.TButton",
             background=[("active", "#059669"), ("pressed", "#047857")],
             foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])

    # Label styles
    style.configure("Header.TLabel",
                   background="#0f172a",
                   foreground=TEXT_COLOR,
                   font=HEADER_FONT)

    style.configure("Subheader.TLabel",
                   background=SURFACE_COLOR,
                   foreground=TEXT_COLOR,
                   font=LABEL_FONT)

    # Combobox style with visible dropdown arrow
    style.configure("Constraint.TCombobox",
    foreground="#e2e8f0",
    background="#1e293b",
    fieldbackground="#1e293b",   # 🔥 main fix
    bordercolor="#22d3ee",
    lightcolor="#22d3ee",
    darkcolor="#22d3ee",
    arrowcolor="#22d3ee",
    borderwidth=0,
    relief="flat",
    highlightthickness=1,
    padding=4,
    font=("Segoe UI", 10)
    )
    style.map("Constraint.TCombobox",
    fieldbackground=[
        ("readonly", "#0f172a"),
        ("active", "#1e293b")   # 🔥 hover pe light
    ],
    background=[
        ("active", "#1e293b"),  # 🔥 arrow area bhi light
        ("!active", "#0f172a")
    ],
    foreground=[("readonly", "#e2e8f0")],
    selectbackground=[("readonly", "#1e293b")],
    selectforeground=[("readonly", "#e2e8f0")],
    arrowcolor=[("active", "#22d3ee"), ("!active", "#22d3ee")],
    bordercolor=[("active", "#38bdf8"), ("!active", "#22d3ee")]
    )

    # Scrollbar style (dark theme)
    style.configure("Vertical.TScrollbar",
                gripcount=0,
                background=SECONDARY_COLOR,   # thumb color
                darkcolor=SECONDARY_COLOR,
                lightcolor=SECONDARY_COLOR,
                troughcolor=BACKGROUND_COLOR, # track color
                bordercolor=BACKGROUND_COLOR,
                arrowcolor=TEXT_COLOR)

    style.map("Vertical.TScrollbar",
          background=[("active", PRIMARY_COLOR), ("pressed", ACCENT_COLOR)])

    # Frame styles (removed unreliable ttk borders)
    style.configure("Card.TFrame",
                   background=SURFACE_COLOR,
                   relief="flat",
                   borderwidth=0)

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

        a.grid(row=row, column=1, padx=3, pady=3)
        x_label.grid(row=row, column=2, padx=(0, 3), pady=3)
        plus_label.grid(row=row, column=3, padx=3, pady=3)
        b.grid(row=row, column=4, padx=3, pady=3)
        y_label.grid(row=row, column=5, padx=(0, 3), pady=3)
        sign_menu.grid(row=row, column=6, padx=3, pady=3, sticky="ew")
        c.grid(row=row, column=7, padx=3, pady=3)
        delete_btn.grid(row=row, column=8, padx=3, pady=3)

    # Position add button after all constraints
    add_btn.grid(row=len(constraints_ui)+2, column=0, columnspan=9, pady=(15, 10))
# ---------- Add Constraint ----------

def add_constraint():
    a = tk.Entry(
    constraints_frame_container,
    width=5,
    font=DEFAULT_FONT,
    justify="center",          # ✅ center text
    relief="groove",
    bd=2,
    bg="#1e293b",         # dark input background
    fg="#e2e8f0",       # light text
    insertbackground="#e2e8f0",
    highlightthickness=1,
    highlightbackground="#22d3ee",   # accent border always
    highlightcolor="#22d3ee", 
    )
    x_label = tk.Label(constraints_frame_container, text="x", font=LABEL_FONT,
                      bg=SURFACE_COLOR, fg=TEXT_COLOR)
    plus_label = tk.Label(constraints_frame_container, text="+", font=LABEL_FONT,
                         bg=SURFACE_COLOR, fg=TEXT_COLOR)
    b = tk.Entry(
    constraints_frame_container,
    width=5,
    font=DEFAULT_FONT,
    justify="center",
    relief="groove",
    bd=2,
    bg="#1e293b",         # dark input background
    fg="#e2e8f0",       # light text
    insertbackground="#e2e8f0",
    highlightthickness=1,
    highlightbackground="#22d3ee",   # accent border always
    highlightcolor="#22d3ee",        # same on focus
    )
    y_label = tk.Label(constraints_frame_container, text="y", font=LABEL_FONT,
                      bg=SURFACE_COLOR, fg=TEXT_COLOR)

    sign_var = tk.StringVar(value="≤")
    sign_menu = ctk.CTkComboBox(
    constraints_frame_container,
    values=["≤", "≥", "<", ">"],
    width=70,
    height=30,
    corner_radius=8,
    border_width=1,
    border_color="#22d3ee",
    fg_color="#0f172a",
    text_color="#e2e8f0",
    button_color="#1e293b",
    button_hover_color="#334155",
    dropdown_fg_color="#0f172a",
    justify="center"
    ) # Set default to first value

    c = tk.Entry(
    constraints_frame_container,
    width=5,
    font=DEFAULT_FONT,
    justify="center",
    relief="groove",
    bd=2,
    bg="#1e293b",         # dark input background
    fg="#e2e8f0",       # light text
    insertbackground="#e2e8f0",  # cursor color (important!)
    highlightthickness=1,
    highlightbackground="#22d3ee",   # accent border always
    highlightcolor="#22d3ee", 
    )

    delete_btn = ctk.CTkButton(
    constraints_frame_container,
    text="🗑",
    width=30,
    height=30,
    corner_radius=8,
    fg_color="#dc2626",
    hover_color="#ef4444",
    text_color="white",
    command=lambda: remove_constraint(a)
    )

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

# ---------- Graph View Controls ----------

def refresh_plot_view():
    global current_fig, graph_canvas, current_zoom
    if current_fig is None or graph_canvas is None:
        return

    ax = current_fig.axes[0]
    base_range = 7.0
    view_range = max(1.0, min(base_range, base_range / current_zoom))

    ax.set_xlim(0, view_range)
    ax.set_ylim(0, view_range)
    graph_canvas.draw_idle()
    status_label.config(text=f"View range set to 0–{view_range:.1f}", foreground=SUCCESS_COLOR)


def zoom_in():
    global current_zoom
    current_zoom = min(MAX_ZOOM, current_zoom * 1.25)
    refresh_plot_view()


def zoom_out():
    global current_zoom
    current_zoom = max(MIN_ZOOM, current_zoom / 1.25)
    refresh_plot_view()


def reset_view():
    global current_zoom
    current_zoom = 1.0
    refresh_plot_view()


def save_graph_image():
    global current_fig
    if current_fig is None:
        status_label.config(text="No graph to save", foreground=ERROR_COLOR)
        return

    file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                             filetypes=[('PNG Image', '*.png'), ('JPEG Image', '*.jpg'), ('All Files', '*.*')])
    if file_path:
        try:
            current_fig.savefig(file_path, dpi=150, bbox_inches='tight', facecolor=current_fig.get_facecolor())
            status_label.config(text=f"Graph saved to {file_path}", foreground=SUCCESS_COLOR)
        except Exception as e:
            status_label.config(text=f"Save failed: {e}", foreground=ERROR_COLOR)


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
        graph_canvas = FigureCanvasTkAgg(fig, master=graph_frame_container)
        graph_canvas.draw()
        graph_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Maintain view control references
        global current_fig, current_zoom
        current_fig = fig
        current_zoom = 1.0
        refresh_plot_view()

        # Build details text area content
        corner_text = "\n".join([f"({round(x, 3)}, {round(y, 3)})" for x, y in sorted(corner_points)])

        # As 'point of intersection', report all corner intersection points
        intersection_text = corner_text if corner_text else "None"

        # Evaluate objective function at corner points
        objective_evals = []
        for x, y in sorted(corner_points):
            zval = p * x + q * y
            objective_evals.append(f"({round(x, 3)}, {round(y, 3)}): Z = {round(zval, 3)}")
        objective_points_text = "\n".join(objective_evals) if objective_evals else "None"

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
        objective_formula = f"Z = {p}x + {q}y ({'Maximize' if var_max.get() else 'Minimize'})"
        details_data = (
            f"Objective Function:\n{objective_formula}\n\n"
            f"Corner Points:\n{corner_text or 'None'}\n\n"
            f"Objective values at corners:\n{objective_points_text}\n\n"
            f"Optimal Point:\n({round(sol_point[0], 3)}, {round(sol_point[1], 3)})\n"
            f"Z = {round(p * sol_point[0] + q * sol_point[1], 3)}\n\n"
            f"Edge Lines (Constraints):\n{edge_text}\n\n"
            f"Binding Constraints:\n{constraints_text}\n\n"
            f"Bounded by Axes:\n{axes_text}"
        )

        details_text.config(state="normal")
        details_text.delete("1.0", "end")
        details_text.insert("end", details_data)
        adjust_text_height()   # 🔥 yeh add kar
        details_text.config(state="disabled")

        # Update result summary label
        result_summary = (
            f"Optimal Solution Found! | Point: ({round(sol_point[0], 3)}, {round(sol_point[1], 3)}) | "
            f"Z = {round(sol_val, 3)} | {objective_formula}"
        )
        result_label.config(
            text=f"✅ {result_summary}",
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

root = ctk.CTk()
root.title("LPP Graphical Method Solver")
root.configure(fg_color=BACKGROUND_COLOR)
root._set_appearance_mode("dark")
root.geometry("1200x700")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.state("zoomed")
root.bind("<Escape>", lambda e: root.state("normal"))

# Configure styles
configure_styles()

# Create canvas and scrollbar for the main window
main_canvas = tk.Canvas(
    root,
    bg=BACKGROUND_COLOR,
    highlightthickness=0,
    bd=0   # 🔥 ADD THIS
)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview, style="Vertical.TScrollbar")
def toggle_main_scrollbar(*args):
    if main_canvas.yview() == (0.0, 1.0):
        scrollbar.pack_forget()
    else:
        scrollbar.pack(side="right", fill="y")

main_canvas.configure(yscrollcommand=lambda *args: (scrollbar.set(*args), toggle_main_scrollbar()))
scrollbar.pack_forget()

main_canvas.pack(side="left", fill="both", expand=True, padx=0, pady=0)
scrollbar.pack(side="right", fill="y")

# Main container (inside canvas)
main_frame = ttk.Frame(main_canvas, style="Card.TFrame")
main_frame.pack(fill="both", expand=True)
main_canvas_window = main_canvas.create_window(0, 0, window=main_frame, anchor="nw")

# Bind mousewheel/scroll events
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def _on_linux_scroll(event):
    if event.num == 5:
        main_canvas.yview_scroll(3, "units")
    elif event.num == 4:
        main_canvas.yview_scroll(-3, "units")

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
main_canvas.bind_all("<Button-4>", _on_linux_scroll)
main_canvas.bind_all("<Button-5>", _on_linux_scroll)

# Update scroll region after frame is rendered
def _configure_scroll_region(event=None):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

main_frame.bind("<Configure>", _configure_scroll_region)
main_canvas.bind("<Configure>", lambda e: main_canvas.itemconfig(main_canvas_window, width=e.width))

# Header section
header_frame = tk.Frame(main_frame, bg=SURFACE_COLOR)
header_frame.pack(fill="x", pady=(0, 10))  # or even (0, 5)

header = ttk.Label(header_frame, text="Linear Programming Problem Solver",
                  style="Header.TLabel", anchor="center")
header.pack(pady=15)

# Content frame with border
content_frame_border, content_frame = create_bordered_container(main_frame, return_inner=True)
content_frame_border.pack(fill="both", expand=True)

# Left panel - Input
left_panel_border, left_panel = create_bordered_container(content_frame, return_inner=True)
left_panel_border.pack(side="left", fill="both", expand=True, padx=(0, 10))

# Constraint frame with border
constraints_frame_border, constraints_frame = create_bordered_container(left_panel, return_inner=True)
constraints_frame_border.pack(fill="x", pady=(0, 15), padx=15)

# Add internal padding to constraints_frame content
constraints_frame_container = tk.Frame(constraints_frame, bg=SURFACE_COLOR)
constraints_frame_container.pack(fill="both", expand=True, padx=10, pady=10)

# Use grid layout for constraints_frame
for i in range(9):
    constraints_frame_container.grid_columnconfigure(i, weight=1)

constraint_title = ttk.Label(constraints_frame_container, text="Constraints",
                            style="Subheader.TLabel")
constraint_title.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 5))

constraint_desc = ttk.Label(constraints_frame_container,
                           text="Add inequalities in the form: ax + by ≤ c",
                           font=("Segoe UI", 9), foreground="white",
                           background=SURFACE_COLOR)
constraint_desc.grid(row=1, column=0, columnspan=8, sticky="w", pady=(0, 10))

add_btn = ctk.CTkButton(
    constraints_frame_container,
    text="Add Constraint",
    fg_color="#2563eb",        # dark blue
    hover_color="#60a5fa",     # light blue on hover
    text_color="white",
    font=("Segoe UI", 14, "bold"),
    corner_radius=50,          # 🔥 rounded corners
    command=add_constraint
)
# add_btn will be positioned by refresh_layout

# Objective frame with border
objective_frame_border, objective_frame = create_bordered_container(left_panel, return_inner=True)
objective_frame_border.pack(fill="x", pady=(15, 0), padx=15)

# Add internal padding to objective_frame content
objective_frame_container = tk.Frame(objective_frame, bg=SURFACE_COLOR)
objective_frame_container.pack(fill="both", expand=True, padx=10, pady=10)

objective_title = ttk.Label(objective_frame_container, text="Objective Function",
                           style="Subheader.TLabel")
objective_title.pack(anchor="w", pady=(0, 5))

objective_desc = ttk.Label(objective_frame_container,
                          text="Maximize or minimize: Z = px + qy",
                          font=("Segoe UI", 9), foreground="white",
                          background=SURFACE_COLOR)
objective_desc.pack(anchor="w", pady=(0, 10))

obj_input_frame = ttk.Frame(objective_frame_container, style="Card.TFrame")
obj_input_frame.pack(fill="x", pady=(0, 10))

ttk.Label(obj_input_frame, text="Z =", font=LABEL_FONT,
         background=SURFACE_COLOR, foreground="white").grid(row=0, column=0, padx=(0, 5), pady=5)
entry_p = tk.Entry(
    obj_input_frame,
    width=5,
    font=DEFAULT_FONT,
    justify="center",
    bg="#1e293b",
    fg="#e2e8f0",
    insertbackground="#e2e8f0",
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground="#22d3ee",
    highlightcolor="#22d3ee"
)
entry_p.grid(row=0, column=1, padx=5, pady=5)
ttk.Label(obj_input_frame, text="x +", font=LABEL_FONT,
         background=SURFACE_COLOR, foreground="white").grid(row=0, column=2, padx=5, pady=5)
entry_q = tk.Entry(
    obj_input_frame,
    width=5,
    font=DEFAULT_FONT,
    justify="center",
    bg="#1e293b",
    fg="#e2e8f0",
    insertbackground="#e2e8f0",
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground="#22d3ee",
    highlightcolor="#22d3ee"
)
entry_q.grid(row=0, column=3, padx=5, pady=5)
ttk.Label(obj_input_frame, text="y", font=LABEL_FONT,
         background=SURFACE_COLOR, foreground="white").grid(row=0, column=4, padx=(5, 15), pady=5)

# Radio buttons
radio_frame = ttk.Frame(obj_input_frame, style="Card.TFrame")
radio_frame.grid(row=0, column=5, padx=(0, 10))

var_max = tk.BooleanVar(value=True)
max_radio = tk.Radiobutton(radio_frame, text="Maximize", variable=var_max,
                          value=True, font=DEFAULT_FONT, bg=SURFACE_COLOR, fg="white",
                          activebackground=SURFACE_COLOR, selectcolor=PRIMARY_COLOR)
min_radio = tk.Radiobutton(radio_frame, text="Minimize", variable=var_max,
                          value=False, font=DEFAULT_FONT, bg=SURFACE_COLOR, fg="white",
                          activebackground=SURFACE_COLOR, selectcolor=PRIMARY_COLOR)
max_radio.pack(side="left", padx=(0, 10))
min_radio.pack(side="left")

# Define solve button hover effects before creating the button
def _on_solve_enter(e):
    solve_btn.config(bg="#059669")

def _on_solve_leave(e):
    solve_btn.config(bg=SUCCESS_COLOR)

# Solve button
solve_btn = ctk.CTkButton(
    objective_frame_container,
    text="Solve Problem",
    fg_color="#16a34a",        # dark green
    hover_color="#4ade80",     # light green
    text_color="white",
    font=("Segoe UI", 14, "bold"),
    corner_radius=50, 
    command=run_solver
)
solve_btn.pack(pady=(10, 0))

# Details panel (NOW BELOW OBJECTIVE FUNCTION)
details_frame_border, details_frame = create_bordered_container(objective_frame_container, return_inner=True)
details_frame_border.pack(fill="both", expand=True, pady=(15, 0))

details_frame_container = tk.Frame(details_frame, bg=SURFACE_COLOR)
details_frame_container.pack(fill="both", expand=True, padx=8, pady=8)
results_heading = ttk.Label(
    details_frame_container,
    text="Results",
    style="Subheader.TLabel"
)
results_heading.pack(anchor="w", pady=(0, 8))

details_text = tk.Text(
    details_frame_container,
    height=5,   # initial
    wrap="word",
    font=("Segoe UI", 10),
    bg=SURFACE_COLOR,
    fg=TEXT_COLOR,
    bd=1,
    relief="groove"
)

details_text.pack(fill="x", expand=False)   # ❗ important
details_text.config(state="disabled")

def adjust_text_height():
    lines = int(details_text.index('end-1c').split('.')[0])
    details_text.config(height=lines)

# Right panel - Results and Graph with border
right_panel_border, right_panel = create_bordered_container(content_frame, return_inner=True)
right_panel_border.pack(side="right", fill="both", expand=True, padx=(10, 0))

results_title = ttk.Label(right_panel, text="Graphical Solution",
                         style="Subheader.TLabel")
results_title.pack(anchor="w", padx=15, pady=(15, 10))

# Graph container (embedded matplotlib) with border
graph_frame_border, graph_frame = create_bordered_container(right_panel, return_inner=True)
graph_frame_border.pack(fill="both", expand=True, padx=15, pady=(0, 10))

# Add padding to graph frame
graph_frame_container = tk.Frame(graph_frame, bg=SURFACE_COLOR, height=400)
graph_frame_container.pack(fill="both", expand=True, padx=8, pady=8)

# Toolbar for graph operations with border
view_toolbar_border, view_toolbar = create_bordered_container(right_panel, return_inner=True)
view_toolbar_border.pack(fill="x", padx=15, pady=(0, 10))

# Add padding to toolbar
view_toolbar_container = tk.Frame(view_toolbar, bg=SURFACE_COLOR)
view_toolbar_container.pack(fill="both", expand=True, padx=8, pady=8)

save_btn = create_toolbar_button(view_toolbar_container, "Save Graph", save_graph_image)
zoom_in_btn = create_toolbar_button(view_toolbar_container, "Zoom In", zoom_in)
zoom_out_btn = create_toolbar_button(view_toolbar_container, "Zoom Out", zoom_out)
reset_view_btn = create_toolbar_button(view_toolbar_container, "Reset View", reset_view)

# Placeholder for the embedded chart
graph_canvas = None



result_label = tk.Label(right_panel, text="Enter constraints and objective function,\nthen click 'Solve Problem' to see results.",
                       font=("Segoe UI", 11), bg=SURFACE_COLOR, fg=TEXT_COLOR,
                       justify="left", anchor="w", wraplength=450)
result_label.pack(padx=15, pady=(0, 10), anchor="w", fill="x")

# Status bar with border
status_frame_border, status_frame = create_bordered_container(main_frame, return_inner=True)
status_frame_border.pack(fill="x", pady=(20, 0), padx=0)

# Add padding to status frame
status_frame_container = tk.Frame(status_frame, bg=SURFACE_COLOR)
status_frame_container.pack(fill="both", expand=True, padx=10, pady=8)

status_label = ttk.Label(status_frame_container, text="Ready to solve LPP",
                        font=("Segoe UI", 9), foreground=SECONDARY_COLOR,
                        background=SURFACE_COLOR)
status_label.pack()

# Preset default constraints
add_constraint()
add_constraint()

print("LPP Graphical Method Solver starting...")
root.mainloop()