"""
Settings panel component for M0 Clipper GUI.

Handles configuration controls for analysis parameters.
Extracted from the monolithic GUI to improve maintainability and testability.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional

from .base_component import BaseComponent
from ...glassmorphism import GlassPanel, GlassButton
from ...core import ValidationError


class SettingsComponent(BaseComponent):
    """
    Professional settings panel component with glassmorphism styling.
    
    Features:
    - Analysis parameter controls
    - Real-time validation
    - Visual feedback for settings changes
    """
    
    def create_widget(self) -> tk.Widget:
        """Create the main settings panel."""
        self.panel = GlassPanel(
            self.parent,
            self.theme,
            title="Analysis Settings"
        )
        return self.panel
    
    def initialize(self):
        """Initialize the settings component."""
        self.setup_threshold_controls()
        self.setup_clip_length_controls()
        self.setup_processing_mode()
        self.setup_output_directory()
        
    def setup_threshold_controls(self):
        """Set up decibel threshold controls."""
        # Threshold frame
        threshold_frame = tk.Frame(
            self.panel.content_frame,
            bg=self.theme.colors.glass_primary
        )
        threshold_frame.grid(
            row=0, column=0, columnspan=2,
            sticky=(tk.W, tk.E), pady=(0, 12)
        )
        threshold_frame.columnconfigure(1, weight=1)
        
        # Threshold label
        threshold_label = tk.Label(
            threshold_frame,
            text="Decibel Threshold:",
            bg=self.theme.colors.glass_primary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['body']
        )
        threshold_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 12))
        
        # Threshold scale
        self.threshold_scale = ttk.Scale(
            threshold_frame,
            from_=-60.0,
            to=0.0,
            orient=tk.HORIZONTAL,
            command=self.on_threshold_changed
        )
        self.threshold_scale.grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 12)
        )
        self.threshold_scale.set(self.state_manager.state.decibel_threshold)
        
        # Threshold value display
        self.threshold_value = tk.Label(
            threshold_frame,
            text=f"{self.state_manager.state.decibel_threshold:.1f} dB",
            bg=self.theme.colors.glass_primary,
            fg=self.theme.colors.accent_primary,
            font=self.theme.fonts['body']
        )
        self.threshold_value.grid(row=0, column=2, sticky=tk.W)
    
    def setup_clip_length_controls(self):
        """Set up clip length controls."""
        # Clip length frame
        length_frame = tk.Frame(
            self.panel.content_frame,
            bg=self.theme.colors.glass_primary
        )
        length_frame.grid(
            row=1, column=0, columnspan=2,
            sticky=(tk.W, tk.E), pady=(0, 12)
        )
        length_frame.columnconfigure(1, weight=1)
        
        # Length label
        length_label = tk.Label(
            length_frame,
            text="Clip Length:",
            bg=self.theme.colors.glass_primary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['body']
        )
        length_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 12))
        
        # Length scale
        self.length_scale = ttk.Scale(
            length_frame,
            from_=5,
            to=120,
            orient=tk.HORIZONTAL,
            command=self.on_length_changed
        )
        self.length_scale.grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 12)
        )
        self.length_scale.set(self.state_manager.state.clip_length)
        
        # Length value display
        self.length_value = tk.Label(
            length_frame,
            text=f"{self.state_manager.state.clip_length}s",
            bg=self.theme.colors.glass_primary,
            fg=self.theme.colors.accent_primary,
            font=self.theme.fonts['body']
        )
        self.length_value.grid(row=0, column=2, sticky=tk.W)
    
    def setup_processing_mode(self):
        """Set up processing mode controls."""
        # Processing mode frame
        mode_frame = tk.Frame(
            self.panel.content_frame,
            bg=self.theme.colors.glass_primary
        )
        mode_frame.grid(
            row=2, column=0, columnspan=2,
            sticky=(tk.W, tk.E), pady=(0, 12)
        )
        
        # Mode label
        mode_label = tk.Label(
            mode_frame,
            text="Processing Mode:",
            bg=self.theme.colors.glass_primary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['body']
        )
        mode_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 12))
        
        # Streaming checkbox
        self.streaming_var = tk.BooleanVar(
            value=self.state_manager.state.use_streaming
        )
        streaming_check = tk.Checkbutton(
            mode_frame,
            text="Use Streaming (Memory Efficient)",
            variable=self.streaming_var,
            command=self.on_streaming_changed,
            bg=self.theme.colors.glass_primary,
            fg=self.theme.colors.pure_white,
            selectcolor=self.theme.colors.glass_secondary,
            activebackground=self.theme.colors.glass_primary,
            activeforeground=self.theme.colors.pure_white,
            font=self.theme.fonts['body']
        )
        streaming_check.grid(row=0, column=1, sticky=tk.W)
    
    def setup_output_directory(self):
        """Set up output directory controls."""
        from tkinter import filedialog
        
        # Output directory frame
        output_frame = tk.Frame(
            self.panel.content_frame,
            bg=self.theme.colors.glass_primary
        )
        output_frame.grid(
            row=3, column=0, columnspan=2,
            sticky=(tk.W, tk.E), pady=(0, 0)
        )
        output_frame.columnconfigure(1, weight=1)
        
        # Output label
        output_label = tk.Label(
            output_frame,
            text="Output Directory:",
            bg=self.theme.colors.glass_primary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['body']
        )
        output_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 12))
        
        # Output entry
        self.output_entry = tk.Entry(
            output_frame,
            bg=self.theme.colors.glass_secondary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['body'],
            relief='flat',
            bd=1,
            highlightbackground=self.theme.colors.border_subtle,
            highlightthickness=1
        )
        self.output_entry.grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 12)
        )
        self.output_entry.insert(0, self.state_manager.state.output_directory)
        
        # Browse output button
        self.output_browse_btn = GlassButton(
            output_frame,
            self.theme,
            "Browse",
            command=self.browse_output_directory,
            style="secondary"
        )
        self.output_browse_btn.grid(row=0, column=2)
    
    def bind_events(self):
        """Bind component-specific events."""
        # Subscribe to state changes
        self.state_manager.subscribe("analysis_parameters_changed", self.on_parameters_changed)
        self.state_manager.subscribe("output_directory_changed", self.on_output_directory_changed)
        
        # Bind output entry changes
        self.output_entry.bind('<FocusOut>', self.on_output_entry_changed)
        self.output_entry.bind('<Return>', self.on_output_entry_changed)
    
    def on_threshold_changed(self, value):
        """Handle threshold scale changes."""
        try:
            threshold = float(value)
            self.threshold_value.config(text=f"{threshold:.1f} dB")
            self.state_manager.set_analysis_parameters(decibel_threshold=threshold)
        except Exception as e:
            self.error_handler.handle_threshold_change_error(e)
    
    def on_length_changed(self, value):
        """Handle clip length scale changes."""
        try:
            length = int(float(value))
            self.length_value.config(text=f"{length}s")
            self.state_manager.set_analysis_parameters(clip_length=length)
        except Exception as e:
            self.error_handler.handle_length_change_error(e)
    
    def on_streaming_changed(self):
        """Handle streaming mode changes."""
        try:
            use_streaming = self.streaming_var.get()
            self.state_manager.set_analysis_parameters(use_streaming=use_streaming)
        except Exception as e:
            self.error_handler.handle_streaming_change_error(e)
    
    def on_output_entry_changed(self, event):
        """Handle output directory entry changes."""
        try:
            directory = self.output_entry.get().strip()
            if directory:
                self.state_manager.set_output_directory(directory)
        except Exception as e:
            self.error_handler.handle_output_directory_error(e)
    
    def browse_output_directory(self):
        """Open directory dialog to select output directory."""
        try:
            from tkinter import filedialog
            directory = filedialog.askdirectory(
                title="Select Output Directory",
                initialdir=self.state_manager.state.output_directory
            )
            
            if directory:
                self.output_entry.delete(0, tk.END)
                self.output_entry.insert(0, directory)
                self.state_manager.set_output_directory(directory)
                
        except Exception as e:
            self.error_handler.handle_directory_browse_error(e)
    
    def on_parameters_changed(self, data):
        """Handle parameter changes from state manager."""
        # Update UI to reflect state changes
        if "decibel_threshold" in data:
            new_threshold = data["decibel_threshold"][1]
            self.threshold_scale.set(new_threshold)
            self.threshold_value.config(text=f"{new_threshold:.1f} dB")
        
        if "clip_length" in data:
            new_length = data["clip_length"][1]
            self.length_scale.set(new_length)
            self.length_value.config(text=f"{new_length}s")
        
        if "use_streaming" in data:
            new_streaming = data["use_streaming"][1]
            self.streaming_var.set(new_streaming)
    
    def on_output_directory_changed(self, data):
        """Handle output directory changes from state manager."""
        new_directory = data["new_directory"]
        
        # Update entry if it's different
        current_text = self.output_entry.get()
        if current_text != new_directory:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, new_directory)
    
    def enable(self):
        """Enable all settings controls."""
        self.threshold_scale.config(state='normal')
        self.length_scale.config(state='normal')
        self.output_entry.config(state='normal')
        
    def disable(self):
        """Disable all settings controls."""
        self.threshold_scale.config(state='disabled')
        self.length_scale.config(state='disabled')
        self.output_entry.config(state='readonly')