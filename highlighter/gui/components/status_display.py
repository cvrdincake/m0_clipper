"""
Status display component for M0 Clipper GUI.

Handles progress tracking, status messages, and log display.
Extracted from the monolithic GUI to improve maintainability and testability.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import List, Optional

from highlighter.gui.components.base_component import BaseComponent
from highlighter.glassmorphism import GlassPanel
from highlighter.core.error_handler import ErrorHandler


class StatusComponent(BaseComponent):
    """
    Professional status display component with glassmorphism styling.
    
    Features:
    - Real-time progress tracking
    - Status message logging
    - Analysis results display
    - Visual feedback system
    """
    
    def create_widget(self) -> tk.Widget:
        """Create the main status display panel."""
        self.panel = GlassPanel(
            self.parent,
            self.theme,
            title="Status & Progress"
        )
        return self.panel
    
    def initialize(self):
        """Initialize the status component."""
        self.setup_progress_bar()
        self.setup_status_log()
        self.setup_results_display()
        
        # Initialize log storage
        self.log_messages: List[str] = []
        self.max_log_entries = 100
        
    def setup_progress_bar(self):
        """Set up the progress bar and status indicator."""
        # Progress frame
        progress_frame = tk.Frame(
            self.panel.content_frame,
            bg=self.theme.colors.glass_primary
        )
        progress_frame.grid(
            row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 12)
        )
        progress_frame.columnconfigure(1, weight=1)
        
        # Status indicator
        self.status_indicator = tk.Label(
            progress_frame,
            text="●",
            fg=self.theme.colors.muted_white,
            bg=self.theme.colors.glass_primary,
            font=('Inter', 14, 'bold')
        )
        self.status_indicator.grid(row=0, column=0, padx=(0, 8))
        
        # Status text
        self.status_text = tk.Label(
            progress_frame,
            text="Ready",
            fg=self.theme.colors.pure_white,
            bg=self.theme.colors.glass_primary,
            font=self.theme.fonts['body'],
            anchor='w'
        )
        self.status_text.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 8))
        
        # Progress bar
        style = ttk.Style()
        style.configure(
            "Glass.Horizontal.TProgressbar",
            background=self.theme.colors.accent_primary,
            troughcolor=self.theme.colors.glass_secondary,
            borderwidth=0,
            lightcolor=self.theme.colors.accent_primary,
            darkcolor=self.theme.colors.accent_primary
        )
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            style="Glass.Horizontal.TProgressbar",
            mode='determinate',
            length=200
        )
        self.progress_bar.grid(row=0, column=2, padx=(8, 0))
    
    def setup_status_log(self):
        """Set up the status message log."""
        # Log frame
        log_frame = tk.Frame(
            self.panel.content_frame,
            bg=self.theme.colors.glass_primary
        )
        log_frame.grid(
            row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 12)
        )
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text widget with scrollbar
        text_frame = tk.Frame(
            log_frame,
            bg=self.theme.colors.glass_secondary,
            relief='flat',
            bd=1,
            highlightbackground=self.theme.colors.border_subtle,
            highlightthickness=1
        )
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Text widget
        self.log_text = tk.Text(
            text_frame,
            bg=self.theme.colors.glass_secondary,
            fg=self.theme.colors.pure_white,
            font=('Consolas', 9),
            relief='flat',
            bd=0,
            wrap=tk.WORD,
            height=8,
            state='disabled',
            insertbackground=self.theme.colors.pure_white
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=8, pady=8)
        
        # Scrollbar
        log_scrollbar = ttk.Scrollbar(
            text_frame,
            orient=tk.VERTICAL,
            command=self.log_text.yview
        )
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S), padx=(0, 8), pady=8)
        self.log_text.config(yscrollcommand=log_scrollbar.set)
    
    def setup_results_display(self):
        """Set up the analysis results display."""
        # Results frame
        results_frame = tk.Frame(
            self.panel.content_frame,
            bg=self.theme.colors.glass_primary
        )
        results_frame.grid(
            row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 0)
        )
        results_frame.columnconfigure([0, 1, 2], weight=1)
        
        # Results labels
        self.clips_generated_label = tk.Label(
            results_frame,
            text="Clips: 0",
            fg=self.theme.colors.muted_white,
            bg=self.theme.colors.glass_primary,
            font=self.theme.fonts['caption']
        )
        self.clips_generated_label.grid(row=0, column=0, pady=4)
        
        self.processing_time_label = tk.Label(
            results_frame,
            text="Time: 0s",
            fg=self.theme.colors.muted_white,
            bg=self.theme.colors.glass_primary,
            font=self.theme.fonts['caption']
        )
        self.processing_time_label.grid(row=0, column=1, pady=4)
        
        self.file_size_label = tk.Label(
            results_frame,
            text="Size: 0 MB",
            fg=self.theme.colors.muted_white,
            bg=self.theme.colors.glass_primary,
            font=self.theme.fonts['caption']
        )
        self.file_size_label.grid(row=0, column=2, pady=4)
    
    def bind_events(self):
        """Bind component-specific events."""
        # Subscribe to state changes
        self.state_manager.subscribe("analysis_state_changed", self.on_analysis_state_changed)
        self.state_manager.subscribe("analysis_results_saved", self.on_analysis_results_saved)
    
    def log_message(self, message: str, level: str = "info"):
        """Add a message to the status log."""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}"
            
            # Add to message storage
            self.log_messages.append(formatted_message)
            
            # Limit log size
            if len(self.log_messages) > self.max_log_entries:
                self.log_messages = self.log_messages[-self.max_log_entries:]
            
            # Update text widget
            self.log_text.config(state='normal')
            self.log_text.insert(tk.END, formatted_message + "\n")
            
            # Apply color coding based on level
            if level == "error":
                line_start = f"{self.log_text.index(tk.END)} linestart"
                line_end = f"{self.log_text.index(tk.END)} lineend"
                self.log_text.tag_add("error", line_start, line_end)
                self.log_text.tag_config("error", foreground=self.theme.colors.error)
            elif level == "success":
                line_start = f"{self.log_text.index(tk.END)} linestart"
                line_end = f"{self.log_text.index(tk.END)} lineend"
                self.log_text.tag_add("success", line_start, line_end)
                self.log_text.tag_config("success", foreground=self.theme.colors.success)
            
            # Auto-scroll to bottom
            self.log_text.see(tk.END)
            self.log_text.config(state='disabled')
            
        except Exception as e:
            # Fallback error handling
            print(f"Error logging message: {e}")
    
    def update_status(self, status: str, indicator_color: Optional[str] = None):
        """Update the status indicator and text."""
        try:
            self.status_text.config(text=status)
            
            if indicator_color:
                self.status_indicator.config(fg=indicator_color)
            
        except Exception as e:
            self.error_handler.handle_status_update_error(e)
    
    def update_progress(self, value: float, maximum: float = 100.0):
        """Update the progress bar."""
        try:
            if maximum > 0:
                percentage = min(100, max(0, (value / maximum) * 100))
                self.progress_bar.config(value=percentage)
            
        except Exception as e:
            self.error_handler.handle_progress_update_error(e)
    
    def set_indeterminate_progress(self, active: bool = True):
        """Set progress bar to indeterminate mode."""
        try:
            if active:
                self.progress_bar.config(mode='indeterminate')
                self.progress_bar.start()
            else:
                self.progress_bar.stop()
                self.progress_bar.config(mode='determinate', value=0)
                
        except Exception as e:
            self.error_handler.handle_progress_mode_error(e)
    
    def update_results(self, clips_count: int = 0, processing_time: float = 0.0, total_size_mb: float = 0.0):
        """Update the analysis results display."""
        try:
            self.clips_generated_label.config(text=f"Clips: {clips_count}")
            self.processing_time_label.config(text=f"Time: {processing_time:.1f}s")
            self.file_size_label.config(text=f"Size: {total_size_mb:.1f} MB")
            
        except Exception as e:
            self.error_handler.handle_results_update_error(e)
    
    def clear_log(self):
        """Clear the status log."""
        try:
            self.log_text.config(state='normal')
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state='disabled')
            self.log_messages.clear()
            
        except Exception as e:
            self.error_handler.handle_log_clear_error(e)
    
    def on_analysis_state_changed(self, data):
        """Handle analysis state changes."""
        is_analyzing = data["new_state"]
        
        if is_analyzing:
            self.update_status("Analyzing video...", self.theme.colors.accent_primary)
            self.set_indeterminate_progress(True)
            self.log_message("🚀 Starting highlight analysis...", "info")
        else:
            self.update_status("Ready", self.theme.colors.muted_white)
            self.set_indeterminate_progress(False)
    
    def on_analysis_results_saved(self, data):
        """Handle analysis results."""
        try:
            clips_count = data.get("clips_generated", 0)
            processing_time = data.get("processing_time", 0.0)
            total_size = data.get("total_size_mb", 0.0)
            
            self.update_results(clips_count, processing_time, total_size)
            
            if clips_count > 0:
                self.log_message(f"✅ Analysis complete! Generated {clips_count} highlight clips", "success")
                self.update_status(f"Complete - {clips_count} clips generated", self.theme.colors.success)
            else:
                self.log_message("⚠️ No highlights found with current settings", "error")
                self.update_status("No highlights found", self.theme.colors.warning)
                
        except Exception as e:
            self.error_handler.handle_results_processing_error(e)