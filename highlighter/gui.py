#!/usr/bin/env python3
"""
Professional glassmorphism GUI client for the auto-highlighter tool.
Features modern dark mode design with smooth animations and glass effects.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import pathlib
import tempfile
from typing import Optional

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    print("Warning: tkinterdnd2 not available. Drag-and-drop functionality will be disabled.")

from . import analyzer, processor
from .common import similarity
from .animations import show_boot_sequence, show_glitch_effect
from rich.console import Console


class ModernHighlighterGUI:
    """Professional glassmorphism GUI for M0 Clipper."""
    
    # Glassmorphism Color Palette
    COLORS = {
        'bg_primary': '#0F0F0F',        # Deep black background
        'bg_secondary': '#1A1A1A',      # Secondary black
        'bg_glass': '#1F1F1F',          # Glass panel background
        'bg_glass_hover': '#2A2A2A',    # Glass panel hover
        'accent': '#FFFFFF',            # Pure white accent
        'accent_dim': '#E0E0E0',        # Dimmed white
        'text_primary': '#FFFFFF',      # Primary text
        'text_secondary': '#B0B0B0',    # Secondary text
        'text_muted': '#808080',        # Muted text
        'border': '#333333',            # Border color
        'border_focus': '#505050',      # Focused border
        'success': '#00FF88',           # Success green
        'warning': '#FFAA00',           # Warning orange
        'error': '#FF4444',             # Error red
        'glass_alpha': '80'             # Transparency for glass effects
    }
    
    def __init__(self):
        # Create main window with drag-and-drop support
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
            
        self.root.title("M0 Clipper - Professional Highlight Generator")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        self.root.configure(bg=self.COLORS['bg_primary'])
        
        # Configure modern styling
        self.setup_modern_styles()
        
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
        
        # Show cyber boot sequence on startup
        self._show_startup_sequence()
        
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
    
    def setup_modern_styles(self):
        """Configure modern glassmorphism styling."""
        self.style = ttk.Style()
        
        # Configure dark theme base
        self.style.theme_use('clam')
        
        # Glass Panel Style
        self.style.configure(
            'Glass.TFrame',
            background=self.COLORS['bg_glass'],
            relief='flat',
            borderwidth=1
        )
        
        # Modern Button Styles
        self.style.configure(
            'Modern.TButton',
            background=self.COLORS['bg_glass'],
            foreground=self.COLORS['text_primary'],
            borderwidth=1,
            relief='flat',
            font=('Segoe UI', 10, 'normal'),
            padding=(20, 10)
        )
        
        self.style.configure(
            'Accent.TButton',
            background=self.COLORS['accent'],
            foreground=self.COLORS['bg_primary'],
            borderwidth=0,
            relief='flat',
            font=('Segoe UI', 11, 'bold'),
            padding=(25, 12)
        )
        
        # Modern Entry Style
        self.style.configure(
            'Modern.TEntry',
            fieldbackground=self.COLORS['bg_glass'],
            foreground=self.COLORS['text_primary'],
            borderwidth=1,
            relief='flat',
            insertcolor=self.COLORS['accent']
        )
        
        # Modern Label Styles
        self.style.configure(
            'Title.TLabel',
            background=self.COLORS['bg_primary'],
            foreground=self.COLORS['accent'],
            font=('Segoe UI', 24, 'bold')
        )
        
        self.style.configure(
            'Subtitle.TLabel',
            background=self.COLORS['bg_primary'],
            foreground=self.COLORS['text_secondary'],
            font=('Segoe UI', 12, 'normal')
        )
        
        self.style.configure(
            'Glass.TLabel',
            background=self.COLORS['bg_glass'],
            foreground=self.COLORS['text_primary'],
            font=('Segoe UI', 10, 'normal')
        )
        
        self.style.configure(
            'GlassSecondary.TLabel',
            background=self.COLORS['bg_glass'],
            foreground=self.COLORS['text_secondary'],
            font=('Segoe UI', 9, 'normal')
        )
        
        # Modern LabelFrame Style
        self.style.configure(
            'Glass.TLabelframe',
            background=self.COLORS['bg_glass'],
            foreground=self.COLORS['text_primary'],
            borderwidth=1,
            relief='flat'
        )
        
        self.style.configure(
            'Glass.TLabelframe.Label',
            background=self.COLORS['bg_glass'],
            foreground=self.COLORS['accent'],
            font=('Segoe UI', 11, 'bold')
        )
        
        # Modern Scale Style
        self.style.configure(
            'Modern.Horizontal.TScale',
            background=self.COLORS['bg_glass'],
            troughcolor=self.COLORS['bg_secondary'],
            borderwidth=0,
            lightcolor=self.COLORS['accent'],
            darkcolor=self.COLORS['accent']
        )
        
        # Modern Progressbar Style
        self.style.configure(
            'Modern.Horizontal.TProgressbar',
            background=self.COLORS['accent'],
            troughcolor=self.COLORS['bg_secondary'],
            borderwidth=0,
            lightcolor=self.COLORS['accent'],
            darkcolor=self.COLORS['accent']
        )
        
    def setup_modern_ui(self):
        """Set up the modern glassmorphism user interface."""
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.COLORS['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Configure grid weights
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Header section
        self.setup_header(main_container)
        
        # Content area with glass panels
        content_frame = tk.Frame(main_container, bg=self.COLORS['bg_primary'])
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(2, weight=1)
        
        # Video input panel
        self.setup_video_input_panel(content_frame)
        
        # Settings panel
        self.setup_settings_panel(content_frame)
        
        # Progress panel
        self.setup_progress_panel(content_frame)
        
        # Control panel
        self.setup_control_panel(content_frame)
        
    def setup_header(self, parent):
        """Set up the modern header section."""
        header_frame = tk.Frame(parent, bg=self.COLORS['bg_primary'])
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # App icon/logo area
        icon_frame = tk.Frame(header_frame, bg=self.COLORS['bg_primary'], width=60, height=60)
        icon_frame.grid(row=0, column=0, padx=(0, 20), sticky=tk.W)
        icon_frame.grid_propagate(False)
        
        # Icon placeholder (you can add an actual icon here)
        icon_label = tk.Label(
            icon_frame, 
            text="🎬", 
            bg=self.COLORS['bg_primary'],
            fg=self.COLORS['accent'],
            font=('Segoe UI', 32)
        )
        icon_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title and subtitle
        title_frame = tk.Frame(header_frame, bg=self.COLORS['bg_primary'])
        title_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(
            title_frame, 
            text="M0 Clipper", 
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        subtitle_label = ttk.Label(
            title_frame, 
            text="Professional Highlight Generator v0.2.0", 
            style='Subtitle.TLabel'
        )
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
        
        # Status indicator
        self.status_indicator = tk.Label(
            header_frame,
            text="●",
            bg=self.COLORS['bg_primary'],
            fg=self.COLORS['success'],
            font=('Segoe UI', 16)
        )
        self.status_indicator.grid(row=0, column=2, padx=(20, 0))
        
    def setup_video_input_panel(self, parent):
        """Set up the modern video input panel with glassmorphism."""
        # Glass panel container
        panel = self.create_glass_panel(parent, "Video Input")
        panel.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Modern drag and drop area
        if DND_AVAILABLE:
            self.drop_area = self.create_modern_drop_area(panel)
            self.drop_area.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        else:
            self.drop_area = self.create_fallback_area(panel)
            self.drop_area.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # File path display
        path_frame = tk.Frame(panel, bg=self.COLORS['bg_glass'])
        path_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        path_frame.columnconfigure(1, weight=1)
        
        ttk.Label(
            path_frame, 
            text="Selected:", 
            style='Glass.TLabel'
        ).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.file_entry = ttk.Entry(
            path_frame, 
            textvariable=self.current_video_path, 
            state='readonly',
            style='Modern.TEntry',
            font=('Segoe UI', 10)
        )
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Modern browse button
        browse_btn = ttk.Button(
            path_frame,
            text="Browse",
            command=self.browse_video_file,
            style='Modern.TButton'
        )
        browse_btn.grid(row=0, column=2)
        
    def create_glass_panel(self, parent, title):
        """Create a glassmorphism panel with title."""
        panel_frame = ttk.LabelFrame(
            parent,
            text=title,
            style='Glass.TLabelframe',
            padding=20
        )
        return panel_frame
        
    def create_modern_drop_area(self, parent):
        """Create modern drag and drop area with glassmorphism styling."""
        drop_container = tk.Frame(parent, bg=self.COLORS['bg_glass'])
        
        # Main drop area
        self.drop_frame = tk.Frame(
            drop_container,
            bg=self.COLORS['bg_secondary'],
            relief='flat',
            borderwidth=2,
            height=120
        )
        self.drop_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.drop_frame.pack_propagate(False)
        
        # Drop content
        content_frame = tk.Frame(self.drop_frame, bg=self.COLORS['bg_secondary'])
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Drop icon
        drop_icon = tk.Label(
            content_frame,
            text="⬇",
            bg=self.COLORS['bg_secondary'],
            fg=self.COLORS['text_muted'],
            font=('Segoe UI', 24)
        )
        drop_icon.pack()
        
        # Drop text
        drop_label = tk.Label(
            content_frame,
            text="Drop video file here or click to browse",
            bg=self.COLORS['bg_secondary'],
            fg=self.COLORS['text_secondary'],
            font=('Segoe UI', 11)
        )
        drop_label.pack(pady=(5, 0))
        
        # Supported formats
        formats_label = tk.Label(
            content_frame,
            text="Supports: MP4, AVI, MOV, MKV, and more",
            bg=self.COLORS['bg_secondary'],
            fg=self.COLORS['text_muted'],
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
        fallback_container = tk.Frame(parent, bg=self.COLORS['bg_glass'])
        
        fallback_frame = tk.Frame(
            fallback_container,
            bg=self.COLORS['bg_secondary'],
            relief='flat',
            borderwidth=2,
            height=120
        )
        fallback_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        fallback_frame.pack_propagate(False)
        
        content_frame = tk.Frame(fallback_frame, bg=self.COLORS['bg_secondary'])
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        browse_icon = tk.Label(
            content_frame,
            text="📁",
            bg=self.COLORS['bg_secondary'],
            fg=self.COLORS['text_muted'],
            font=('Segoe UI', 24)
        )
        browse_icon.pack()
        
        browse_label = tk.Label(
            content_frame,
            text="Click here to browse for video files",
            bg=self.COLORS['bg_secondary'],
            fg=self.COLORS['text_secondary'],
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
            self.drop_frame.configure(bg=self.COLORS['bg_glass_hover'])
            
        def on_leave(event):
            self.drop_frame.configure(bg=self.COLORS['bg_secondary'])
            
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
        
        output_frame = tk.Frame(panel, bg=self.COLORS['bg_glass'])
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
        
        threshold_container = tk.Frame(panel, bg=self.COLORS['bg_glass'])
        threshold_container.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(10, 0))
        threshold_container.columnconfigure(0, weight=1)
        
        # Threshold scale
        threshold_frame = tk.Frame(threshold_container, bg=self.COLORS['bg_glass'])
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
        
        clip_container = tk.Frame(panel, bg=self.COLORS['bg_glass'])
        clip_container.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(15, 0))
        
        clip_frame = tk.Frame(clip_container, bg=self.COLORS['bg_glass'])
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
        advanced_frame = tk.Frame(panel, bg=self.COLORS['bg_glass'])
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
        progress_frame = tk.Frame(panel, bg=self.COLORS['bg_glass'])
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
        text_frame = tk.Frame(panel, bg=self.COLORS['bg_glass'])
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(15, 0))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Custom text widget with dark styling
        self.status_text = tk.Text(
            text_frame,
            height=8,
            wrap=tk.WORD,
            state='disabled',
            bg=self.COLORS['bg_secondary'],
            fg=self.COLORS['text_primary'],
            font=('Consolas', 9),
            relief='flat',
            borderwidth=0,
            insertbackground=self.COLORS['accent']
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
        panel = tk.Frame(parent, bg=self.COLORS['bg_primary'])
        panel.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 0))
        
        # Button container
        button_container = tk.Frame(panel, bg=self.COLORS['bg_primary'])
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
            background=self.COLORS['bg_glass_hover'],
            foreground=self.COLORS['accent'],
            borderwidth=1,
            relief='flat'
        )
        
        self.style.configure(
            'AccentHover.TButton',
            background=self.COLORS['accent_dim'],
            foreground=self.COLORS['bg_primary'],
            borderwidth=0,
            relief='flat'
        )
        
        # Apply hover effects
        create_hover_effect(self.reference_btn, 'Modern.TButton', 'ModernHover.TButton')
        create_hover_effect(self.open_folder_btn, 'Modern.TButton', 'ModernHover.TButton')
        create_hover_effect(self.analyze_btn, 'Accent.TButton', 'AccentHover.TButton')
        
    def animate_status_indicator(self, state):
        """Animate the status indicator."""
        colors = {
            'ready': self.COLORS['success'],
            'analyzing': self.COLORS['warning'],
            'error': self.COLORS['error']
        }
        
        if state == 'analyzing':
            # Pulsing animation for analyzing state
            def pulse():
                if self.is_analyzing:
                    current_color = self.status_indicator.cget('fg')
                    new_color = self.COLORS['warning'] if current_color == self.COLORS['text_muted'] else self.COLORS['text_muted']
                    self.status_indicator.configure(fg=new_color)
                    self.root.after(500, pulse)
                else:
                    self.status_indicator.configure(fg=colors.get('ready', self.COLORS['success']))
            pulse()
        else:
            self.status_indicator.configure(fg=colors.get(state, self.COLORS['success']))
    
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
                self.animate_drop_success()
            else:
                messagebox.showerror("Invalid File", "Please drop a video file.")
                self.animate_drop_error()
                
    def animate_drop_success(self):
        """Animate successful file drop."""
        # Brief success animation
        original_bg = self.drop_frame.cget('bg')
        self.drop_frame.configure(bg=self.COLORS['success'])
        self.root.after(150, lambda: self.drop_frame.configure(bg=original_bg))
        
    def animate_drop_error(self):
        """Animate failed file drop."""
        # Brief error animation
        original_bg = self.drop_frame.cget('bg')
        self.drop_frame.configure(bg=self.COLORS['error'])
        self.root.after(150, lambda: self.drop_frame.configure(bg=original_bg))
                
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
            foreground=self.COLORS['text_muted'],
            font=('Consolas', 8)
        )
        self.status_text.tag_configure(
            "success", 
            foreground=self.COLORS['success'],
            font=('Consolas', 9, 'bold')
        )
        self.status_text.tag_configure(
            "warning", 
            foreground=self.COLORS['warning'],
            font=('Consolas', 9, 'bold')
        )
        self.status_text.tag_configure(
            "error", 
            foreground=self.COLORS['error'],
            font=('Consolas', 9, 'bold')
        )
        self.status_text.tag_configure(
            "info", 
            foreground=self.COLORS['text_primary'],
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
        self.animate_status_indicator('analyzing')
        
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
        self.animate_status_indicator('ready')
        
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
        self.animate_status_indicator('error')
        
        self.log_message(f"❌ Analysis failed: {error_message}")
        messagebox.showerror("Analysis Failed", f"Analysis failed with error:\n\n{error_message}")
        
    def analysis_failed_ffmpeg(self, error_message):
        """Handle FFmpeg-specific analysis failure with modern UI updates."""
        self.is_analyzing = False
        self.update_progress_bar_style('determinate')
        self.progress_bar.configure(value=0)
        self.analyze_btn.configure(text="🎬 Generate Highlights", state='normal')
        self.animate_status_indicator('error')
        
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
        self.log_message("� M0 Clipper: Highlight Forge v3.0 initialized!")
        self.log_message("⚡ Cyber systems online. Drop a video file or click Browse to begin extraction.")
        self.animate_status_indicator('ready')
        self.root.mainloop()
        
    def __del__(self):
        """Clean up temporary directory."""
        if hasattr(self, 'temp_dir'):
            self.temp_dir.cleanup()


def main():
    """Main entry point for the GUI application."""
    app = ModernHighlighterGUI()
    app.run()


if __name__ == "__main__":
    main()