# Tkinter Border Solution - Clean, Reliable Borders for Dark Theme UIs

## Problem
TTK frames with `relief="raised"` or `relief="solid"` have unreliable borders, especially:
- Left and top edges disappear or appear uneven
- Borders don't render consistently across platforms
- Borders look cut off due to padding/margin interactions

## Solution: Bordered Container Helper

Replace unreliable ttk borders with `tk.Frame` wrappers that create borders reliably.

### Core Pattern: Bordered Container Helper Function

```python
BORDER_COLOR = "#334155"  # Dark theme border color
SURFACE_COLOR = "#0f172a" # Surface background

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

## Usage Pattern

### Single-Element Return (Simple Case)
```python
my_frame = create_bordered_container(parent)
my_frame.pack(fill="both", expand=True, padx=15, pady=10)

# Add content to my_frame
label = tk.Label(my_frame, text="Content", bg=SURFACE_COLOR)
label.pack()
```

### Dual Return (Recommended for Layout)
```python
border_frame, inner_frame = create_bordered_container(parent, return_inner=True)
border_frame.pack(fill="both", expand=True, padx=15, pady=10)

# Add content to inner_frame
label = tk.Label(inner_frame, text="Content", bg=SURFACE_COLOR)
label.pack()
```

## Complete Implementation Pattern

```python
# Step 1: Create the bordered container (outer + inner)
section_border, section_inner = create_bordered_container(parent, return_inner=True)
section_border.pack(fill="x", padx=15, pady=(0, 15))

# Step 2: Add internal padding container (optional but recommended)
section_container = tk.Frame(section_inner, bg=SURFACE_COLOR)
section_container.pack(fill="both", expand=True, padx=10, pady=10)

# Step 3: Add content to the padding container
title = ttk.Label(section_container, text="Section Title", style="Subheader.TLabel")
title.pack(anchor="w", pady=(0, 5))

content = tk.Label(section_container, text="Your content here", bg=SURFACE_COLOR, fg=TEXT_COLOR)
content.pack(fill="x")
```

## Visual Structure

```
Outer Container (your parent)
    ├─ border_frame (tk.Frame, bg=BORDER_COLOR)
    │  └─ inner_frame (tk.Frame, bg=SURFACE_COLOR) [padx=1, pady=1]
    │     └─ section_container (tk.Frame, bg=SURFACE_COLOR) [padx=10, pady=10]
    │        └─ Your widgets (content)
```

This creates:
- 1px solid border on all 4 sides (BORDER_COLOR)
- 10px internal padding around content
- Clean separation between sections

## Key Benefits

✅ **Reliable**: Borders render on all 4 sides consistently  
✅ **Visible**: No hidden left/top edges  
✅ **Themeable**: Easy to change `BORDER_COLOR` for different themes  
✅ **Reusable**: Single function works for all containers  
✅ **Flexible**: Customize border width, colors, and padding per container  
✅ **Platform Independent**: Works identically on Windows, macOS, Linux

## Color Recommendations

### Dark Theme
- **Border Color**: `#334155` (slate-700) - subtle gray
- **Surface Color**: `#0f172a` (slate-950) - dark background
- **Accent**: `#14b8a6` (teal-500) - primary highlight

### Light Theme
- **Border Color**: `#cbd5e1` (slate-300) - light gray
- **Surface Color**: `#f8fafc` (slate-50) - light background
- **Accent**: `#0891b2` (cyan-600) - primary highlight

## Advanced: Customizing Per Container

```python
# Regular border
bordered_frame = create_bordered_container(parent, border_width=1, border_color="#334155", return_inner=True)

# Thick accent border
accent_frame = create_bordered_container(parent, border_width=2, border_color="#14b8a6", return_inner=True)

# Subtle border
subtle_frame = create_bordered_container(parent, border_width=1, border_color="#1e293b", return_inner=True)
```

## Migration: Converting from TTK Borders

### Before (Broken)
```python
constraints_frame = ttk.Frame(parent, style="Card.TFrame")
constraints_frame.pack(fill="x", ipadx=10, ipady=10)

# Issues: TTK borders unreliable, missing edges
```

### After (Fixed)
```python
constraints_frame_border, constraints_frame = create_bordered_container(parent, return_inner=True)
constraints_frame_border.pack(fill="x", padx=15)

constraints_frame_container = tk.Frame(constraints_frame, bg=SURFACE_COLOR)
constraints_frame_container.pack(fill="both", expand=True, padx=10, pady=10)

# ✅ All 4 borders visible, consistent, themeable
```

## TTK Style Update

Remove problematic `relief` and `borderwidth` from ttk styles:

```python
# ❌ OLD (unreliable)
style.configure("Card.TFrame",
                background=SURFACE_COLOR,
                relief="raised",
                borderwidth=2,
                lightcolor=ACCENT_COLOR,
                darkcolor="#0f172a")

# ✅ NEW (clean, no borders in ttk)
style.configure("Card.TFrame",
                background=SURFACE_COLOR,
                relief="flat",
                borderwidth=0)
```

Borders are now created by `create_bordered_container()`, not by TTK.

## Spacing Convention

For consistent spacing between sections:
```python
section_border.pack(fill="x", padx=15, pady=(0, 15))  # 15px side, 15px bottom gap

# Results in:
# - 15px padding on left/right (from parent container)
# - 15px gap between sections vertically
```

## Example: Section Container

```python
def create_section(parent, title, bg_color=SURFACE_COLOR):
    """
    Create a reusable section container with border and title.
    """
    border, inner = create_bordered_container(parent, bg_color=bg_color, return_inner=True)
    border.pack(fill="x", padx=15, pady=(0, 15))
    
    container = tk.Frame(inner, bg=bg_color)
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Add title
    if title:
        ttk.Label(container, text=title, style="Subheader.TLabel").pack(anchor="w", pady=(0, 10))
    
    return border, inner, container  # Return all three levels if needed

# Usage
section_title_bar, section_inner, section_content = create_section(parent, "Constraints")

# Add content to section_content
```

## Summary

The **bordered container helper** replaces unreliable TTK borders with solid tk.Frame-based borders that:
- Render consistently on all platforms
- Show all 4 edges with no cutoff
- Support easy theming with a single color variable
- Maintain clean internal padding
- Are fully reusable across your application

Use `create_bordered_container()` for all section containers, data panels, and visual groupings.
