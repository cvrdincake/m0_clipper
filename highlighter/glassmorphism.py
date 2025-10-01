#!/usr/bin/env python3
"""
Ultra-modern glassmorphism theme system for M0 Clipper.
Provides sophisticated black/white aesthetic with glass effects, animations, and modern UI components.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import math
from typing import Dict, Tuple, Optional, Callable, List
from dataclasses import dataclass


@dataclass
class GlassmorphismColors:
    """Ultra-modern black and white glassmorphism color palette."""
    
    # Core blacks and whites
    pure_black: str = "#000000"
    deep_black: str = "#0A0A0A"
    dark_black: str = "#111111"
    medium_black: str = "#1A1A1A"
    light_black: str = "#2A2A2A"
    
    pure_white: str = "#FFFFFF"
    ice_white: str = "#F8F8F8"
    silver_white: str = "#F0F0F0"
    soft_white: str = "#E8E8E8"
    muted_white: str = "#D0D0D0"
    
    # Glass layers with transparency
    glass_primary: str = "#1A1A1A"     # Main glass panels
    glass_secondary: str = "#2A2A2A"   # Secondary panels
    glass_tertiary: str = "#3A3A3A"    # Accent panels
    glass_hover: str = "#4A4A4A"       # Hover states
    glass_active: str = "#5A5A5A"      # Active states
    
    # Transparency levels
    alpha_100: str = "FF"  # Completely opaque
    alpha_95: str = "F2"   # Subtle transparency
    alpha_90: str = "E6"   # Light transparency
    alpha_80: str = "CC"   # Medium transparency
    alpha_70: str = "B3"   # Glass effect
    alpha_60: str = "99"   # Strong glass
    alpha_50: str = "80"   # Semi-transparent
    alpha_40: str = "66"   # Heavy transparency
    alpha_30: str = "4D"   # Very transparent
    alpha_20: str = "33"   # Barely visible
    alpha_10: str = "1A"   # Ultra subtle
    
    # Gradients for glass effects
    glass_gradient_start: str = "#1A1A1A"
    glass_gradient_end: str = "#0F0F0F"
    
    # Borders and highlights
    border_subtle: str = "#333333"
    border_medium: str = "#444444"
    border_bright: str = "#666666"
    border_highlight: str = "#888888"
    
    # Status colors (monochrome)
    success: str = "#FFFFFF"
    warning: str = "#CCCCCC"
    error: str = "#999999"
    info: str = "#EEEEEE"
    
    # Accent colors (very subtle)
    accent_primary: str = "#F5F5F5"
    accent_secondary: str = "#E0E0E0"
    accent_tertiary: str = "#CCCCCC"


class GlassmorphismTheme:
    """Main theme controller for glassmorphism aesthetics."""
    
    def __init__(self):
        self.colors = GlassmorphismColors()
        self.animation_speed = 200  # milliseconds
        self.blur_radius = 20
        self.border_radius = 12
        self.shadow_offset = (0, 4)
        self.shadow_blur = 20
        
        # Font configuration
        self.fonts = {
            'title': ('Inter', 28, 'bold'),
            'subtitle': ('Inter', 16, 'normal'),
            'heading': ('Inter', 14, 'bold'),
            'body': ('Inter', 11, 'normal'),
            'caption': ('Inter', 9, 'normal'),
            'mono': ('JetBrains Mono', 10, 'normal'),
        }
        
        # Animation easing functions
        self.easing = {
            'ease_out': lambda t: 1 - (1 - t) ** 3,
            'ease_in': lambda t: t ** 3,
            'ease_in_out': lambda t: 3 * t ** 2 - 2 * t ** 3 if t < 0.5 else 1 - ((-2 * t + 2) ** 3) / 2,
            'elastic': lambda t: (2 ** (-10 * t)) * math.sin((t - 0.1) * (2 * math.pi) / 0.4) + 1,
        }
    
    def create_glass_style(self, style: ttk.Style) -> None:
        """Configure comprehensive glassmorphism styles for ttk widgets."""
        
        # Glass Frame Styles
        style.configure(
            'Glass.TFrame',
            background=self.colors.glass_primary,
            relief='flat',
            borderwidth=1,
            bordercolor=self.colors.border_subtle
        )
        
        style.configure(
            'GlassSecondary.TFrame',
            background=self.colors.glass_secondary,
            relief='flat',
            borderwidth=1,
            bordercolor=self.colors.border_medium
        )
        
        # Glass Button Styles
        style.configure(
            'Glass.TButton',
            background=self.colors.glass_primary,
            foreground=self.colors.pure_white,
            borderwidth=1,
            bordercolor=self.colors.border_subtle,
            relief='flat',
            font=self.fonts['body'],
            padding=(16, 8),
            focuscolor='none'
        )
        
        style.map(
            'Glass.TButton',
            background=[
                ('active', self.colors.glass_hover),
                ('pressed', self.colors.glass_active),
                ('disabled', self.colors.glass_secondary)
            ],
            bordercolor=[
                ('active', self.colors.border_medium),
                ('pressed', self.colors.border_bright),
                ('focus', self.colors.border_highlight)
            ]
        )
        
        # Primary Action Button
        style.configure(
            'GlassPrimary.TButton',
            background=self.colors.pure_white,
            foreground=self.colors.pure_black,
            borderwidth=0,
            relief='flat',
            font=self.fonts['heading'],
            padding=(20, 12),
            focuscolor='none'
        )
        
        style.map(
            'GlassPrimary.TButton',
            background=[
                ('active', self.colors.ice_white),
                ('pressed', self.colors.silver_white),
                ('disabled', self.colors.muted_white)
            ]
        )
        
        # Glass Entry Styles
        style.configure(
            'Glass.TEntry',
            fieldbackground=self.colors.glass_secondary,
            foreground=self.colors.pure_white,
            borderwidth=1,
            bordercolor=self.colors.border_subtle,
            relief='flat',
            insertcolor=self.colors.pure_white,
            font=self.fonts['body']
        )
        
        style.map(
            'Glass.TEntry',
            fieldbackground=[
                ('focus', self.colors.glass_tertiary),
                ('readonly', self.colors.glass_primary)
            ],
            bordercolor=[
                ('focus', self.colors.border_bright),
                ('invalid', self.colors.error)
            ]
        )
        
        # Glass Label Styles
        style.configure(
            'GlassTitle.TLabel',
            background=self.colors.deep_black,
            foreground=self.colors.pure_white,
            font=self.fonts['title']
        )
        
        style.configure(
            'GlassSubtitle.TLabel',
            background=self.colors.deep_black,
            foreground=self.colors.soft_white,
            font=self.fonts['subtitle']
        )
        
        style.configure(
            'GlassHeading.TLabel',
            background=self.colors.glass_primary,
            foreground=self.colors.pure_white,
            font=self.fonts['heading']
        )
        
        style.configure(
            'GlassBody.TLabel',
            background=self.colors.glass_primary,
            foreground=self.colors.ice_white,
            font=self.fonts['body']
        )
        
        style.configure(
            'GlassCaption.TLabel',
            background=self.colors.glass_primary,
            foreground=self.colors.muted_white,
            font=self.fonts['caption']
        )
        
        # Glass LabelFrame Styles
        style.configure(
            'Glass.TLabelframe',
            background=self.colors.glass_primary,
            borderwidth=1,
            bordercolor=self.colors.border_subtle,
            relief='flat'
        )
        
        style.configure(
            'Glass.TLabelframe.Label',
            background=self.colors.glass_primary,
            foreground=self.colors.pure_white,
            font=self.fonts['heading']
        )
        
        # Glass Scale Styles
        style.configure(
            'Glass.Horizontal.TScale',
            background=self.colors.glass_primary,
            troughcolor=self.colors.glass_secondary,
            borderwidth=0,
            sliderlength=20,
            sliderrelief='flat'
        )
        
        # Glass Progressbar Styles
        style.configure(
            'Glass.Horizontal.TProgressbar',
            background=self.colors.pure_white,
            troughcolor=self.colors.glass_secondary,
            borderwidth=0,
            lightcolor=self.colors.pure_white,
            darkcolor=self.colors.pure_white
        )
        
        # Glass Scrollbar Styles
        style.configure(
            'Glass.Vertical.TScrollbar',
            background=self.colors.glass_secondary,
            troughcolor=self.colors.glass_primary,
            borderwidth=0,
            arrowcolor=self.colors.pure_white,
            relief='flat'
        )


class GlassPanel(tk.Frame):
    """Advanced glass panel with blur effects and animations."""
    
    def __init__(self, parent, theme: GlassmorphismTheme, title: str = "", **kwargs):
        self.theme = theme
        self.title = title
        self.is_hovered = False
        self.is_focused = False
        
        # Initialize with glass background
        super().__init__(
            parent,
            bg=theme.colors.glass_primary,
            relief='flat',
            bd=1,
            highlightbackground=theme.colors.border_subtle,
            highlightthickness=1,
            **kwargs
        )
        
        self.setup_glass_effect()
        self.bind_hover_events()
        
    def setup_glass_effect(self):
        """Set up the glass effect appearance."""
        # Create inner container for content
        self.content_frame = tk.Frame(
            self,
            bg=self.theme.colors.glass_primary,
            relief='flat',
            bd=0
        )
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # The content_frame will now manage its children with grid
        self.content_frame.rowconfigure(1, weight=1)
        self.content_frame.columnconfigure(0, weight=1)

        # Add title if provided
        if self.title:
            self.title_label = tk.Label(
                self.content_frame,
                text=self.title,
                bg=self.theme.colors.glass_primary,
                fg=self.theme.colors.pure_white,
                font=self.theme.fonts['heading'],
                anchor='w'
            )
            self.title_label.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
    
    def bind_hover_events(self):
        """Bind hover events for glass effects."""
        def on_enter(event):
            self.is_hovered = True
            self.animate_hover(True)
            
        def on_leave(event):
            self.is_hovered = False
            self.animate_hover(False)
            
        self.bind("<Enter>", on_enter)
        self.bind("<Leave>", on_leave)
        
        # Bind to all child widgets recursively
        def bind_children(widget):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            for child in widget.winfo_children():
                bind_children(child)
        
        bind_children(self.content_frame)
    
    def animate_hover(self, hover_in: bool):
        """Animate hover state changes."""
        target_bg = self.theme.colors.glass_hover if hover_in else self.theme.colors.glass_primary
        target_border = self.theme.colors.border_medium if hover_in else self.theme.colors.border_subtle
        
        # Smooth color transition
        def transition():
            self.configure(
                bg=target_bg,
                highlightbackground=target_border
            )
            self.content_frame.configure(bg=target_bg)
            if hasattr(self, 'title_label'):
                self.title_label.configure(bg=target_bg)
        
        # Use after() for smooth transition
        self.after(50, transition)


class GlassButton(tk.Button):
    """Advanced glass button with hover animations and effects."""
    
    def __init__(self, parent, theme: GlassmorphismTheme, text: str = "", command: Callable = None, 
                 style: str = "primary", **kwargs):
        self.theme = theme
        self.style_type = style
        self.is_hovered = False
        self.is_pressed = False
        self.animation_frame = 0
        
        # Configure based on style
        if style == "primary":
            bg_color = theme.colors.pure_white
            fg_color = theme.colors.pure_black
            font = theme.fonts['heading']
        else:
            bg_color = theme.colors.glass_primary
            fg_color = theme.colors.pure_white
            font = theme.fonts['body']
        
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=fg_color,
            font=font,
            relief='flat',
            bd=0,
            pady=12,
            padx=20,
            cursor='hand2',
            **kwargs
        )
        
        self.original_bg = bg_color
        self.original_fg = fg_color
        
        self.bind_events()
        self.create_ripple_effect()
    
    def bind_events(self):
        """Bind interactive events."""
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
    
    def on_enter(self, event):
        """Handle mouse enter."""
        self.is_hovered = True
        self.animate_hover()
    
    def on_leave(self, event):
        """Handle mouse leave."""
        self.is_hovered = False
        self.animate_hover()
    
    def on_press(self, event):
        """Handle button press."""
        self.is_pressed = True
        self.animate_press()
    
    def on_release(self, event):
        """Handle button release."""
        self.is_pressed = False
        self.animate_release()
    
    def animate_hover(self):
        """Animate hover state."""
        if self.style_type == "primary":
            target_bg = self.theme.colors.ice_white if self.is_hovered else self.theme.colors.pure_white
        else:
            target_bg = self.theme.colors.glass_hover if self.is_hovered else self.theme.colors.glass_primary
        
        self.configure(bg=target_bg)
    
    def animate_press(self):
        """Animate button press."""
        if self.style_type == "primary":
            press_bg = self.theme.colors.silver_white
        else:
            press_bg = self.theme.colors.glass_active
        
        self.configure(bg=press_bg)
    
    def animate_release(self):
        """Animate button release."""
        # Return to hover state
        self.animate_hover()
    
    def create_ripple_effect(self):
        """Create ripple effect on click (placeholder for future implementation)."""
        # This would require a canvas overlay for true ripple effects
        pass


class AnimationManager:
    """Manages smooth animations for glassmorphism UI elements."""
    
    def __init__(self, theme: GlassmorphismTheme):
        self.theme = theme
        self.running_animations = {}
        
    def fade_in(self, widget: tk.Widget, duration: int = 300, callback: Optional[Callable] = None):
        """Fade in animation for widgets."""
        animation_id = id(widget)
        steps = 20
        step_duration = duration // steps
        
        def animate_step(step: int):
            if animation_id not in self.running_animations:
                return
                
            progress = step / steps
            alpha = int(255 * self.theme.easing['ease_out'](progress))
            
            # Apply alpha to widget (simplified - would need more complex implementation)
            if step < steps:
                widget.after(step_duration, lambda: animate_step(step + 1))
            else:
                del self.running_animations[animation_id]
                if callback:
                    callback()
        
        self.running_animations[animation_id] = True
        animate_step(0)
    
    def slide_in(self, widget: tk.Widget, direction: str = "up", duration: int = 400, 
                 callback: Optional[Callable] = None):
        """Slide in animation for widgets."""
        animation_id = id(widget)
        steps = 30
        step_duration = duration // steps
        
        # Store original position
        original_x = widget.winfo_x()
        original_y = widget.winfo_y()
        
        # Calculate start position based on direction
        if direction == "up":
            start_offset = 50
            widget.place(x=original_x, y=original_y + start_offset)
        elif direction == "down":
            start_offset = -50
            widget.place(x=original_x, y=original_y + start_offset)
        elif direction == "left":
            start_offset = 50
            widget.place(x=original_x + start_offset, y=original_y)
        else:  # right
            start_offset = -50
            widget.place(x=original_x + start_offset, y=original_y)
        
        def animate_step(step: int):
            if animation_id not in self.running_animations:
                return
                
            progress = step / steps
            eased_progress = self.theme.easing['ease_out'](progress)
            
            if direction in ["up", "down"]:
                current_y = original_y + start_offset * (1 - eased_progress)
                widget.place(x=original_x, y=current_y)
            else:
                current_x = original_x + start_offset * (1 - eased_progress)
                widget.place(x=current_x, y=original_y)
            
            if step < steps:
                widget.after(step_duration, lambda: animate_step(step + 1))
            else:
                widget.place(x=original_x, y=original_y)
                del self.running_animations[animation_id]
                if callback:
                    callback()
        
        self.running_animations[animation_id] = True
        animate_step(0)
    
    def morphing_transition(self, widget: tk.Widget, target_bg: str, duration: int = 200):
        """Smooth color morphing transition."""
        animation_id = f"{id(widget)}_morph"
        steps = 15
        step_duration = duration // steps
        
        # Get current background (simplified)
        current_bg = widget.cget('bg')
        
        def animate_step(step: int):
            if animation_id not in self.running_animations:
                return
                
            progress = step / steps
            eased_progress = self.theme.easing['ease_in_out'](progress)
            
            # For now, just set the target color (real implementation would interpolate)
            if step >= steps // 2:
                widget.configure(bg=target_bg)
            
            if step < steps:
                widget.after(step_duration, lambda: animate_step(step + 1))
            else:
                del self.running_animations[animation_id]
        
        self.running_animations[animation_id] = True
        animate_step(0)
    
    def stop_animation(self, widget: tk.Widget):
        """Stop any running animation for a widget."""
        animation_id = id(widget)
        if animation_id in self.running_animations:
            del self.running_animations[animation_id]


class GlassmorphismWindow:
    """Main window with glassmorphism theme and effects."""
    
    def __init__(self, title: str = "Glassmorphism App", size: Tuple[int, int] = (1000, 800)):
        self.theme = GlassmorphismTheme()
        self.animation_manager = AnimationManager(self.theme)
        
        # Create main window
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{size[0]}x{size[1]}")
        self.root.configure(bg=self.theme.colors.deep_black)
        self.root.resizable(True, True)
        
        # Configure modern styling
        self.style = ttk.Style()
        self.theme.create_glass_style(self.style)
        
        # Set minimum size
        self.root.minsize(800, 600)
        
        # Create main container
        self.main_container = tk.Frame(
            self.root,
            bg=self.theme.colors.deep_black
        )
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configure grid weights
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(0, weight=1)
        
    def create_glass_panel(self, parent, title: str = "", **kwargs) -> GlassPanel:
        """Create a new glass panel."""
        return GlassPanel(parent, self.theme, title, **kwargs)
    
    def create_glass_button(self, parent, text: str = "", command: Callable = None, 
                           style: str = "primary", **kwargs) -> GlassButton:
        """Create a new glass button."""
        return GlassButton(parent, self.theme, text, command, style, **kwargs)
    
    def add_blur_overlay(self, widget: tk.Widget, blur_strength: float = 0.7):
        """Add blur overlay effect to widget (placeholder for advanced implementation)."""
        # This would require platform-specific implementations or libraries like Pillow
        overlay = tk.Frame(
            widget,
            bg=self.theme.colors.glass_primary + self.theme.colors.alpha_30,
            relief='flat',
            bd=0
        )
        overlay.place(relwidth=1, relheight=1)
        return overlay
    
    def run(self):
        """Start the application."""
        # Add startup animation
        self.animate_startup()
        self.root.mainloop()
    
    def animate_startup(self):
        """Animate the startup sequence."""
        # Fade in main container
        self.animation_manager.fade_in(self.main_container, duration=600)


# Example usage and demo functions
def create_glassmorphism_demo():
    """Create a demonstration of the glassmorphism system."""
    
    app = GlassmorphismWindow("Glassmorphism Demo", (1200, 900))
    
    # Header panel
    header_panel = app.create_glass_panel(app.main_container, "Glassmorphism Demo")
    header_panel.grid(row=0, column=0, sticky="ew", pady=(0, 20))
    
    # Content panels
    content_frame = tk.Frame(app.main_container, bg=app.theme.colors.deep_black)
    content_frame.grid(row=1, column=0, sticky="nsew")
    content_frame.columnconfigure([0, 1], weight=1)
    content_frame.rowconfigure(0, weight=1)
    
    # Left panel
    left_panel = app.create_glass_panel(content_frame, "Controls")
    left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    
    # Right panel
    right_panel = app.create_glass_panel(content_frame, "Output")
    right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
    
    # Add some demo content
    demo_button = app.create_glass_button(
        left_panel.content_frame, 
        "Primary Action", 
        style="primary"
    )
    demo_button.pack(pady=10)
    
    secondary_button = app.create_glass_button(
        left_panel.content_frame,
        "Secondary Action",
        style="secondary"
    )
    secondary_button.pack(pady=5)
    
    return app


if __name__ == "__main__":
    demo = create_glassmorphism_demo()
    demo.run()