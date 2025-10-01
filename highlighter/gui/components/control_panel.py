"""
Control panel component for M0 Clipper GUI.

Handles action buttons and analysis control workflow.
Extracted from the monolithic GUI to improve maintainability and testability.
"""

import tkinter as tk
from typing import Optional

from .base_component import BaseComponent
from ...glassmorphism import GlassButton
from ...core import ValidationError


class ControlComponent(BaseComponent):
    """
    Professional control panel component with glassmorphism styling.
    
    Features:
    - Analysis workflow controls
    - Reference analysis functionality
    - Output folder access
    - State-aware button management
    """
    
    def __init__(self, parent, theme, state_manager, analysis_service, error_handler):
        """Initialize with analysis service dependency."""
        self.analysis_service = analysis_service
        super().__init__(parent, theme, state_manager, error_handler)
    
    def create_widget(self) -> tk.Widget:
        """Create the main control panel."""
        # Control panel container
        self.panel = tk.Frame(
            self.parent,
            bg=self.theme.colors.deep_black
        )
        return self.panel
    
    def initialize(self):
        """Initialize the control component."""
        self.setup_button_container()
        self.setup_control_buttons()
        
    def setup_button_container(self):
        """Set up the button container with glassmorphism styling."""
        # Enhanced button container
        self.button_container = tk.Frame(
            self.panel,
            bg=self.theme.colors.glass_primary,
            relief='flat',
            bd=1,
            highlightbackground=self.theme.colors.border_subtle,
            highlightthickness=1
        )
        self.button_container.pack(expand=True, padx=2, pady=2)
        
        # Button content frame
        self.button_content = tk.Frame(
            self.button_container,
            bg=self.theme.colors.glass_primary
        )
        self.button_content.pack(expand=True, padx=20, pady=16)
    
    def setup_control_buttons(self):
        """Set up all control buttons."""
        # Reference analysis button
        self.reference_btn = GlassButton(
            self.button_content,
            self.theme,
            "📊 Analyze Reference",
            command=self.analyze_reference,
            style="secondary"
        )
        self.reference_btn.pack(side=tk.LEFT, padx=(0, 16))
        
        # Main analysis button
        self.analyze_btn = GlassButton(
            self.button_content,
            self.theme,
            "🎬 Generate Highlights",
            command=self.start_analysis,
            style="primary"
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 16))
        
        # Open folder button
        self.open_folder_btn = GlassButton(
            self.button_content,
            self.theme,
            "📁 Open Output",
            command=self.open_output_folder,
            style="secondary"
        )
        self.open_folder_btn.pack(side=tk.LEFT)
    
    def bind_events(self):
        """Bind component-specific events."""
        # Subscribe to state changes
        self.state_manager.subscribe("analysis_state_changed", self.on_analysis_state_changed)
        self.state_manager.subscribe("video_path_changed", self.on_video_path_changed)
    
    def analyze_reference(self):
        """Start reference analysis to determine optimal threshold."""
        try:
            # Validate video file is selected
            if not self.state_manager.state.current_video_path:
                from tkinter import messagebox
                messagebox.showerror("No Video", "Please select a video file first.")
                return
            
            # Start reference analysis through service
            self.analysis_service.start_reference_analysis()
            
        except Exception as e:
            self.error_handler.handle_reference_analysis_error(e)
    
    def start_analysis(self):
        """Start the main highlight analysis."""
        try:
            # Check if already analyzing
            if self.state_manager.state.is_analyzing:
                return
            
            # Validate video file is selected
            if not self.state_manager.state.current_video_path:
                from tkinter import messagebox
                messagebox.showerror("No Video", "Please select a video file first.")
                return
            
            # Validate state
            issues = self.state_manager.validate_current_state()
            if issues:
                from tkinter import messagebox
                messagebox.showerror("Validation Error", "\n".join(issues))
                return
            
            # Start analysis through service
            self.analysis_service.start_highlight_analysis()
            
        except Exception as e:
            self.error_handler.handle_analysis_start_error(e)
    
    def open_output_folder(self):
        """Open the output folder in the system file manager."""
        try:
            import subprocess
            import platform
            import os
            
            output_dir = self.state_manager.state.output_directory
            
            # Create directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Open in file manager based on platform
            if platform.system() == "Windows":
                subprocess.run(["explorer", output_dir])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", output_dir])
            else:  # Linux
                subprocess.run(["xdg-open", output_dir])
                
        except Exception as e:
            self.error_handler.handle_folder_open_error(e)
    
    def on_analysis_state_changed(self, data):
        """Handle analysis state changes."""
        is_analyzing = data["new_state"]
        
        if is_analyzing:
            # Disable buttons during analysis
            self.analyze_btn.configure(text="⏳ Analyzing...", state='disabled')
            self.reference_btn.configure(state='disabled')
        else:
            # Re-enable buttons
            self.analyze_btn.configure(text="🎬 Generate Highlights", state='normal')
            self.reference_btn.configure(state='normal')
    
    def on_video_path_changed(self, data):
        """Handle video path changes."""
        new_path = data["new_path"]
        
        # Enable/disable buttons based on video selection
        if new_path:
            self.analyze_btn.configure(state='normal')
            self.reference_btn.configure(state='normal')
        else:
            self.analyze_btn.configure(state='disabled')
            self.reference_btn.configure(state='disabled')
    
    def enable(self):
        """Enable all control buttons."""
        if self.state_manager.state.current_video_path and not self.state_manager.state.is_analyzing:
            self.analyze_btn.configure(state='normal')
            self.reference_btn.configure(state='normal')
        self.open_folder_btn.configure(state='normal')
    
    def disable(self):
        """Disable all control buttons."""
        self.analyze_btn.configure(state='disabled')
        self.reference_btn.configure(state='disabled')
        self.open_folder_btn.configure(state='disabled')