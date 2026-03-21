# Main.py - Key Changes for Border Fixes

## Color Scheme Update

```python
# Add BORDER_COLOR
PRIMARY_COLOR = "#14b8a6"      
SECONDARY_COLOR = "#475569"
SUCCESS_COLOR = "#4ade80"
ERROR_COLOR = "#f87171"
BACKGROUND_COLOR = "#020617"
SURFACE_COLOR = "#0f172a"
TEXT_COLOR = "#e2e8f0"
ACCENT_COLOR = "#22d3ee"
BORDER_COLOR = "#334155"  # ✅ NEW - Clean dark theme border
```

## The Helper Function

```python
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
```

## Updated TTK Style Configuration

```python
def configure_styles():
    style = ttk.Style()

    # ... other styles ...

    # Frame styles (removed unreliable ttk borders)
    style.configure("Card.TFrame",
                   background=SURFACE_COLOR,
                   relief="flat",
                   borderwidth=0)  # ✅ No borders in TTK - let tk.Frame handle it
```

## Layout Section - Key Changes

### Content Frame
```python
# ✅ BEFORE: ttk.Frame with broken borders
# content_frame = ttk.Frame(main_frame, style="Card.TFrame")
# content_frame.pack(fill="both", expand=True)

# ✅ AFTER: Using bordered container
content_frame_border, content_frame = create_bordered_container(main_frame, return_inner=True)
content_frame_border.pack(fill="both", expand=True)
```

### Left Panel (Input Section)
```python
# ✅ Left panel with border
left_panel_border, left_panel = create_bordered_container(content_frame, return_inner=True)
left_panel_border.pack(side="left", fill="both", expand=True, padx=(0, 10))
```

### Constraints Frame
```python
# ✅ Constraint frame with proper border and padding structure
constraints_frame_border, constraints_frame = create_bordered_container(left_panel, return_inner=True)
constraints_frame_border.pack(fill="x", pady=(0, 15), padx=15)

# ✅ Add internal padding container
constraints_frame_container = tk.Frame(constraints_frame, bg=SURFACE_COLOR)
constraints_frame_container.pack(fill="both", expand=True, padx=10, pady=10)

# Now add content to constraints_frame_container
constraints_frame_container.grid_columnconfigure(0, weight=1)
# ... rest of grid config ...

constraint_title = ttk.Label(constraints_frame_container, text="Constraints", style="Subheader.TLabel")
constraint_title.grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 5))
```

### Objective Frame
```python
# ✅ Objective frame with border
objective_frame_border, objective_frame = create_bordered_container(left_panel, return_inner=True)
objective_frame_border.pack(fill="x", pady=(15, 0), padx=15)

# ✅ Add internal padding
objective_frame_container = tk.Frame(objective_frame, bg=SURFACE_COLOR)
objective_frame_container.pack(fill="both", expand=True, padx=10, pady=10)

objective_title = ttk.Label(objective_frame_container, text="Objective Function", style="Subheader.TLabel")
objective_title.pack(anchor="w", pady=(0, 5))

objective_desc = ttk.Label(objective_frame_container, text="Maximize or minimize: Z = px + qy", ...)
objective_desc.pack(anchor="w", pady=(0, 10))

# ... continue adding to objective_frame_container ...
```

### Right Panel (Results Section)
```python
# ✅ Right panel with border
right_panel_border, right_panel = create_bordered_container(content_frame, return_inner=True)
right_panel_border.pack(side="right", fill="both", expand=True, padx=(10, 0))
```

### Graph Frame
```python
# ✅ Graph frame with border
graph_frame_border, graph_frame = create_bordered_container(right_panel, return_inner=True)
graph_frame_border.pack(fill="both", expand=False, padx=15, pady=(0, 10))

# ✅ Padding container for graph
graph_frame_container = tk.Frame(graph_frame, bg=SURFACE_COLOR, height=150)
graph_frame_container.pack(fill="both", expand=True, padx=8, pady=8)
graph_frame_container.pack_propagate(False)
```

### Toolbar
```python
# ✅ Toolbar with border
view_toolbar_border, view_toolbar = create_bordered_container(right_panel, return_inner=True)
view_toolbar_border.pack(fill="x", padx=15, pady=(0, 10))

# ✅ Padding container
view_toolbar_container = tk.Frame(view_toolbar, bg=SURFACE_COLOR)
view_toolbar_container.pack(fill="both", expand=True, padx=8, pady=8)

# Add buttons to view_toolbar_container
save_btn = ttk.Button(view_toolbar_container, text="Save Graph", ...)
save_btn.pack(side="left", padx=5, pady=5)
# ... more buttons ...
```

### Details Frame
```python
# ✅ Details frame with border
details_frame_border, details_frame = create_bordered_container(right_panel, return_inner=True)
details_frame_border.pack(fill="both", expand=True, padx=15, pady=(0, 10))

# ✅ Padding container
details_frame_container = tk.Frame(details_frame, bg=SURFACE_COLOR)
details_frame_container.pack(fill="both", expand=True, padx=8, pady=8)

details_text = tk.Text(details_frame_container, height=12, ...)
details_text.pack(fill="both", expand=True)
```

### Status Bar
```python
# ✅ Status bar with border
status_frame_border, status_frame = create_bordered_container(main_frame, return_inner=True)
status_frame_border.pack(fill="x", pady=(20, 0), padx=0)

# ✅ Padding container
status_frame_container = tk.Frame(status_frame, bg=SURFACE_COLOR)
status_frame_container.pack(fill="both", expand=True, padx=10, pady=8)

status_label = ttk.Label(status_frame_container, text="Ready to solve LPP", ...)
status_label.pack()
```

## All Constraint UI Updates

Update `add_constraint()` function to use `constraints_frame_container`:

```python
def add_constraint():
    # ✅ All widgets created in constraints_frame_container
    a = tk.Entry(constraints_frame_container, width=8, font=DEFAULT_FONT, ...)
    x_label = tk.Label(constraints_frame_container, text="x", ...)
    # ... rest of widgets in constraints_frame_container ...
```

## Summary of Changes

| Component | Before | After |
|-----------|--------|-------|
| Borders | TTK relief (broken) | tk.Frame wrapper (solid) |
| Border Color | hardcoded | `BORDER_COLOR = "#334155"` |
| Visibility | Missing left/top edges | All 4 edges visible |
| Padding | ipadx/ipady | Dedicated container with padx/pady |
| Consistency | Varied | Uniform 1px border throughout |

## Result

✅ **All borders fully visible on 4 sides**  
✅ **Consistent thickness (1px) and color (#334155)**  
✅ **No cut-off or broken borders**  
✅ **Clean internal padding (8-10px)**  
✅ **Proper spacing between sections (15px)**  
✅ **Dark theme-compatible colors**
