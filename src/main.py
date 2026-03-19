import tkinter as tk
from tkinter import messagebox
from solver import solve_lpp
from plotter import plot_graph

def run_solver():
    try:
        # Read constraints
        a1 = float(entry_a1.get())
        b1 = float(entry_b1.get())
        c1 = float(entry_c1.get())
        
        a2 = float(entry_a2.get())
        b2 = float(entry_b2.get())
        c2 = float(entry_c2.get())
        
        constraints = [(a1,b1,c1), (a2,b2,c2)]
        
        # Objective function
        p = float(entry_p.get())
        q = float(entry_q.get())
        
        maximize = var_max.get()
        
        sol_point, sol_val = solve_lpp(constraints, (p,q), maximize)
        messagebox.showinfo("Optimal Solution", f"x = {sol_point[0]:.2f}, y = {sol_point[1]:.2f}\nZ = {sol_val:.2f}")
        
        plot_graph(constraints, sol_point)
        
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Tkinter window
root = tk.Tk()
root.title("Graphical Method Solver (2-variable LPP)")

# Labels & Entries
tk.Label(root, text="Constraint 1: a1*x + b1*y <= c1").grid(row=0, column=0, columnspan=2)
entry_a1 = tk.Entry(root); entry_a1.grid(row=1,column=0)
entry_b1 = tk.Entry(root); entry_b1.grid(row=1,column=1)
entry_c1 = tk.Entry(root); entry_c1.grid(row=1,column=2)

tk.Label(root, text="Constraint 2: a2*x + b2*y <= c2").grid(row=2, column=0, columnspan=2)
entry_a2 = tk.Entry(root); entry_a2.grid(row=3,column=0)
entry_b2 = tk.Entry(root); entry_b2.grid(row=3,column=1)
entry_c2 = tk.Entry(root); entry_c2.grid(row=3,column=2)

tk.Label(root, text="Objective Function: Z = p*x + q*y").grid(row=4, column=0, columnspan=2)
entry_p = tk.Entry(root); entry_p.grid(row=5,column=0)
entry_q = tk.Entry(root); entry_q.grid(row=5,column=1)

# Max/Min Option
var_max = tk.BooleanVar()
var_max.set(True)
tk.Radiobutton(root, text="Maximize", variable=var_max, value=True).grid(row=6,column=0)
tk.Radiobutton(root, text="Minimize", variable=var_max, value=False).grid(row=6,column=1)

# Solve Button
tk.Button(root, text="Solve", command=run_solver).grid(row=7, column=0, columnspan=3)

root.mainloop()