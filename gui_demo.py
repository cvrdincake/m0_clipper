#!/usr/bin/env python3
"""
Comprehensive demonstration of the M0 Clipper glassmorphism UI system.
Showcases all glassmorphism effects, animations, and cyber enhancements.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from highlighter.glassmorphism import (
    GlassmorphismTheme, 
    GlassPanel, 
    GlassButton, 
    AnimationManager,
    GlassmorphismWindow
)
from highlighter.window_effects import (
    WindowEffects, 
    ModernWindowFrame, 
    GlassmorphismNotification
)
from highlighter.cyber_effects import (
    CyberEnhancedWidget,
    CyberProgressRing,
    MatrixRain,
    HolographicScanline,
    ParticleSystem,
    create_cyber_enhanced_button
)


class GlassmorphismShowcase:
    """Comprehensive showcase of glassmorphism UI capabilities."""
    
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("M0 Clipper - Glassmorphism UI Showcase")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0A0A0A")
        
        # Initialize theme and effects
        self.theme = GlassmorphismTheme()
        self.animation_manager = AnimationManager(self.theme)
        self.window_effects = WindowEffects(self.root)
        self.notifications = GlassmorphismNotification(self.root)
        
        # Enable window effects
        self.enable_effects()
        
        # Create modern styling
        self.setup_styles()
        
        # Create the showcase interface
        self.create_showcase_ui()
        
        # Demo state
        self.demo_running = False
        
    def enable_effects(self):
        """Enable glassmorphism window effects."""
        try:
            self.window_effects.enable_blur_effect("acrylic")
            self.window_effects.set_window_transparency(0.96)
            self.window_effects.add_drop_shadow()
        except Exception as e:
            print(f"Window effects not available: {e}")
    
    def setup_styles(self):
        """Setup glassmorphism styling."""
        self.style = ttk.Style()
        self.theme.create_glass_style(self.style)
    
    def create_showcase_ui(self):
        """Create the comprehensive showcase interface."""
        # Main container
        main_container = tk.Frame(self.root, bg=self.theme.colors.deep_black)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        main_container.columnconfigure([0, 1, 2], weight=1)
        main_container.rowconfigure([0, 1, 2], weight=1)
        
        # Header showcase
        self.create_header_showcase(main_container)
        
        # Color palette showcase
        self.create_color_showcase(main_container)
        
        # Component showcase
        self.create_component_showcase(main_container)
        
        # Animation showcase
        self.create_animation_showcase(main_container)
        
        # Cyber effects showcase
        self.create_cyber_showcase(main_container)
        
        # Interactive demo panel
        self.create_demo_panel(main_container)
    
    def create_header_showcase(self, parent):
        """Create header showcase section."""
        header_panel = GlassPanel(parent, self.theme, "Glassmorphism Header Demo")
        header_panel.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        
        header_panel.content_frame.columnconfigure(0, weight=1)

        # Title with modern typography
        title_label = tk.Label(
            header_panel.content_frame,
            text="M0 Clipper Ultra-Modern Glassmorphism UI",
            bg=header_panel.content_frame.cget("bg"),
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['title']
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        subtitle_label = tk.Label(
            header_panel.content_frame,
            text="Professional Video Highlight Generator with Advanced UI Technology",
            bg=header_panel.content_frame.cget("bg"),
            fg=self.theme.colors.soft_white,
            font=self.theme.fonts['subtitle']
        )
        subtitle_label.grid(row=1, column=0)
        
        # Add cyber effects to title
        title_effects = CyberEnhancedWidget(title_label)
        title_effects.add_scanline_effect(["#FFFFFF", "#E0E0E0"])
    
    def create_color_showcase(self, parent):
        """Create color palette showcase."""
        color_panel = GlassPanel(parent, self.theme, "Color Palette")
        color_panel.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Color swatches
        colors_frame = tk.Frame(color_panel.content_frame, bg=self.theme.colors.glass_primary)
        colors_frame.pack(fill=tk.BOTH, expand=True)
        
        # Define color groups
        color_groups = [
            ("Blacks", [
                ("Pure Black", self.theme.colors.pure_black),
                ("Deep Black", self.theme.colors.deep_black),
                ("Dark Black", self.theme.colors.dark_black),
                ("Medium Black", self.theme.colors.medium_black),
                ("Light Black", self.theme.colors.light_black)
            ]),
            ("Whites", [
                ("Pure White", self.theme.colors.pure_white),
                ("Ice White", self.theme.colors.ice_white),
                ("Silver White", self.theme.colors.silver_white),
                ("Soft White", self.theme.colors.soft_white),
                ("Muted White", self.theme.colors.muted_white)
            ]),
            ("Glass", [
                ("Primary", self.theme.colors.glass_primary),
                ("Secondary", self.theme.colors.glass_secondary),
                ("Tertiary", self.theme.colors.glass_tertiary),
                ("Hover", self.theme.colors.glass_hover),
                ("Active", self.theme.colors.glass_active)
            ])
        ]
        
        for group_name, colors in color_groups:
            group_frame = tk.LabelFrame(
                colors_frame,
                text=group_name,
                bg=self.theme.colors.glass_primary,
                fg=self.theme.colors.pure_white,
                font=self.theme.fonts['heading']
            )
            group_frame.pack(fill=tk.X, pady=5)
            
            for color_name, color_value in colors:
                color_row = tk.Frame(group_frame, bg=self.theme.colors.glass_primary)
                color_row.pack(fill=tk.X, pady=2)
                
                # Color swatch
                swatch = tk.Frame(
                    color_row,
                    bg=color_value,
                    width=30,
                    height=20,
                    relief="flat",
                    bd=1,
                    highlightbackground=self.theme.colors.border_subtle,
                    highlightthickness=1
                )
                swatch.pack(side=tk.LEFT, padx=(0, 10))
                swatch.pack_propagate(False)
                
                # Color info
                info_label = tk.Label(
                    color_row,
                    text=f"{color_name}: {color_value}",
                    bg=self.theme.colors.glass_primary,
                    fg=self.theme.colors.pure_white,
                    font=self.theme.fonts['caption'],
                    anchor="w"
                )
                info_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def create_component_showcase(self, parent):
        """Create component showcase section."""
        component_panel = GlassPanel(parent, self.theme, "UI Components")
        component_panel.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # Buttons showcase
        button_frame = tk.LabelFrame(
            component_panel.content_frame,
            text="Buttons",
            bg=self.theme.colors.glass_primary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['heading']
        )
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Primary button
        primary_btn = GlassButton(
            button_frame,
            self.theme,
            "Primary Action",
            style="primary"
        )
        primary_btn.pack(pady=5)
        
        # Secondary button
        secondary_btn = GlassButton(
            button_frame,
            self.theme,
            "Secondary Action",
            style="secondary"
        )
        secondary_btn.pack(pady=5)
        
        # Input components showcase
        input_frame = tk.LabelFrame(
            component_panel.content_frame,
            text="Input Elements",
            bg=self.theme.colors.glass_primary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['heading']
        )
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Entry field
        entry_container = tk.Frame(
            input_frame,
            bg=self.theme.colors.glass_secondary,
            relief='flat',
            bd=1,
            highlightbackground=self.theme.colors.border_subtle,
            highlightthickness=1
        )
        entry_container.pack(fill=tk.X, pady=5)
        
        demo_entry = tk.Entry(
            entry_container,
            bg=self.theme.colors.glass_secondary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['body'],
            relief='flat',
            bd=0,
            insertbackground=self.theme.colors.pure_white
        )
        demo_entry.pack(fill=tk.X, padx=10, pady=8)
        demo_entry.insert(0, "Glassmorphism Text Input")
        
        # Progress indicator
        progress_frame = tk.LabelFrame(
            component_panel.content_frame,
            text="Progress Indicators",
            bg=self.theme.colors.glass_primary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['heading']
        )
        progress_frame.pack(fill=tk.X)
        
        # Cyber progress ring
        self.progress_ring = CyberProgressRing(progress_frame, 60, 6)
        self.progress_ring.pack(pady=10)
        self.progress_ring.set_indeterminate(True)
    
    def create_animation_showcase(self, parent):
        """Create animation showcase section."""
        animation_panel = GlassPanel(parent, self.theme, "Animations")
        animation_panel.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        
        # Animation controls
        controls_frame = tk.Frame(animation_panel.content_frame, bg=self.theme.colors.glass_primary)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Fade animation demo
        fade_btn = GlassButton(
            controls_frame,
            self.theme,
            "Fade Animation",
            command=self.demo_fade_animation,
            style="secondary"
        )
        fade_btn.pack(pady=2, fill=tk.X)
        
        # Slide animation demo
        slide_btn = GlassButton(
            controls_frame,
            self.theme,
            "Slide Animation",
            command=self.demo_slide_animation,
            style="secondary"
        )
        slide_btn.pack(pady=2, fill=tk.X)
        
        # Morph animation demo
        morph_btn = GlassButton(
            controls_frame,
            self.theme,
            "Color Morph",
            command=self.demo_morph_animation,
            style="secondary"
        )
        morph_btn.pack(pady=2, fill=tk.X)
        
        # Animation target
        self.animation_target = tk.Label(
            animation_panel.content_frame,
            text="Animation Target",
            bg=self.theme.colors.glass_secondary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['heading'],
            width=20,
            height=3,
            relief='flat',
            bd=1,
            highlightbackground=self.theme.colors.border_subtle,
            highlightthickness=1
        )
        self.animation_target.pack(pady=10)
    
    def create_cyber_showcase(self, parent):
        """Create cyber effects showcase section."""
        cyber_panel = GlassPanel(parent, self.theme, "Cyber Effects")
        cyber_panel.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Cyber effects controls
        effects_frame = tk.Frame(cyber_panel.content_frame, bg=self.theme.colors.glass_primary)
        effects_frame.pack(fill=tk.X, pady=(0, 10))
        effects_frame.columnconfigure([0, 1, 2], weight=1)
        
        # Scanline effect
        scanline_btn = GlassButton(
            effects_frame,
            self.theme,
            "Scanlines",
            command=self.demo_scanlines,
            style="secondary"
        )
        scanline_btn.grid(row=0, column=0, padx=5, sticky="ew")
        
        # Particle effect
        particle_btn = GlassButton(
            effects_frame,
            self.theme,
            "Particles",
            command=self.demo_particles,
            style="secondary"
        )
        particle_btn.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Glitch effect
        glitch_btn = GlassButton(
            effects_frame,
            self.theme,
            "Glitch",
            command=self.demo_glitch,
            style="secondary"
        )
        glitch_btn.grid(row=0, column=2, padx=5, sticky="ew")
        
        # Cyber demo area
        self.cyber_demo_frame = tk.Frame(
            cyber_panel.content_frame,
            bg=self.theme.colors.glass_secondary,
            relief='flat',
            bd=1,
            highlightbackground=self.theme.colors.border_subtle,
            highlightthickness=1,
            height=150
        )
        self.cyber_demo_frame.pack(fill=tk.BOTH, expand=True)
        self.cyber_demo_frame.pack_propagate(False)
        
        # Cyber demo label
        self.cyber_label = tk.Label(
            self.cyber_demo_frame,
            text="CYBER EFFECTS DEMO AREA",
            bg=self.theme.colors.glass_secondary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['title']
        )
        self.cyber_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Initialize cyber effects
        self.cyber_effects = CyberEnhancedWidget(self.cyber_demo_frame)
    
    def create_demo_panel(self, parent):
        """Create interactive demo panel."""
        demo_panel = GlassPanel(parent, self.theme, "Interactive Demo")
        demo_panel.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)
        
        # Demo controls
        controls_frame = tk.Frame(demo_panel.content_frame, bg=self.theme.colors.glass_primary)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Start demo button
        self.demo_btn = GlassButton(
            controls_frame,
            self.theme,
            "Start Full Demo",
            command=self.start_full_demo,
            style="primary"
        )
        self.demo_btn.pack(fill=tk.X, pady=5)
        
        # Notification demo
        notification_btn = GlassButton(
            controls_frame,
            self.theme,
            "Show Notification",
            command=self.demo_notification,
            style="secondary"
        )
        notification_btn.pack(fill=tk.X, pady=2)
        
        # Window effects demo
        effects_btn = GlassButton(
            controls_frame,
            self.theme,
            "Toggle Blur",
            command=self.toggle_window_blur,
            style="secondary"
        )
        effects_btn.pack(fill=tk.X, pady=2)
        
        # Demo info
        info_text = tk.Text(
            demo_panel.content_frame,
            height=8,
            wrap=tk.WORD,
            bg=self.theme.colors.glass_secondary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['caption'],
            relief='flat',
            bd=0,
            state='disabled'
        )
        info_text.pack(fill=tk.BOTH, expand=True)
        
        # Add demo information
        demo_info = '''
Glassmorphism UI Features:

• Ultra-modern black & white aesthetic
• Translucent glass panels with blur effects
• Smooth animations and transitions
• Cyber-enhanced visual effects
• Professional typography system
• Advanced window effects
• Responsive hover interactions
• Modern notification system

Explore all the interactive elements to experience the full glassmorphism aesthetic!'''
        
        info_text.configure(state='normal')
        info_text.insert('1.0', demo_info)
        info_text.configure(state='disabled')
    
    # Demo methods
    def demo_fade_animation(self):
        """Demonstrate fade animation."""
        self.animation_manager.fade_in(self.animation_target, duration=1000)
    
    def demo_slide_animation(self):
        """Demonstrate slide animation."""
        self.animation_manager.slide_in(self.animation_target, "up", duration=800)
    
    def demo_morph_animation(self):
        """Demonstrate color morphing animation."""
        import random
        colors = [self.theme.colors.glass_hover, self.theme.colors.glass_active, self.theme.colors.glass_secondary]
        target_color = random.choice(colors)
        self.animation_manager.morphing_transition(self.animation_target, target_color, duration=500)
    
    def demo_scanlines(self):
        """Demonstrate scanline effects."""
        self.cyber_effects.stop_all_effects()
        self.cyber_effects.add_scanline_effect(["#FFFFFF", "#E0E0E0", "#CCCCCC"])
    
    def demo_particles(self):
        """Demonstrate particle effects."""
        self.cyber_effects.stop_all_effects()
        self.cyber_effects.add_particle_effect()
    
    def demo_glitch(self):
        """Demonstrate glitch effects."""
        self.cyber_effects.add_glitch_effect(2.0)
    
    def demo_notification(self):
        """Demonstrate notification system."""
        import random
        notifications = [
            ("System Online", "Glassmorphism UI initialized successfully", "success"),
            ("Processing", "Analyzing video content for highlights", "info"),
            ("Warning", "Memory usage is approaching limits", "warning"),
            ("Error", "Failed to process video file", "error")
        ]
        
        title, message, type_name = random.choice(notifications)
        self.notifications.show_notification(title, message, type_name)
    
    def toggle_window_blur(self):
        """Toggle window blur effect."""
        try:
            if hasattr(self.window_effects, 'is_blur_enabled') and self.window_effects.is_blur_enabled:
                # Disable blur (simplified - would need platform-specific implementation)
                self.root.wm_attributes('-alpha', 1.0)
            else:
                # Enable blur
                self.window_effects.enable_blur_effect("acrylic")
                self.window_effects.set_window_transparency(0.96)
        except Exception as e:
            self.notifications.show_notification("Window Effects", f"Effect not available: {e}", "warning")
    
    def start_full_demo(self):
        """Start comprehensive demo sequence."""
        if self.demo_running:
            return
            
        self.demo_running = True
        self.demo_btn.configure(text="Demo Running...")
        
        # Demo sequence
        def demo_sequence():
            # Step 1: Notifications
            self.notifications.show_notification("Demo Started", "Beginning glassmorphism showcase", "info")
            
            self.root.after(1000, lambda: [
                # Step 2: Animations
                self.demo_fade_animation(),
                self.notifications.show_notification("Animations", "Demonstrating smooth transitions", "info")
            ])
            
            self.root.after(2500, lambda: [
                # Step 3: Cyber effects
                self.demo_scanlines(),
                self.notifications.show_notification("Cyber Effects", "Activating holographic scanlines", "info")
            ])
            
            self.root.after(4000, lambda: [
                # Step 4: Particles
                self.demo_particles(),
                self.notifications.show_notification("Particle System", "Engaging particle effects", "info")
            ])
            
            self.root.after(6000, lambda: [
                # Step 5: Glitch
                self.demo_glitch(),
                self.notifications.show_notification("Glitch Effect", "Applying digital distortion", "warning")
            ])
            
            self.root.after(8000, lambda: [
                # Step 6: Complete
                self.notifications.show_notification("Demo Complete", "Glassmorphism showcase finished!", "success"),
                self.reset_demo()
            ])
        
        demo_sequence()
    
    def reset_demo(self):
        """Reset demo to initial state."""
        self.demo_running = False
        self.demo_btn.configure(text="Start Full Demo")
        self.cyber_effects.stop_all_effects()
    
    def run(self):
        """Run the glassmorphism showcase."""
        self.root.mainloop()


def main():
    """Main entry point for the glassmorphism showcase."""
    print("🎨 Initializing M0 Clipper Glassmorphism Showcase...")
    print("⚡ Loading ultra-modern UI components...")
    
    showcase = GlassmorphismShowcase()
    
    print("✨ Glassmorphism UI ready! Launching showcase...")
    showcase.run()


if __name__ == "__main__":
    main()