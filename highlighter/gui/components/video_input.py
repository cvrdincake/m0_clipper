"""
Video input component for M0 Clipper GUI.

Handles video file selection, drag-and-drop functionality, and file validation.
Extracted from the monolithic GUI to improve maintainability and testability.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pathlib
from typing import Optional

try:
    from tkinterdnd2 import DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

from .base_component import BaseComponent
from ...glassmorphism import GlassPanel
from ...core import ValidationError


class VideoInputComponent(BaseComponent):
    """
    Professional video input component with glassmorphism styling.
    
    Features:
    - Drag-and-drop support (when available)
    - File browser dialog
    - Video file validation
    - Visual feedback for file operations
    """
    
    def create_widget(self) -> tk.Widget:
        """Create the main video input panel."""
        # Create glass panel container
        self.panel = GlassPanel(
            self.parent,
            self.theme,
            title="Video Input"
        )
        return self.panel
    
    def initialize(self):
        """Initialize the video input component."""
        self.setup_drop_area()
        self.setup_file_path_display()
        self.setup_browse_button()
        
    def setup_drop_area(self):
        """Set up the drag-and-drop area."""
        if DND_AVAILABLE:
            self.drop_area = self.create_drag_drop_area()
        else:
            self.drop_area = self.create_fallback_area()
        
        self.drop_area.grid(
            row=0, column=0, columnspan=3, 
            sticky=(tk.W, tk.E), pady=(0, 16)
        )
    
    def create_drag_drop_area(self) -> tk.Frame:
        """Create modern drag-and-drop area."""
        # Main drop container
        drop_container = tk.Frame(
            self.panel.content_frame,
            bg=self.theme.colors.glass_secondary,
            relief='flat',
            bd=2,
            highlightbackground=self.theme.colors.border_subtle,
            highlightthickness=2
        )
        
        # Content frame
        content_frame = tk.Frame(
            drop_container,
            bg=self.theme.colors.glass_secondary
        )
        content_frame.pack(expand=True, padx=30, pady=30)
        
        # Drop icon
        icon_container = tk.Frame(
            content_frame,
            bg=self.theme.colors.glass_tertiary,
            width=60,
            height=60,
            relief='flat',
            bd=1,
            highlightbackground=self.theme.colors.border_medium,
            highlightthickness=1
        )
        icon_container.pack(pady=(0, 12))
        icon_container.pack_propagate(False)
        
        drop_icon = tk.Label(
            icon_container,
            text="🎬",
            bg=self.theme.colors.glass_tertiary,
            fg=self.theme.colors.pure_white,
            font=('Inter', 24)
        )
        drop_icon.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Drop text
        drop_label = tk.Label(
            content_frame,
            text="Drop video file here or click to browse",
            bg=self.theme.colors.glass_secondary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['heading']
        )
        drop_label.pack(pady=(0, 8))
        
        # Supported formats
        formats_label = tk.Label(
            content_frame,
            text="Supports: MP4, AVI, MOV, MKV, WebM, and more",
            bg=self.theme.colors.glass_secondary,
            fg=self.theme.colors.muted_white,
            font=self.theme.fonts['caption']
        )
        formats_label.pack()
        
        # Register drag and drop
        drop_container.drop_target_register(DND_FILES)
        drop_container.dnd_bind('<<Drop>>', self.on_file_drop)
        
        # Click to browse functionality
        drop_container.bind("<Button-1>", lambda e: self.browse_file())
        content_frame.bind("<Button-1>", lambda e: self.browse_file())
        drop_icon.bind("<Button-1>", lambda e: self.browse_file())
        drop_label.bind("<Button-1>", lambda e: self.browse_file())
        formats_label.bind("<Button-1>", lambda e: self.browse_file())
        
        # Store reference for hover effects
        self.drop_frame = drop_container
        
        return drop_container
    
    def create_fallback_area(self) -> tk.Frame:
        """Create fallback area when drag-and-drop is not available."""
        # Main container
        fallback_container = tk.Frame(
            self.panel.content_frame,
            bg=self.theme.colors.glass_secondary,
            relief='flat',
            bd=2,
            highlightbackground=self.theme.colors.border_subtle,
            highlightthickness=2
        )
        
        # Content frame
        content_frame = tk.Frame(
            fallback_container,
            bg=self.theme.colors.glass_secondary
        )
        content_frame.pack(expand=True, padx=30, pady=30)
        
        # Browse icon
        icon_container = tk.Frame(
            content_frame,
            bg=self.theme.colors.glass_tertiary,
            width=60,
            height=60,
            relief='flat',
            bd=1,
            highlightbackground=self.theme.colors.border_medium,
            highlightthickness=1
        )
        icon_container.pack(pady=(0, 12))
        icon_container.pack_propagate(False)
        
        browse_icon = tk.Label(
            icon_container,
            text="📁",
            bg=self.theme.colors.glass_tertiary,
            fg=self.theme.colors.pure_white,
            font=('Inter', 24)
        )
        browse_icon.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        browse_label = tk.Label(
            content_frame,
            text="Click here to browse for video files",
            bg=self.theme.colors.glass_secondary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['heading']
        )
        browse_label.pack(pady=(0, 8))
        
        # Click handler
        fallback_container.bind("<Button-1>", lambda e: self.browse_file())
        content_frame.bind("<Button-1>", lambda e: self.browse_file())
        browse_icon.bind("<Button-1>", lambda e: self.browse_file())
        browse_label.bind("<Button-1>", lambda e: self.browse_file())
        
        return fallback_container
    
    def setup_file_path_display(self):
        """Set up the file path display area."""
        # Path display frame
        path_frame = tk.Frame(
            self.panel.content_frame, 
            bg=self.theme.colors.glass_primary
        )
        path_frame.grid(
            row=1, column=0, columnspan=3, 
            sticky=(tk.W, tk.E), pady=(0, 12)
        )
        path_frame.columnconfigure(1, weight=1)
        
        # Path label
        path_label = tk.Label(
            path_frame,
            text="Selected File:",
            bg=self.theme.colors.glass_primary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['body']
        )
        path_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 12))
        
        # File entry container
        entry_container = tk.Frame(
            path_frame,
            bg=self.theme.colors.glass_secondary,
            relief='flat',
            bd=1,
            highlightbackground=self.theme.colors.border_subtle,
            highlightthickness=1
        )
        entry_container.grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 12)
        )
        
        # File entry
        self.file_entry = tk.Entry(
            entry_container,
            state='readonly',
            bg=self.theme.colors.glass_secondary,
            fg=self.theme.colors.pure_white,
            font=self.theme.fonts['body'],
            relief='flat',
            bd=0,
            insertbackground=self.theme.colors.pure_white
        )
        self.file_entry.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
    
    def setup_browse_button(self):
        """Set up the browse button."""
        from ...glassmorphism import GlassButton
        
        self.browse_btn = GlassButton(
            self.panel.content_frame,
            self.theme,
            "Browse Files",
            command=self.browse_file,
            style="secondary"
        )
        self.browse_btn.grid(row=1, column=2)
    
    def bind_events(self):
        """Bind component-specific events."""
        # Subscribe to state changes
        self.state_manager.subscribe("video_path_changed", self.on_video_path_changed)
    
    def on_file_drop(self, event):
        """Handle file drop event."""
        try:
            files = self.parent.master.tk.splitlist(event.data)
            if files:
                file_path = files[0]
                self.set_video_file(file_path)
                
        except Exception as e:
            self.error_handler.handle_file_drop_error(e)
    
    def browse_file(self):
        """Open file dialog to select video file."""
        try:
            file_path = filedialog.askopenfilename(
                title="Select Video File",
                filetypes=[
                    ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                self.set_video_file(file_path)
                
        except Exception as e:
            self.error_handler.handle_file_browse_error(e)
    
    def set_video_file(self, file_path: str):
        """Set the video file with validation."""
        try:
            # Validate file
            if not self.validate_video_file(file_path):
                return
            
            # Update state
            if self.state_manager.set_video_path(file_path):
                self.animate_success()
            else:
                self.animate_error()
                
        except Exception as e:
            self.error_handler.handle_video_file_error(e)
            self.animate_error()
    
    def validate_video_file(self, file_path: str) -> bool:
        """Validate the selected video file."""
        path = pathlib.Path(file_path)
        
        # Check if file exists
        if not path.exists():
            messagebox.showerror("File Not Found", "The selected file does not exist.")
            return False
        
        # Check file extension
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
        if path.suffix.lower() not in video_extensions:
            messagebox.showerror("Invalid File", "Please select a video file.")
            return False
        
        return True
    
    def on_video_path_changed(self, data):
        """Handle video path changes from state manager."""
        new_path = data["new_path"]
        
        # Update file entry display
        self.file_entry.config(state='normal')
        self.file_entry.delete(0, tk.END)
        if new_path:
            self.file_entry.insert(0, new_path)
        self.file_entry.config(state='readonly')
    
    def animate_success(self):
        """Animate successful file selection."""
        # Simple success animation - can be enhanced
        original_bg = self.drop_frame.cget('bg') if hasattr(self, 'drop_frame') else None
        if original_bg:
            self.drop_frame.config(highlightbackground=self.theme.colors.success)
            self.panel.content_frame.after(1000, 
                lambda: self.drop_frame.config(highlightbackground=self.theme.colors.border_subtle))
    
    def animate_error(self):
        """Animate error state."""
        # Simple error animation - can be enhanced
        original_bg = self.drop_frame.cget('bg') if hasattr(self, 'drop_frame') else None
        if original_bg:
            self.drop_frame.config(highlightbackground=self.theme.colors.error)
            self.panel.content_frame.after(1000, 
                lambda: self.drop_frame.config(highlightbackground=self.theme.colors.border_subtle))
    
    def get_current_file(self) -> Optional[str]:
        """Get the currently selected video file."""
        return self.state_manager.state.current_video_path
    
    def clear_file(self):
        """Clear the currently selected file."""
        self.state_manager.set_video_path("")