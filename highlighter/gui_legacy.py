#!/usr/bin/env python3
"""
DEPRECATED: Legacy monolithic GUI module.

This module has been refactored into a professional modular architecture.
The new modular GUI is located in the highlighter.gui package.

For backward compatibility, this module provides a bridge to the new architecture.
New development should use the modular components directly.
"""

import warnings
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import tempfile
import threading
from typing import Optional
from rich.console import Console
import pathlib
from highlighter import processor, analyzer

# Check for optional dependencies
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    DND_FILES = ""

# Try to import glassmorphism components for legacy compatibility
try:
    from highlighter.glassmorphism import GlassmorphismTheme, GlassPanel, GlassButton, AnimationManager
    from highlighter.window_effects import WindowEffects, GlassmorphismNotification
    from highlighter.animations import show_boot_sequence, show_glitch_effect
    GLASSMORPHISM_AVAILABLE = True
except ImportError:
    GLASSMORPHISM_AVAILABLE = False

# Import the new modular GUI system
try:
    from highlighter.gui import main as new_gui_main
    NEW_GUI_AVAILABLE = True
except ImportError as e:
    NEW_GUI_AVAILABLE = False
    import_error = e

def main():
    """
    Main entry point for the GUI application.
    
    Routes to the new modular GUI architecture if available,
    otherwise shows an error message.
    """
    if NEW_GUI_AVAILABLE:
        # Show deprecation warning
        warnings.warn(
            "The monolithic GUI module is deprecated. "
            "Please use 'from highlighter.gui import main' for the new modular architecture.",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Route to new modular GUI
        return new_gui_main()
    else:
        # Fallback error message
        print("ERROR: New modular GUI system not available.")
        print(f"Import error: {import_error}")
        print("\nThe monolithic GUI has been refactored into a modular architecture.")
        print("Please ensure all components are properly installed.")
        raise RuntimeError("Modular GUI system not available. Please check your installation.")


# Legacy class reference for backward compatibility
class ModernHighlighterGUI:
    """
    DEPRECATED: Legacy monolithic GUI class.
    
    This class has been refactored into modular components.
    Use the new highlighter.gui package for new development.
    """
    
    def __init__(self):
        warnings.warn(
            "ModernHighlighterGUI class is deprecated. "
            "Use the new modular architecture in highlighter.gui package.",
            DeprecationWarning,
            stacklevel=2
        )
        
        if NEW_GUI_AVAILABLE:
            from highlighter.gui import MainApplication
            self._app = MainApplication()
        else:
            raise ImportError("New modular GUI system not available")
    
    def run(self):
        """Run the application using the new modular architecture."""
        return self._app.run()


class LegacyModernHighlighterGUI:
    """Legacy glassmorphism GUI implementation (DEPRECATED - use modular architecture)."""
    
    def __init__(self):
        # Check if glassmorphism components are available
        if not GLASSMORPHISM_AVAILABLE:
            raise ImportError("Legacy GUI glassmorphism dependencies not available")
            
        # Initialize glassmorphism theme
        self.glass_theme = GlassmorphismTheme()
        self.colors = self.glass_theme.colors
        self.animation_manager = AnimationManager(self.glass_theme)
        self.window_effects = None
        self.notifications = None
    
        # Create main window with drag-and-drop support
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
            
        self.root.title("M0 Clipper - Professional Highlight Generator")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        self.root.configure(bg=self.colors.deep_black)
        
        # Initialize window effects
        self.window_effects = WindowEffects(self.root)
        self.notifications = GlassmorphismNotification(self.root)
        
        # Enable modern window effects
        self.enable_glassmorphism_effects()
        
        # Configure ultra-modern styling
        self.setup_glassmorphism_styles()
        
        # Variables
        self.current_video_path = tk.StringVar()
        self.output_directory = tk.StringVar(value=os.path.join(os.getcwd(), "highlights"))
        self.decibel_threshold = tk.DoubleVar(value=-10.0)
        self.clip_length = tk.IntVar(value=30)
        self.use_streaming = tk.BooleanVar(value=True)  # Default to streaming
        self.verbose_logging = tk.BooleanVar(value=False)
        
        # Animation state
        self.is_analyzing = False
        self.analysis_thread: Optional[threading.Thread] = None
        self.temp_dir = tempfile.TemporaryDirectory()
        self.rich_console = Console()  # For terminal animations
        
        # Animation state
        self.hover_states = {}
        
        self.setup_modern_ui()
        
    def enable_glassmorphism_effects(self):
        """Enable advanced glassmorphism window effects."""
        try:
            # Enable blur effect
            self.window_effects.enable_blur_effect("acrylic")
            
            # Set window transparency
            self.window_effects.set_window_transparency(0.96)
            
            # Add drop shadow
            self.window_effects.add_drop_shadow()
            
        except Exception as e:
            # Graceful fallback if effects aren't supported
            print(f"Advanced window effects not available: {e}")
    
    def setup_glassmorphism_styles(self):
        """Configure ultra-modern glassmorphism styling."""
        self.style = ttk.Style()
        
        # Apply glassmorphism theme
        self.glass_theme.create_glass_style(self.style)
        
        # Configure dark theme base
        self.style.theme_use('clam')
    
    def create_glass_panel(self, parent, title: str = "", **kwargs) -> "GlassPanel":
        """Create a new glassmorphism panel."""
        return GlassPanel(parent, self.glass_theme, title, **kwargs)
    
    def create_glass_button(self, parent, text: str = "", command=None, style: str = "primary", **kwargs) -> "GlassButton":
        """Create a new glassmorphism button."""
        return GlassButton(parent, self.glass_theme, text, command, style, **kwargs)
    
    def show_notification(self, title: str, message: str, type: str = "info"):
        """Show a glassmorphism notification."""
        if self.notifications:
            self.notifications.show_notification(title, message, type)
        
    def _show_startup_sequence(self):
        """Show futuristic startup sequence in console."""
        try:
            # Run boot sequence in background to not block GUI
            def boot_worker():
                show_boot_sequence(self.rich_console)
            
            boot_thread = threading.Thread(target=boot_worker, daemon=True)
            boot_thread.start()
        except Exception as e:
            # Graceful fallback if animations fail
            pass
    
    def _show_completion_effect(self, message: str):
        """Show completion effect in console."""
        try:
            def effect_worker():
                show_glitch_effect(message, self.rich_console, duration=1.5)
            
            effect_thread = threading.Thread(target=effect_worker, daemon=True)
            effect_thread.start()
        except Exception as e:
            # Graceful fallback if animations fail
            pass
    

        
    def setup_modern_ui(self):
        """Set up the ultra-modern glassmorphism user interface."""
        # Main container with enhanced padding and background
        main_container = tk.Frame(self.root, bg=self.colors.deep_black)
        main_container.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)
        
        # Configure grid weights for responsive design
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Enhanced header section with glassmorphism
        self.setup_glassmorphism_header(main_container)
        
        # Content area with ultra-modern glass panels
        content_frame = tk.Frame(main_container, bg=self.colors.deep_black)
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(24, 0))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(2, weight=1)
        
        # Video input panel with enhanced glassmorphism
        self.setup_glassmorphism_video_input(content_frame)
        
        # Settings panel with modern styling
        self.setup_glassmorphism_settings(content_frame)
        
        # Progress panel with advanced animations
        self.setup_glassmorphism_progress(content_frame)
        
        # Control panel with ultra-modern buttons
        self.setup_glassmorphism_controls(content_frame)
        
    def setup_glassmorphism_header(self, parent):
        """Set up the ultra-modern glassmorphism header section."""
        # Create glass header panel
        header_panel = self.create_glass_panel(parent)
        header_panel.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 16))
        header_panel.content_frame.columnconfigure(1, weight=1)
        
        # App icon with modern design
        icon_frame = tk.Frame(
            header_panel.content_frame, 
            bg=self.colors.glass_primary,
            width=64, 
            height=64
        )
        icon_frame.grid(row=0, column=0, padx=(0, 20), sticky=tk.W)
        icon_frame.grid_propagate(False)
        
        # Enhanced icon with glassmorphism effect
        icon_container = tk.Frame(
            icon_frame,
            bg=self.colors.glass_secondary,
            relief='flat',
            bd=1,
            highlightbackground=self.colors.border_subtle,
            highlightthickness=1
        )
        icon_container.place(relwidth=1, relheight=1)
        
        icon_label = tk.Label(
            icon_container, 
            text="🎬", 
            bg=self.colors.glass_secondary,
            fg=self.colors.pure_white,
            font=('Inter', 28)
        )
        icon_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title and subtitle with modern typography
        title_frame = tk.Frame(header_panel.content_frame, bg=self.colors.glass_primary)
        title_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        title_label = tk.Label(
            title_frame, 
            text="M0 Clipper", 
            bg=self.colors.glass_primary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['title'],
            anchor='w'
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = tk.Label(
            title_frame, 
            text="Professional Highlight Generator v3.0", 
            bg=self.colors.glass_primary,
            fg=self.colors.soft_white,
            font=self.glass_theme.fonts['subtitle'],
            anchor='w'
        )
        subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(4, 0))
        
        # Status indicator with glassmorphism effect
        status_frame = tk.Frame(
            header_panel.content_frame,
            bg=self.colors.glass_primary,
            width=120,
            height=40
        )
        status_frame.grid(row=0, column=2, padx=(20, 0))
        status_frame.grid_propagate(False)
        
        status_container = tk.Frame(
            status_frame,
            bg=self.colors.glass_secondary,
            relief='flat',
            bd=1,
            highlightbackground=self.colors.border_subtle,
            highlightthickness=1
        )
        status_container.place(relwidth=1, relheight=1)
        
        # Status text and indicator
        status_content = tk.Frame(status_container, bg=self.colors.glass_secondary)
        status_content.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.status_indicator = tk.Label(
            status_content,
            text="●",
            bg=self.colors.glass_secondary,
            fg=self.colors.success,
            font=('Inter', 12, 'bold')
        )
        self.status_indicator.pack(side=tk.LEFT, padx=(8, 4))
        
        self.status_text = tk.Label(
            status_content,
            text="Ready",
            bg=self.colors.glass_secondary,
            fg=self.colors.pure_white,
            font=('Inter', 10, 'bold')
        )
        self.status_text.pack(side=tk.LEFT, padx=(0, 8))
        
    def setup_glassmorphism_video_input(self, parent):
        """Set up the ultra-modern video input panel with glassmorphism."""
        # Create main glass panel
        panel = self.create_glass_panel(parent, "Video Input")
        panel.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 16))
        
        # Enhanced drag and drop area
        if DND_AVAILABLE:
            self.drop_area = self.create_glassmorphism_drop_area(panel.content_frame)
            self.drop_area.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 16))
        else:
            self.drop_area = self.create_glassmorphism_fallback_area(panel.content_frame)
            self.drop_area.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 16))
        
        # File path display with glassmorphism styling
        path_frame = tk.Frame(panel.content_frame, bg=self.colors.glass_primary)
        path_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 12))
        path_frame.columnconfigure(1, weight=1)
        
        path_label = tk.Label(
            path_frame, 
            text="Selected File:", 
            bg=self.colors.glass_primary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['body']
        )
        path_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 12))
        
        # Enhanced file entry with glassmorphism
        entry_container = tk.Frame(
            path_frame,
            bg=self.colors.glass_secondary,
            relief='flat',
            bd=1,
            highlightbackground=self.colors.border_subtle,
            highlightthickness=1
        )
        entry_container.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 12))
        
        self.file_entry = tk.Entry(
            entry_container,
            textvariable=self.current_video_path,
            state='readonly',
            bg=self.colors.glass_secondary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['body'],
            relief='flat',
            bd=0,
            insertbackground=self.colors.pure_white
        )
        self.file_entry.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        
        # Modern browse button
        browse_btn = self.create_glass_button(
            path_frame,
            "Browse Files",
            command=self.browse_video_file,
            style="secondary"
        )
        browse_btn.grid(row=0, column=2)
        
    def create_glassmorphism_drop_area(self, parent):
        """Create ultra-modern drag and drop area with glassmorphism styling."""
        drop_container = tk.Frame(parent, bg=self.colors.glass_primary)
        
        # Enhanced drop area with glassmorphism effect
        self.drop_frame = tk.Frame(
            drop_container,
            bg=self.colors.glass_secondary,
            relief='flat',
            bd=2,
            highlightbackground=self.colors.border_subtle,
            highlightthickness=1,
            height=140
        )
        self.drop_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.drop_frame.pack_propagate(False)
        
        # Content with enhanced glassmorphism styling
        content_frame = tk.Frame(self.drop_frame, bg=self.colors.glass_secondary)
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Enhanced drop icon with glassmorphism background
        icon_container = tk.Frame(
            content_frame,
            bg=self.colors.glass_tertiary,
            width=60,
            height=60,
            relief='flat',
            bd=1,
            highlightbackground=self.colors.border_medium,
            highlightthickness=1
        )
        icon_container.pack(pady=(0, 12))
        icon_container.pack_propagate(False)
        
        drop_icon = tk.Label(
            icon_container,
            text="⬇️",
            bg=self.colors.glass_tertiary,
            fg=self.colors.pure_white,
            font=('Inter', 24)
        )
        drop_icon.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Enhanced text styling
        drop_label = tk.Label(
            content_frame,
            text="Drop video file here or click to browse",
            bg=self.colors.glass_secondary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['heading']
        )
        drop_label.pack(pady=(0, 8))
        
        # Supported formats with modern typography
        formats_label = tk.Label(
            content_frame,
            text="Supports: MP4, AVI, MOV, MKV, WebM, and more",
            bg=self.colors.glass_secondary,
            fg=self.colors.muted_white,
            font=self.glass_theme.fonts['caption']
        )
        formats_label.pack()
        
        # Register drag and drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_file_drop)
        
        # Click to browse functionality
        self.drop_frame.bind("<Button-1>", lambda e: self.browse_video_file())
        for widget in [content_frame, icon_container, drop_icon, drop_label, formats_label]:
            widget.bind("<Button-1>", lambda e: self.browse_video_file())
        
        # Enhanced hover effects with glassmorphism
        self.setup_glassmorphism_hover_effects()
        
        return drop_container
    
    def create_glassmorphism_fallback_area(self, parent):
        """Create fallback area when drag-and-drop is not available."""
        fallback_container = tk.Frame(parent, bg=self.colors.glass_primary)
        
        fallback_frame = tk.Frame(
            fallback_container,
            bg=self.colors.glass_secondary,
            relief='flat',
            bd=2,
            highlightbackground=self.colors.border_subtle,
            highlightthickness=1,
            height=140
        )
        fallback_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        fallback_frame.pack_propagate(False)
        
        content_frame = tk.Frame(fallback_frame, bg=self.colors.glass_secondary)
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Browse icon with glassmorphism
        icon_container = tk.Frame(
            content_frame,
            bg=self.colors.glass_tertiary,
            width=60,
            height=60,
            relief='flat',
            bd=1,
            highlightbackground=self.colors.border_medium,
            highlightthickness=1
        )
        icon_container.pack(pady=(0, 12))
        icon_container.pack_propagate(False)
        
        browse_icon = tk.Label(
            icon_container,
            text="📁",
            bg=self.colors.glass_tertiary,
            fg=self.colors.pure_white,
            font=('Inter', 24)
        )
        browse_icon.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        browse_label = tk.Label(
            content_frame,
            text="Click here to browse for video files",
            bg=self.colors.glass_secondary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['heading']
        )
        browse_label.pack(pady=(0, 8))
        
        # Click handler
        fallback_frame.bind("<Button-1>", lambda e: self.browse_video_file())
        for widget in [content_frame, icon_container, browse_icon, browse_label]:
            widget.bind("<Button-1>", lambda e: self.browse_video_file())
            
        return fallback_container
    
    def setup_glassmorphism_hover_effects(self):
        """Set up enhanced hover effects for the drop area."""
        def on_enter(event):
            self.drop_frame.configure(
                bg=self.colors.glass_hover,
                highlightbackground=self.colors.border_medium
            )
            # Animate with glassmorphism effect
            self.animation_manager.morphing_transition(
                self.drop_frame, 
                self.colors.glass_hover,
                duration=150
            )
            
        def on_leave(event):
            self.drop_frame.configure(
                bg=self.colors.glass_secondary,
                highlightbackground=self.colors.border_subtle
            )
            # Animate back to normal
            self.animation_manager.morphing_transition(
                self.drop_frame, 
                self.colors.glass_secondary,
                duration=150
            )
            
        self.drop_frame.bind("<Enter>", on_enter)
        self.drop_frame.bind("<Leave>", on_leave)
    
    def setup_glassmorphism_settings(self, parent):
        """Set up the ultra-modern settings panel with glassmorphism."""
        panel = self.create_glass_panel(parent, "Analysis Settings")
        panel.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 16))
        panel.content_frame.columnconfigure(1, weight=1)
        
        current_row = 0
        
        # Output directory with enhanced styling
        output_label = tk.Label(
            panel.content_frame, 
            text="Output Directory:", 
            bg=self.colors.glass_primary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['body']
        )
        output_label.grid(row=current_row, column=0, sticky=tk.W, pady=(0, 12))
        
        output_frame = tk.Frame(panel.content_frame, bg=self.colors.glass_primary)
        output_frame.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=(16, 0), pady=(0, 12))
        output_frame.columnconfigure(0, weight=1)
        
        # Enhanced output entry with glassmorphism
        output_container = tk.Frame(
            output_frame,
            bg=self.colors.glass_secondary,
            relief='flat',
            bd=1,
            highlightbackground=self.colors.border_subtle,
            highlightthickness=1
        )
        output_container.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 12))
        
        self.output_entry = tk.Entry(
            output_container,
            textvariable=self.output_directory,
            bg=self.colors.glass_secondary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['body'],
            relief='flat',
            bd=0,
            insertbackground=self.colors.pure_white
        )
        self.output_entry.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        
        output_browse_btn = self.create_glass_button(
            output_frame,
            "Browse",
            command=self.browse_output_directory,
            style="secondary"
        )
        output_browse_btn.grid(row=0, column=1)
        
        current_row += 1
        
        # Enhanced threshold settings
        threshold_label = tk.Label(
            panel.content_frame, 
            text="Detection Threshold:", 
            bg=self.colors.glass_primary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['body']
        )
        threshold_label.grid(row=current_row, column=0, sticky=tk.W, pady=(12, 0))
        
        threshold_container = tk.Frame(panel.content_frame, bg=self.colors.glass_primary)
        threshold_container.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=(16, 0), pady=(12, 0))
        threshold_container.columnconfigure(0, weight=1)
        
        # Modern threshold scale with glassmorphism
        threshold_frame = tk.Frame(threshold_container, bg=self.colors.glass_primary)
        threshold_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        threshold_frame.columnconfigure(0, weight=1)
        
        # Custom scale with glassmorphism styling
        scale_container = tk.Frame(
            threshold_frame,
            bg=self.colors.glass_secondary,
            relief='flat',
            bd=1,
            highlightbackground=self.colors.border_subtle,
            highlightthickness=1,
            height=40
        )
        scale_container.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 12))
        scale_container.grid_propagate(False)
        
        threshold_scale = tk.Scale(
            threshold_frame,
            from_=-20.0,
            to=10.0,
            variable=self.decibel_threshold,
            orient=tk.HORIZONTAL,
            bg=self.colors.glass_secondary,
            fg=self.colors.pure_white,
            highlightthickness=0,
            relief='flat',
            font=self.glass_theme.fonts['caption'],
            showvalue=0
        )
        threshold_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 12))
        
        self.threshold_label = tk.Label(
            threshold_frame,
            text=f"{self.decibel_threshold.get():.1f} dB",
            bg=self.colors.glass_primary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['heading']
        )
        self.threshold_label.grid(row=0, column=1)
        
        # Update label when scale changes
        threshold_scale.configure(
            command=lambda val: self.threshold_label.configure(
                text=f"{float(val):.1f} dB"
            )
        )
        
        # Enhanced description
        threshold_desc = tk.Label(
            threshold_container,
            text="Higher values = fewer clips, Lower values = more clips",
            bg=self.colors.glass_primary,
            fg=self.colors.muted_white,
            font=self.glass_theme.fonts['caption']
        )
        threshold_desc.grid(row=1, column=0, sticky=tk.W)
        
        current_row += 1
        
        # Enhanced clip length setting
        clip_label = tk.Label(
            panel.content_frame, 
            text="Clip Duration:", 
            bg=self.colors.glass_primary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['body']
        )
        clip_label.grid(row=current_row, column=0, sticky=tk.W, pady=(16, 0))
        
        clip_container = tk.Frame(panel.content_frame, bg=self.colors.glass_primary)
        clip_container.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=(16, 0), pady=(16, 0))
        
        clip_frame = tk.Frame(clip_container, bg=self.colors.glass_primary)
        clip_frame.grid(row=0, column=0, sticky=tk.W)
        
        # Enhanced spinbox with glassmorphism
        spinbox_container = tk.Frame(
            clip_frame,
            bg=self.colors.glass_secondary,
            relief='flat',
            bd=1,
            highlightbackground=self.colors.border_subtle,
            highlightthickness=1
        )
        spinbox_container.grid(row=0, column=0, padx=(0, 12))
        
        clip_spin = tk.Spinbox(
            spinbox_container,
            from_=10,
            to=120,
            width=8,
            textvariable=self.clip_length,
            bg=self.colors.glass_secondary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['body'],
            relief='flat',
            bd=0,
            insertbackground=self.colors.pure_white,
            buttonbackground=self.colors.glass_tertiary,
            highlightthickness=0
        )
        clip_spin.pack(padx=8, pady=8)
        
        clip_unit_label = tk.Label(
            clip_frame,
            text="seconds (centered on highlight)",
            bg=self.colors.glass_primary,
            fg=self.colors.muted_white,
            font=self.glass_theme.fonts['body']
        )
        clip_unit_label.grid(row=0, column=1)
        
        current_row += 1
        
        # Enhanced advanced options
        advanced_frame = tk.Frame(panel.content_frame, bg=self.colors.glass_primary)
        advanced_frame.grid(row=current_row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        # Custom checkboxes with glassmorphism
        self.create_glassmorphism_checkbox(
            advanced_frame,
            "Enable verbose logging",
            self.verbose_logging,
            row=0
        )
        
        self.create_glassmorphism_checkbox(
            advanced_frame,
            "Use streaming processing (memory efficient)",
            self.use_streaming,
            row=1
        )
    
    def create_glassmorphism_checkbox(self, parent, text: str, variable: "tk.BooleanVar", row: int):
        """Create a custom glassmorphism checkbox."""
        checkbox_frame = tk.Frame(parent, bg=self.colors.glass_primary)
        checkbox_frame.grid(row=row, column=0, sticky=tk.W, pady=(8, 0))
        
        # Custom checkbox using a button
        checkbox_button = tk.Button(
            checkbox_frame,
            text="☐",
            bg=self.colors.glass_secondary,
            fg=self.colors.pure_white,
            font=('Inter', 12),
            relief='flat',
            bd=1,
            width=2,
            height=1,
            command=lambda: self.toggle_checkbox(checkbox_button, variable),
            cursor='hand2',
            highlightbackground=self.colors.border_subtle,
            highlightthickness=1
        )
        checkbox_button.pack(side=tk.LEFT, padx=(0, 12))
        
        # Checkbox label
        checkbox_label = tk.Label(
            checkbox_frame,
            text=text,
            bg=self.colors.glass_primary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['body'],
            cursor='hand2'
        )
        checkbox_label.pack(side=tk.LEFT)
        checkbox_label.bind("<Button-1>", lambda e: self.toggle_checkbox(checkbox_button, variable))
        
        # Set initial state
        self.update_checkbox_appearance(checkbox_button, variable.get())
        
        # Store reference for updates
        variable.trace_add('write', lambda *args: self.update_checkbox_appearance(checkbox_button, variable.get()))
    
    def toggle_checkbox(self, button: tk.Button, variable: tk.BooleanVar):
        """Toggle checkbox state."""
        variable.set(not variable.get())
    
    def update_checkbox_appearance(self, button: tk.Button, checked: bool):
        """Update checkbox visual appearance."""
        if checked:
            button.configure(
                text="☑",
                bg=self.colors.pure_white,
                fg=self.colors.pure_black
            )
        else:
            button.configure(
                text="☐",
                bg=self.colors.glass_secondary,
                fg=self.colors.pure_white
            )
        
    def setup_glassmorphism_progress(self, parent):
        """Set up the ultra-modern progress panel with glassmorphism."""
        panel = self.create_glass_panel(parent, "Progress & Results")
        panel.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 16))
        panel.content_frame.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)
        
        # Enhanced progress bar with glassmorphism
        progress_frame = tk.Frame(panel.content_frame, bg=self.colors.glass_primary)
        progress_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 16))
        progress_frame.columnconfigure(0, weight=1)
        
        progress_label = tk.Label(
            progress_frame,
            text="Status:",
            bg=self.colors.glass_primary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['body']
        )
        progress_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 8))
        
        # Custom progress bar with glassmorphism styling
        progress_container = tk.Frame(
            progress_frame,
            bg=self.colors.glass_secondary,
            relief='flat',
            bd=1,
            highlightbackground=self.colors.border_subtle,
            highlightthickness=1,
            height=8
        )
        progress_container.grid(row=1, column=0, sticky=(tk.W, tk.E))
        progress_container.grid_propagate(False)
        
        self.progress_bar = ttk.Progressbar(
            progress_container,
            mode='indeterminate',
            style='Glass.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Enhanced status text area with glassmorphism
        text_frame = tk.Frame(panel.content_frame, bg=self.colors.glass_primary)
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(16, 0))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Glass text container
        text_container = tk.Frame(
            text_frame,
            bg=self.colors.glass_secondary,
            relief='flat',
            bd=1,
            highlightbackground=self.colors.border_subtle,
            highlightthickness=1
        )
        text_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=2, pady=2)
        text_container.columnconfigure(0, weight=1)
        text_container.rowconfigure(0, weight=1)
        
        # Enhanced text widget with glassmorphism styling
        self.status_text = tk.Text(
            text_container,
            height=8,
            wrap=tk.WORD,
            state='disabled',
            bg=self.colors.glass_secondary,
            fg=self.colors.pure_white,
            font=self.glass_theme.fonts['mono'],
            relief='flat',
            bd=0,
            insertbackground=self.colors.pure_white,
            selectbackground=self.colors.glass_hover,
            selectforeground=self.colors.pure_white
        )
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=12, pady=12)
        
        # Modern scrollbar with glassmorphism
        scrollbar_container = tk.Frame(
            text_container,
            bg=self.colors.glass_tertiary,
            width=12
        )
        scrollbar_container.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_container.grid_propagate(False)
        
        scrollbar = ttk.Scrollbar(
            scrollbar_container,
            orient=tk.VERTICAL,
            command=self.status_text.yview,
            style='Glass.Vertical.TScrollbar'
        )
        scrollbar.pack(fill=tk.Y, expand=True, padx=2, pady=2)
        self.status_text.configure(yscrollcommand=scrollbar.set)
    
    def setup_glassmorphism_controls(self, parent):
        """Set up the ultra-modern control panel with glassmorphism."""
        panel = tk.Frame(parent, bg=self.colors.deep_black)
        panel.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 0))
        
        # Enhanced button container with glassmorphism background
        button_container = tk.Frame(
            panel,
            bg=self.colors.glass_primary,
            relief='flat',
            bd=1,
            highlightbackground=self.colors.border_subtle,
            highlightthickness=1
        )
        button_container.pack(expand=True, padx=2, pady=2)
        
        # Button content frame
        button_content = tk.Frame(button_container, bg=self.colors.glass_primary)
        button_content.pack(expand=True, padx=20, pady=16)
        
        # Enhanced reference analysis button
        self.reference_btn = self.create_glass_button(
            button_content,
            "📊 Analyze Reference",
            command=self.analyze_reference,
            style="secondary"
        )
        self.reference_btn.pack(side=tk.LEFT, padx=(0, 16))
        
        # Enhanced main action button
        self.analyze_btn = self.create_glass_button(
            button_content,
            "🎬 Generate Highlights",
            command=self.start_analysis,
            style="primary"
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 16))
        
        # Enhanced open folder button
        self.open_folder_btn = self.create_glass_button(
            button_content,
            "📁 Open Output",
            command=self.open_output_folder,
            style="secondary"
        )
        self.open_folder_btn.pack(side=tk.LEFT)
        
        # Add advanced button animations
        self.setup_glassmorphism_button_animations()
    
    def setup_glassmorphism_button_animations(self):
        """Set up enhanced glassmorphism animations for buttons."""
        def create_advanced_hover_effect(button, style_type):
            def on_enter(event):
                if style_type == "primary":
                    self.animation_manager.morphing_transition(
                        button, 
                        self.colors.ice_white,
                        duration=100
                    )
                else:
                    self.animation_manager.morphing_transition(
                        button, 
                        self.colors.glass_hover,
                        duration=100
                    )
                    
            def on_leave(event):
                if style_type == "primary":
                    self.animation_manager.morphing_transition(
                        button, 
                        self.colors.pure_white,
                        duration=100
                    )
                else:
                    self.animation_manager.morphing_transition(
                        button, 
                        self.colors.glass_primary,
                        duration=100
                    )
                    
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
        
        # Apply enhanced hover effects
        create_advanced_hover_effect(self.reference_btn, "secondary")
        create_advanced_hover_effect(self.open_folder_btn, "secondary")
        create_advanced_hover_effect(self.analyze_btn, "primary")
        
    def create_modern_drop_area(self, parent):
        """Create modern drag and drop area with glassmorphism styling."""
        drop_container = tk.Frame(parent, bg=self.colors.glass_primary)
        
        # Main drop area
        self.drop_frame = tk.Frame(
            drop_container,
            bg=self.colors.glass_secondary,
            relief='flat',
            borderwidth=2,
            height=120
        )
        self.drop_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.drop_frame.pack_propagate(False)
        
        # Drop content
        content_frame = tk.Frame(self.drop_frame, bg=self.colors.glass_secondary)
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Drop icon
        drop_icon = tk.Label(
            content_frame,
            text="⬇",
            bg=self.colors.glass_secondary,
            fg=self.colors.muted_white,
            font=('Segoe UI', 24)
        )
        drop_icon.pack()
        
        # Drop text
        drop_label = tk.Label(
            content_frame,
            text="Drop video file here or click to browse",
            bg=self.colors.glass_secondary,
            fg=self.colors.soft_white,
            font=('Segoe UI', 11)
        )
        drop_label.pack(pady=(5, 0))
        
        # Supported formats
        formats_label = tk.Label(
            content_frame,
            text="Supports: MP4, AVI, MOV, MKV, and more",
            bg=self.colors.glass_secondary,
            fg=self.colors.muted_white,
            font=('Segoe UI', 9)
        )
        formats_label.pack(pady=(3, 0))
        
        # Register drag and drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.on_file_drop)
        
        # Click to browse
        self.drop_frame.bind("<Button-1>", lambda e: self.browse_video_file())
        for widget in [content_frame, drop_icon, drop_label, formats_label]:
            widget.bind("<Button-1>", lambda e: self.browse_video_file())
        
        # Hover effects
        self.setup_drop_hover_effects()
        
        return drop_container
        
    def create_fallback_area(self, parent):
        """Create fallback area when drag-and-drop is not available."""
        fallback_container = tk.Frame(parent, bg=self.colors.glass_primary)
        
        fallback_frame = tk.Frame(
            fallback_container,
            bg=self.colors.glass_secondary,
            relief='flat',
            borderwidth=2,
            height=120
        )
        fallback_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        fallback_frame.pack_propagate(False)
        
        content_frame = tk.Frame(fallback_frame, bg=self.colors.glass_secondary)
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        browse_icon = tk.Label(
            content_frame,
            text="📁",
            bg=self.colors.glass_secondary,
            fg=self.colors.muted_white,
            font=('Segoe UI', 24)
        )
        browse_icon.pack()
        
        browse_label = tk.Label(
            content_frame,
            text="Click here to browse for video files",
            bg=self.colors.glass_secondary,
            fg=self.colors.soft_white,
            font=('Segoe UI', 11)
        )
        browse_label.pack(pady=(5, 0))
        
        # Click handler
        fallback_frame.bind("<Button-1>", lambda e: self.browse_video_file())
        for widget in [content_frame, browse_icon, browse_label]:
            widget.bind("<Button-1>", lambda e: self.browse_video_file())
            
        return fallback_container
        
    def setup_drop_hover_effects(self):
        """Set up hover effects for the drop area."""
        def on_enter(event):
            self.drop_frame.configure(bg=self.colors.glass_hover)
            
        def on_leave(event):
            self.drop_frame.configure(bg=self.colors.glass_secondary)
            
        self.drop_frame.bind("<Enter>", on_enter)
        self.drop_frame.bind("<Leave>", on_leave)
        
    def setup_settings_panel(self, parent):
        """Set up the modern settings panel."""
        panel = self.create_glass_panel(parent, "Analysis Settings")
        panel.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        panel.columnconfigure(1, weight=1)
        
        current_row = 0
        
        # Output directory
        ttk.Label(
            panel, 
            text="Output Directory:", 
            style='Glass.TLabel'
        ).grid(row=current_row, column=0, sticky=tk.W, pady=(0, 10))
        
        output_frame = tk.Frame(panel, bg=self.colors.glass_primary)
        output_frame.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(0, 10))
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(
            output_frame, 
            textvariable=self.output_directory,
            style='Modern.TEntry',
            font=('Segoe UI', 10)
        )
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        output_browse_btn = ttk.Button(
            output_frame,
            text="Browse",
            command=self.browse_output_directory,
            style='Modern.TButton'
        )
        output_browse_btn.grid(row=0, column=1)
        
        current_row += 1
        
        # Decibel threshold with modern styling
        ttk.Label(
            panel, 
            text="Detection Threshold:", 
            style='Glass.TLabel'
        ).grid(row=current_row, column=0, sticky=tk.W, pady=(10, 0))
        
        threshold_container = tk.Frame(panel, bg=self.colors.glass_primary)
        threshold_container.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(10, 0))
        threshold_container.columnconfigure(0, weight=1)
        
        # Threshold scale
        threshold_frame = tk.Frame(threshold_container, bg=self.colors.glass_primary)
        threshold_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        threshold_frame.columnconfigure(0, weight=1)
        
        threshold_scale = ttk.Scale(
            threshold_frame,
            from_=-20.0,
            to=10.0,
            variable=self.decibel_threshold,
            orient=tk.HORIZONTAL,
            style='Modern.Horizontal.TScale'
        )
        threshold_scale.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.threshold_label = ttk.Label(
            threshold_frame,
            text=f"{self.decibel_threshold.get():.1f} dB",
            style='Glass.TLabel',
            font=('Segoe UI', 10, 'bold')
        )
        self.threshold_label.grid(row=0, column=1)
        
        # Update label when scale changes
        threshold_scale.configure(
            command=lambda val: self.threshold_label.configure(
                text=f"{float(val):.1f} dB"
            )
        )
        
        # Threshold description
        threshold_desc = ttk.Label(
            threshold_container,
            text="Higher values = fewer clips, Lower values = more clips",
            style='GlassSecondary.TLabel'
        )
        threshold_desc.grid(row=1, column=0, sticky=tk.W)
        
        current_row += 1
        
        # Clip length setting
        ttk.Label(
            panel, 
            text="Clip Duration:", 
            style='Glass.TLabel'
        ).grid(row=current_row, column=0, sticky=tk.W, pady=(15, 0))
        
        clip_container = tk.Frame(panel, bg=self.colors.glass_primary)
        clip_container.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(15, 0))
        
        clip_frame = tk.Frame(clip_container, bg=self.colors.glass_primary)
        clip_frame.grid(row=0, column=0, sticky=tk.W)
        
        clip_spin = ttk.Spinbox(
            clip_frame,
            from_=10,
            to=120,
            width=8,
            textvariable=self.clip_length,
            font=('Segoe UI', 10)
        )
        clip_spin.grid(row=0, column=0)
        
        ttk.Label(
            clip_frame,
            text="seconds (centered on highlight)",
            style='Glass.TLabel'
        ).grid(row=0, column=1, padx=(10, 0))
        
        current_row += 1
        
        # Advanced options
        advanced_frame = tk.Frame(panel, bg=self.colors.glass_primary)
        advanced_frame.grid(row=current_row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        verbose_check = ttk.Checkbutton(
            advanced_frame,
            text="Enable verbose logging",
            variable=self.verbose_logging
        )
        verbose_check.grid(row=0, column=0, sticky=tk.W)
        
        streaming_check = ttk.Checkbutton(
            advanced_frame,
            text="Use streaming processing (memory efficient)",
            variable=self.use_streaming
        )
        streaming_check.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
    def setup_progress_panel(self, parent):
        """Set up the modern progress panel."""
        panel = self.create_glass_panel(parent, "Progress & Results")
        panel.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        panel.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)
        
        # Progress bar
        progress_frame = tk.Frame(panel, bg=self.colors.glass_primary)
        progress_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)
        
        ttk.Label(
            progress_frame,
            text="Status:",
            style='Glass.TLabel'
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            style='Modern.Horizontal.TProgressbar'
        )
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Status text area with modern styling
        text_frame = tk.Frame(panel, bg=self.colors.glass_primary)
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(15, 0))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Custom text widget with dark styling
        self.status_text = tk.Text(
            text_frame,
            height=8,
            wrap=tk.WORD,
            state='disabled',
            bg=self.colors.glass_secondary,
            fg=self.colors.pure_white,
            font=('Consolas', 9),
            relief='flat',
            borderwidth=0,
            insertbackground=self.colors.accent
        )
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=2, pady=2)
        
        # Modern scrollbar
        scrollbar = ttk.Scrollbar(
            text_frame,
            orient=tk.VERTICAL,
            command=self.status_text.yview
        )
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
    def setup_control_panel(self, parent):
        """Set up the modern control panel."""
        panel = tk.Frame(parent, bg=self.colors.deep_black)
        panel.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 0))
        
        # Button container
        button_container = tk.Frame(panel, bg=self.colors.deep_black)
        button_container.pack(expand=True)
        
        # Reference analysis button
        self.reference_btn = ttk.Button(
            button_container,
            text="📊 Analyze Reference",
            command=self.analyze_reference,
            style='Modern.TButton'
        )
        self.reference_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Main action button
        self.analyze_btn = ttk.Button(
            button_container,
            text="🎬 Generate Highlights",
            command=self.start_analysis,
            style='Accent.TButton'
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Open folder button
        self.open_folder_btn = ttk.Button(
            button_container,
            text="📁 Open Output",
            command=self.open_output_folder,
            style='Modern.TButton'
        )
        self.open_folder_btn.pack(side=tk.LEFT)
        
        # Add button hover effects
        self.setup_button_animations()
        
    def setup_button_animations(self):
        """Set up smooth hover animations for buttons."""
        def create_hover_effect(button, normal_style, hover_style):
            def on_enter(event):
                button.configure(style=hover_style)
                
            def on_leave(event):
                button.configure(style=normal_style)
                
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
        
        # Create hover styles
        self.style.configure(
            'ModernHover.TButton',
            background=self.colors.glass_hover,
            foreground=self.colors.accent,
            borderwidth=1,
            relief='flat'
        )
        
        self.style.configure(
            'AccentHover.TButton',
            background=self.colors.accent_dim,
            foreground=self.colors.deep_black,
            borderwidth=0,
            relief='flat'
        )
        
        # Apply hover effects
        create_hover_effect(self.reference_btn, 'Modern.TButton', 'ModernHover.TButton')
        create_hover_effect(self.open_folder_btn, 'Modern.TButton', 'ModernHover.TButton')
        create_hover_effect(self.analyze_btn, 'Accent.TButton', 'AccentHover.TButton')
        
    def animate_glassmorphism_status_indicator(self, state):
        """Animate the status indicator with glassmorphism effects."""
        colors = {
            'ready': self.colors.success,
            'analyzing': self.colors.warning,
            'error': self.colors.error
        }
        
        status_texts = {
            'ready': 'Ready',
            'analyzing': 'Processing',
            'error': 'Error'
        }
        
        if state == 'analyzing':
            # Enhanced pulsing animation for analyzing state
            def pulse():
                if self.is_analyzing:
                    current_color = self.status_indicator.cget('fg')
                    new_color = colors['analyzing'] if current_color == self.colors.muted_white else self.colors.muted_white
                    self.status_indicator.configure(fg=new_color)
                    # Animate status text
                    self.animation_manager.morphing_transition(
                        self.status_text, 
                        self.colors.glass_hover,
                        duration=250
                    )
                    self.root.after(750, pulse)
                else:
                    self.status_indicator.configure(fg=colors.get('ready', self.colors.success))
                    self.status_text.configure(text='Ready')
            pulse()
        else:
            self.status_indicator.configure(fg=colors.get(state, self.colors.success))
            self.status_text.configure(text=status_texts.get(state, 'Ready'))
    
    def update_progress_bar_style(self, mode='indeterminate'):
        """Update progress bar with smooth animations."""
        if mode == 'indeterminate':
            self.progress_bar.configure(mode='indeterminate')
            self.progress_bar.start(10)  # Smooth animation
        else:
            self.progress_bar.stop()
            self.progress_bar.configure(mode='determinate')
    
    def on_file_drop(self, event):
        """Handle file drop event with modern visual feedback."""
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0]
            # Check if it's a video file (basic check)
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
            if pathlib.Path(file_path).suffix.lower() in video_extensions:
                self.current_video_path.set(file_path)
                self.log_message(f"✅ Video file loaded: {os.path.basename(file_path)}")
                self.animate_glassmorphism_drop_success()
            else:
                messagebox.showerror("Invalid File", "Please drop a video file.")
                self.animate_glassmorphism_drop_error()
                
    def animate_glassmorphism_drop_success(self):
        """Animate successful file drop with glassmorphism effects."""
        # Enhanced success animation
        original_bg = self.drop_frame.cget('bg')
        self.drop_frame.configure(
            bg=self.colors.success,
            highlightbackground=self.colors.success
        )
        
        # Show success notification
        self.show_notification("File Loaded", "Video file loaded successfully", "success")
        
        # Animate back to normal with glassmorphism transition
        def restore_normal():
            self.animation_manager.morphing_transition(
                self.drop_frame, 
                original_bg,
                duration=200
            )
            self.drop_frame.configure(
                bg=original_bg,
                highlightbackground=self.colors.border_subtle
            )
        
        self.root.after(200, restore_normal)
        
    def animate_glassmorphism_drop_error(self):
        """Animate failed file drop with glassmorphism effects."""
        # Enhanced error animation
        original_bg = self.drop_frame.cget('bg')
        self.drop_frame.configure(
            bg=self.colors.error,
            highlightbackground=self.colors.error
        )
        
        # Show error notification
        self.show_notification("Invalid File", "Please select a valid video file", "error")
        
        # Animate back to normal
        def restore_normal():
            self.animation_manager.morphing_transition(
                self.drop_frame, 
                original_bg,
                duration=200
            )
            self.drop_frame.configure(
                bg=original_bg,
                highlightbackground=self.colors.border_subtle
            )
        
        self.root.after(200, restore_normal)
                
    def browse_video_file(self):
        """Open file dialog to select video file with modern styling."""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.current_video_path.set(file_path)
            self.log_message(f"✅ Video file selected: {os.path.basename(file_path)}")
            
    def browse_output_directory(self):
        """Open directory dialog to select output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_directory.set(directory)
            self.log_message(f"📁 Output directory set: {directory}")
            
    def log_message(self, message):
        """Add a styled message to the status text area with modern formatting."""
        import datetime
        
        self.status_text.configure(state='normal')
        
        # Add timestamp
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Configure text tags for styling
        self.status_text.tag_configure(
            "timestamp", 
            foreground=self.colors['text_muted'],
            font=('Consolas', 8)
        )
        self.status_text.tag_configure(
            "success", 
            foreground=self.colors['success'],
            font=('Consolas', 9, 'bold')
        )
        self.status_text.tag_configure(
            "warning", 
            foreground=self.colors['warning'],
            font=('Consolas', 9, 'bold')
        )
        self.status_text.tag_configure(
            "error", 
            foreground=self.colors['error'],
            font=('Consolas', 9, 'bold')
        )
        self.status_text.tag_configure(
            "info", 
            foreground=self.colors['text_primary'],
            font=('Consolas', 9)
        )
        
        # Insert timestamp
        self.status_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Style message based on content
        if "✅" in message or "success" in message.lower():
            self.status_text.insert(tk.END, f"{message}\n", "success")
        elif "⚠️" in message or "warning" in message.lower():
            self.status_text.insert(tk.END, f"{message}\n", "warning")
        elif "❌" in message or "error" in message.lower() or "fail" in message.lower():
            self.status_text.insert(tk.END, f"{message}\n", "error")
        else:
            self.status_text.insert(tk.END, f"{message}\n", "info")
        
        self.status_text.configure(state='disabled')
        self.status_text.see(tk.END)
        self.root.update_idletasks()
        
    def analyze_reference(self):
        """Analyze the reference video to get decibel information."""
        if not self.current_video_path.get():
            messagebox.showerror("No Video", "Please select a video file first.")
            return
            
        if not os.path.exists(self.current_video_path.get()):
            messagebox.showerror("File Not Found", "The selected video file does not exist.")
            return
            
        self.log_message("Starting reference analysis...")
        
        def run_reference_analysis():
            try:
                self.root.after(0, lambda: self.log_message("Extracting audio from video..."))
                
                # Extract audio
                audio_path = processor.extract_audio_from_video(
                    self.current_video_path.get(), 
                    self.temp_dir.name
                )
                
                self.root.after(0, lambda: self.log_message("Analyzing audio characteristics..."))
                
                # Use streaming or legacy processor based on setting
                if self.use_streaming.get():
                    self.root.after(0, lambda: self.log_message("Using streaming processing (memory efficient)..."))
                    audio_processor = processor.StreamingAudioProcessor(audio_path)
                else:
                    self.root.after(0, lambda: self.log_message("Using legacy processing (faster but more memory)..."))
                    audio_processor = processor.AudioProcessor(audio_path)
                
                avg_db = audio_processor.get_avg_decibel()
                max_db = audio_processor.get_max_decibel()
                
                # Better threshold calculation for gaming content
                # Use multiple recommendations based on content type
                db_range = max_db - avg_db
                
                # Conservative (fewer clips, only very loud moments)
                conservative_threshold = max_db - 2.0
                
                # Balanced (good for most gaming content)
                balanced_threshold = avg_db + (db_range * 0.6)
                
                # Aggressive (more clips, catches quieter highlights)
                aggressive_threshold = avg_db + (db_range * 0.4)
                
                # Default to balanced
                recommended_threshold = balanced_threshold
                
                # Update UI in main thread
                self.root.after(0, lambda: self.show_reference_results(
                    avg_db, max_db, recommended_threshold, 
                    conservative_threshold, balanced_threshold, aggressive_threshold
                ))
                
            except RuntimeError as e:
                error_msg = str(e)
                self.root.after(0, lambda: self.show_ffmpeg_error(error_msg))
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self.log_message(f"Reference analysis failed: {error_msg}"))
                
        # Run in separate thread
        thread = threading.Thread(target=run_reference_analysis, daemon=True)
        thread.start()
        
    def show_reference_results(self, avg_db, max_db, recommended_threshold, 
                               conservative_threshold, balanced_threshold, aggressive_threshold):
        """Show reference analysis results with multiple threshold options."""
        self.log_message(f"Reference Analysis Complete:")
        self.log_message(f"  Average Decibel: {avg_db:.1f} dB")
        self.log_message(f"  Maximum Decibel: {max_db:.1f} dB")
        self.log_message(f"  Dynamic Range: {max_db - avg_db:.1f} dB")
        self.log_message("")
        self.log_message("Threshold Recommendations:")
        self.log_message(f"  🎯 Balanced (Recommended): {balanced_threshold:.1f} dB")
        self.log_message(f"  🔒 Conservative (Fewer clips): {conservative_threshold:.1f} dB") 
        self.log_message(f"  🔓 Aggressive (More clips): {aggressive_threshold:.1f} dB")
        
        # Create a custom dialog with multiple options
        self.show_threshold_options_dialog(
            balanced_threshold, conservative_threshold, aggressive_threshold
        )
            
    def show_threshold_options_dialog(self, balanced, conservative, aggressive):
        """Show dialog with multiple threshold options."""
        import tkinter as tk
        from tkinter import ttk
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Choose Threshold Setting")
        dialog.geometry("450x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"450x300+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Select Threshold Setting", 
                 font=('TkDefaultFont', 12, 'bold')).pack(pady=(0, 15))
        
        # Threshold options
        threshold_var = tk.StringVar(value="balanced")
        
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Balanced option (recommended)
        balanced_frame = ttk.Frame(options_frame)
        balanced_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(balanced_frame, text=f"🎯 Balanced: {balanced:.1f} dB (Recommended)", 
                       variable=threshold_var, value="balanced").pack(anchor=tk.W)
        ttk.Label(balanced_frame, text="Good balance for most gaming content", 
                 foreground="gray", font=('TkDefaultFont', 9)).pack(anchor=tk.W, padx=(20, 0))
        
        # Conservative option
        conservative_frame = ttk.Frame(options_frame)
        conservative_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(conservative_frame, text=f"🔒 Conservative: {conservative:.1f} dB", 
                       variable=threshold_var, value="conservative").pack(anchor=tk.W)
        ttk.Label(conservative_frame, text="Fewer clips, only very loud moments", 
                 foreground="gray", font=('TkDefaultFont', 9)).pack(anchor=tk.W, padx=(20, 0))
        
        # Aggressive option
        aggressive_frame = ttk.Frame(options_frame)
        aggressive_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(aggressive_frame, text=f"🔓 Aggressive: {aggressive:.1f} dB", 
                       variable=threshold_var, value="aggressive").pack(anchor=tk.W)
        ttk.Label(aggressive_frame, text="More clips, catches quieter highlights", 
                 foreground="gray", font=('TkDefaultFont', 9)).pack(anchor=tk.W, padx=(20, 0))
        
        # Manual option
        manual_frame = ttk.Frame(options_frame)
        manual_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(manual_frame, text="✏️ Keep current setting", 
                       variable=threshold_var, value="manual").pack(anchor=tk.W)
        ttk.Label(manual_frame, text=f"Use current threshold: {self.decibel_threshold.get():.1f} dB", 
                 foreground="gray", font=('TkDefaultFont', 9)).pack(anchor=tk.W, padx=(20, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def apply_threshold():
            choice = threshold_var.get()
            if choice == "balanced":
                new_threshold = balanced
            elif choice == "conservative":
                new_threshold = conservative
            elif choice == "aggressive":
                new_threshold = aggressive
            else:  # manual
                dialog.destroy()
                return
                
            self.decibel_threshold.set(new_threshold)
            self.threshold_label.configure(text=f"{new_threshold:.1f} dB")
            self.log_message(f"✅ Threshold updated to {new_threshold:.1f} dB ({choice})")
            dialog.destroy()
        
        ttk.Button(button_frame, text="Apply", command=apply_threshold).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
            
    def show_ffmpeg_error(self, error_msg):
        """Show FFmpeg-specific error with helpful guidance."""
        self.log_message(f"❌ FFmpeg Error: {error_msg}")
        
        if "not found" in error_msg.lower():
            messagebox.showerror("FFmpeg Not Found", 
                               "FFmpeg is not installed or not in your PATH.\n\n"
                               "Please install FFmpeg:\n"
                               "• Windows: Download from https://ffmpeg.org or use 'choco install ffmpeg'\n"
                               "• macOS: 'brew install ffmpeg'\n"
                               "• Linux: 'sudo apt install ffmpeg' or similar\n\n"
                               "After installation, restart the application.")
        else:
            messagebox.showerror("FFmpeg Error", 
                               f"FFmpeg failed to process the video:\n\n{error_msg}\n\n"
                               "Please check:\n"
                               "• Video file is not corrupted\n"
                               "• You have write permissions to the output directory\n"
                               "• FFmpeg is properly installed")
            
    def start_analysis(self):
        """Start the highlight analysis process with modern UI feedback."""
        if self.is_analyzing:
            return
            
        if not self.current_video_path.get():
            messagebox.showerror("No Video", "Please select a video file first.")
            return
            
        if not os.path.exists(self.current_video_path.get()):
            messagebox.showerror("File Not Found", "The selected video file does not exist.")
            return
            
        # Create output directory if it doesn't exist
        output_path = pathlib.Path(self.output_directory.get())
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Update UI for analysis state
        self.is_analyzing = True
        self.analyze_btn.configure(text="⏳ Analyzing...", state='disabled')
        self.update_progress_bar_style('indeterminate')
        self.animate_glassmorphism_status_indicator('analyzing')
        
        self.log_message("🚀 Starting highlight analysis...")
        self.log_message(f"📹 Video: {os.path.basename(self.current_video_path.get())}")
        self.log_message(f"📁 Output: {self.output_directory.get()}")
        self.log_message(f"🎯 Threshold: {self.decibel_threshold.get():.1f} dB")
        self.log_message(f"🔄 Mode: {'Streaming (Memory Efficient)' if self.use_streaming.get() else 'Legacy (Faster)'}")
        
        # Run analysis in separate thread
        self.analysis_thread = threading.Thread(target=self.run_analysis, daemon=True)
        self.analysis_thread.start()
        
    def run_analysis(self):
        """Run the actual analysis in a background thread."""
        try:
            # Extract audio
            self.root.after(0, lambda: self.log_message("Extracting audio from video..."))
            audio_path = processor.extract_audio_from_video(
                self.current_video_path.get(), 
                self.temp_dir.name
            )
            
            # Create analyzer based on processing mode
            self.root.after(0, lambda: self.log_message("Initializing analyzer..."))
            
            if self.use_streaming.get():
                # Use streaming processing
                audio_processor = processor.StreamingAudioProcessor(audio_path)
                audio_analyzer = analyzer.StreamingAudioAnalysis(
                    video_path=self.current_video_path.get(),
                    audio_processor=audio_processor,
                    output_path=self.output_directory.get(),
                    decibel_threshold=self.decibel_threshold.get()
                )
            else:
                # Use legacy processing
                audio_analyzer = analyzer.AudioAnalysis(
                    video_path=self.current_video_path.get(),
                    audio_path=audio_path,
                    output_path=self.output_directory.get(),
                    decibel_threshold=self.decibel_threshold.get()
                )
            
            # Set clip length settings (split total length around highlight moment)
            total_length = self.clip_length.get()
            audio_analyzer.start_point = total_length // 2  # Half before
            audio_analyzer.end_point = total_length - audio_analyzer.start_point  # Half after (handles odd numbers)
            
            # Run analysis
            self.root.after(0, lambda: self.log_message("Analyzing audio for highlights..."))
            
            if self.use_streaming.get():
                audio_analyzer.streaming_crest_ceiling_algorithm()
            else:
                audio_analyzer.crest_ceiling_algorithm()
            
            # Export results
            self.root.after(0, lambda: self.log_message("Exporting analysis results..."))
            audio_analyzer.export()
            
            # Generate highlight clips with futuristic animations
            highlight_count = len(audio_analyzer._captured_result)
            self.root.after(0, lambda: self.log_message(f"Found {highlight_count} highlights to process"))
            
            if highlight_count == 0:
                self.root.after(0, lambda: self.log_message("⚠️ No highlights found! Try lowering the decibel threshold."))
                self.root.after(0, lambda: self.analysis_complete(0))
                return

            self.root.after(0, lambda: self.log_message(f"🎮 Initializing Highlight Forge v3.0 for {highlight_count} clips..."))
            
            # Use optimized generator with animations enabled
            clip_generator = analyzer.OptimizedClipGenerator(max_workers=4, use_animations=True)
            completed_count, failed_count = clip_generator.generate_clips_parallel(
                audio_analyzer._captured_result,
                self.current_video_path.get(),
                self.output_directory.get(),
                audio_analyzer.start_point,
                audio_analyzer.end_point
            )

            # Report results with actual counts
            self.root.after(0, lambda: self.analysis_complete_with_results(completed_count, failed_count, highlight_count))
            
        except RuntimeError as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.analysis_failed_ffmpeg(error_msg))
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.analysis_failed(error_msg))
            
    def verify_clips_generated(self, expected_count):
        """Verify that video clips were actually generated."""
        import time
        import glob
        
        # Wait a moment for file system to update
        time.sleep(1)
        
        # Count actual video files
        video_pattern = os.path.join(self.output_directory.get(), "*.mp4")
        video_files = glob.glob(video_pattern)
        actual_count = len(video_files)
        
        self.log_message(f"Verification: {actual_count} video files found out of {expected_count} expected")
        
        if actual_count == 0:
            self.log_message("❌ No video clips were generated!")
            self.log_message("This usually means FFmpeg failed to create the clips.")
            self.log_message("Check that FFmpeg is properly installed and in your PATH.")
        elif actual_count < expected_count:
            self.log_message(f"⚠️ Only {actual_count}/{expected_count} clips were generated")
            self.log_message("Some clips may have failed due to FFmpeg errors")
        
        # Complete analysis with actual count
        self.analysis_complete(actual_count)
        
    def analysis_complete_with_results(self, completed_count, failed_count, expected_count):
        """Handle analysis completion with detailed results and cyber effects."""
        self.is_analyzing = False
        self.progress_bar.stop()
        self.analyze_btn.configure(text="🎬 Generate Highlights", state='normal')
        
        total_processed = completed_count + failed_count
        
        # Show cyber completion effect
        if completed_count > 0:
            completion_msg = f"HIGHLIGHT EXTRACTION COMPLETE! {completed_count} clips generated!"
            self._show_completion_effect(completion_msg)
        
        if failed_count > 0:
            self.log_message(f"✅ Analysis complete! {completed_count} clips generated successfully, {failed_count} failed.")
            self.log_message(f"Clips saved to: {self.output_directory.get()}")
            
            if completed_count > 0:
                messagebox.showwarning("Partial Success", 
                                     f"Generated {completed_count} out of {expected_count} clips.\n"
                                     f"{failed_count} clips failed (likely FFmpeg errors).\n\n"
                                     f"Successful clips saved to:\n{self.output_directory.get()}")
            else:
                messagebox.showerror("Generation Failed", 
                                   f"All {expected_count} clips failed to generate.\n\n"
                                   "This is usually due to FFmpeg errors or file permissions.\n"
                                   "Check the log for details.")
        else:
            self.log_message(f"✅ Analysis complete! Generated {completed_count} highlight clips successfully.")
            self.log_message(f"Clips saved to: {self.output_directory.get()}")
            
            messagebox.showinfo("Analysis Complete", 
                               f"Successfully generated {completed_count} highlight clips!\n\n"
                               f"Clips saved to:\n{self.output_directory.get()}")
        
    def analysis_complete(self, highlight_count):
        """Handle successful analysis completion with modern UI updates and cyber effects."""
        self.is_analyzing = False
        self.update_progress_bar_style('determinate')
        self.progress_bar.configure(value=100)
        self.analyze_btn.configure(text="🎬 Generate Highlights", state='normal')
        self.animate_glassmorphism_status_indicator('ready')
        
        self.log_message(f"✅ Analysis complete! Generated {highlight_count} highlight clips.")
        self.log_message(f"📁 Clips saved to: {self.output_directory.get()}")
        
        if highlight_count > 0:
            # Show cyber completion effect
            completion_msg = f"MISSION ACCOMPLISHED! {highlight_count} highlights extracted!"
            self._show_completion_effect(completion_msg)
            
            messagebox.showinfo("Analysis Complete", 
                               f"Successfully generated {highlight_count} highlight clips!\n\n"
                               f"Clips saved to:\n{self.output_directory.get()}")
        else:
            messagebox.showwarning("No Highlights Found", 
                                  "No highlights were found with the current settings.\n\n"
                                  "Try lowering the decibel threshold or use 'Analyze Reference' "
                                  "to find a better threshold.")
            
    def analysis_failed(self, error_message):
        """Handle analysis failure with modern UI updates."""
        self.is_analyzing = False
        self.update_progress_bar_style('determinate')
        self.progress_bar.configure(value=0)
        self.analyze_btn.configure(text="🎬 Generate Highlights", state='normal')
        self.animate_glassmorphism_status_indicator('error')
        
        self.log_message(f"❌ Analysis failed: {error_message}")
        messagebox.showerror("Analysis Failed", f"Analysis failed with error:\n\n{error_message}")
        
    def analysis_failed_ffmpeg(self, error_message):
        """Handle FFmpeg-specific analysis failure with modern UI updates."""
        self.is_analyzing = False
        self.update_progress_bar_style('determinate')
        self.progress_bar.configure(value=0)
        self.analyze_btn.configure(text="🎬 Generate Highlights", state='normal')
        self.animate_glassmorphism_status_indicator('error')
        
        self.log_message(f"❌ FFmpeg Error: {error_message}")
        
        if "not found" in error_message.lower():
            messagebox.showerror("FFmpeg Not Found", 
                               "FFmpeg is required but not found on your system.\n\n"
                               "Please install FFmpeg:\n"
                               "• Windows: Download from https://ffmpeg.org or use 'choco install ffmpeg'\n"
                               "• macOS: 'brew install ffmpeg'\n"
                               "• Linux: 'sudo apt install ffmpeg'\n\n"
                               "After installation, restart the application.")
        else:
            messagebox.showerror("Video Processing Error", 
                               f"Failed to process video file:\n\n{error_message}\n\n"
                               "Please check:\n"
                               "• Video file is not corrupted\n"
                               "• File format is supported\n"
                               "• You have sufficient disk space")
        
    def open_output_folder(self):
        """Open the output folder in the file manager."""
        output_path = self.output_directory.get()
        if os.path.exists(output_path):
            # Cross-platform way to open folder
            import subprocess
            import sys
            
            if sys.platform == "win32":
                os.startfile(output_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", output_path])
            else:
                subprocess.run(["xdg-open", output_path])
        else:
            messagebox.showerror("Folder Not Found", "Output folder does not exist yet.")
            
    def run(self):
        """Start the modern GUI application."""
        self.log_message("🔥 M0 Clipper: Highlight Forge v3.0 initialized!")
        self.log_message("⚡ Cyber systems online. Drop a video file or click Browse to begin extraction.")
        self.animate_glassmorphism_status_indicator('ready')
        self.root.mainloop()
        
    def __del__(self):
        """Clean up temporary directory."""
        if hasattr(self, 'temp_dir'):
            self.temp_dir.cleanup()


def main():
    """Main entry point for the GUI application."""
    # Try new modular GUI first, fallback to legacy if needed
    try:
        app = ModernHighlighterGUI()  # This redirects to new modular GUI
        app.run()
    except Exception:
        # Ultimate fallback to legacy implementation
        app = LegacyModernHighlighterGUI()
        app.run()


if __name__ == "__main__":
    main()