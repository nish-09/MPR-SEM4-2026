# LPP Graphical Method Solver

A modern, user-friendly application for solving Linear Programming Problems using the graphical method.

## Features

- **Modern UI**: Clean, intuitive interface with improved styling
- **Interactive Constraints**: Easily add, edit, and remove constraints
- **Objective Function**: Support for both maximization and minimization problems
- **Visual Results**: Automatic graph plotting of feasible regions and optimal solutions
- **Error Handling**: Clear error messages and validation

## How to Use

1. **Add Constraints**: Click "➕ Add Constraint" to add inequality constraints in the form `ax + by ≤ c`
2. **Set Objective**: Enter coefficients p and q for the objective function `Z = px + qy`
3. **Choose Type**: Select whether to maximize or minimize the objective function
4. **Solve**: Click "🚀 Solve Problem" to find the optimal solution
5. **View Results**: See the optimal point, objective value, and graphical representation

## Requirements

- Python 3.x
- tkinter (usually included with Python)
- matplotlib
- numpy (for solver calculations)

## Running the Application

```bash
cd src
python main.py
```

## UI Improvements

- Modern color scheme with blue primary colors
- Card-based layout for better organization
- Icons and emojis for visual clarity
- Improved typography and spacing
- Better error messaging with status indicators
- Responsive design with proper padding and margins