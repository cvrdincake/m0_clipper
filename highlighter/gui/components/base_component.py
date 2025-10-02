"""
Base component class for M0 Clipper GUI components.

Provides a common interface and shared functionality for all UI components.
"""

import tkinter as tk
from abc import ABC, abstractmethod
from typing import Optional, Any

from highlighter.core.error_handler import ErrorHandler
from highlighter.gui.state.app_state import StateManager


class BaseComponent(ABC):
    """
    Abstract base class for all GUI components.
    
    Provides common functionality and enforces a consistent interface
    for all components in the modular architecture.
    """
    
    def __init__(self, 
                 parent: tk.Widget, 
                 theme: Any,
                 state_manager: StateManager,
                 error_handler: ErrorHandler):
        """Initialize the base component."""
        self.parent = parent
        self.theme = theme
        self.state_manager = state_manager
        self.error_handler = error_handler
        
        # Create the main widget
        self.widget = self.create_widget()
        
        # Initialize component
        self.initialize()
        
        # Bind events
        self.bind_events()
    
    @abstractmethod
    def create_widget(self) -> tk.Widget:
        """Create and return the main widget for this component."""
        pass
    
    @abstractmethod
    def initialize(self):
        """Initialize the component after widget creation."""
        pass
    
    @abstractmethod
    def bind_events(self):
        """Bind component-specific events."""
        pass
    
    def destroy(self):
        """Clean up the component."""
        if hasattr(self, 'widget') and self.widget:
            self.widget.destroy()
    
    def show(self):
        """Show the component."""
        if self.widget:
            self.widget.grid()
    
    def hide(self):
        """Hide the component."""
        if self.widget:
            self.widget.grid_remove()
    
    def enable(self):
        """Enable the component."""
        # Override in subclasses as needed
        pass
    
    def disable(self):
        """Disable the component."""
        # Override in subclasses as needed
        pass