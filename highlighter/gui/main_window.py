"""
Main application window for M0 Clipper GUI.

This module contains the primary application window that coordinates
all GUI components and manages the overall application lifecycle.
"""

import tkinter as tk
from tkinter import ttk
import sys
import threading
from typing import Optional

try:
    from tkinterdnd2 import TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

from ..glassmorphism import GlassmorphismTheme, AnimationManager
from ..window_effects import WindowEffects, GlassmorphismNotification
from ..core import ErrorHandler, setup_logging
from .state import get_state_manager, StateManager
from .components.video_input import VideoInputComponent
from .components.settings_panel import SettingsComponent  
from .components.control_panel import ControlComponent
from .components.status_display import StatusComponent
from .services.analysis_service import AnalysisService
from .services.notification_service import NotificationService


class MainApplication:
    """
    Main application window for M0 Clipper.
    
    Coordinates all GUI components and manages the application lifecycle
    following professional architecture patterns.
    """
    
    def __init__(self):
        """Initialize the main application window."""
        self.setup_logging()
        self.initialize_core_services()
        self.create_main_window()
        self.setup_theme_and_effects()
        self.initialize_components()
        self.setup_layout()
        self.bind_events()
        
        # Async processing support
        self._cleanup_scheduled = False
        self._analysis_service = None
        
    def setup_logging(self):
        """Initialize logging for the application."""
        self.logger = setup_logging()
        self.logger.info("Initializing M0 Clipper GUI application")
        
    def initialize_core_services(self):
        """Initialize core application services."""
        self.error_handler = ErrorHandler()
        self.state_manager = get_state_manager()
        
        # Initialize services
        self.analysis_service = AnalysisService(self.state_manager)
        self._analysis_service = self.analysis_service  # Keep reference for cleanup
        self.notification_service = NotificationService()
        
        # Link state manager to root for async updates
        self.state_manager.root_widget = self.root
        
    def create_main_window(self):
        """Create and configure the main application window."""
        try:
            # Create main window with drag-and-drop support if available
            if DND_AVAILABLE:
                self.root = TkinterDnD.Tk()
                self.logger.info("Drag-and-drop support enabled")
            else:
                self.root = tk.Tk()
                self.logger.warning("Drag-and-drop support not available")
            
            # Configure window
            self.root.title("M0 Clipper - Professional Highlight Generator")
            self.root.geometry("1000x800")
            self.root.minsize(900, 700)
            
            # Set up window close handler
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
        except Exception as e:
            self.error_handler.handle_window_creation_error(e)
            raise
    
    def setup_theme_and_effects(self):
        """Initialize theme and visual effects."""
        try:
            # Initialize glassmorphism theme
            self.glass_theme = GlassmorphismTheme()
            self.root.configure(bg=self.glass_theme.colors.deep_black)
            
            # Initialize animation manager
            self.animation_manager = AnimationManager(self.glass_theme)
            
            # Initialize window effects
            self.window_effects = WindowEffects(self.root)
            self.notifications = GlassmorphismNotification(self.root)
            
            # Enable advanced window effects
            self.enable_glassmorphism_effects()
            
            self.logger.info("Theme and effects initialized successfully")
            
        except Exception as e:
            self.logger.warning(f"Some visual effects may not be available: {e}")
            # Continue without advanced effects
    
    def enable_glassmorphism_effects(self):
        """Enable advanced glassmorphism window effects."""
        try:
            self.window_effects.enable_blur_effect("acrylic")
            self.window_effects.set_window_transparency(0.96)
            self.window_effects.add_drop_shadow()
        except Exception as e:
            self.logger.debug(f"Advanced window effects not supported: {e}")
    
    def initialize_components(self):
        """Initialize all GUI components."""
        try:
            # Create main container
            self.main_container = tk.Frame(
                self.root, 
                bg=self.glass_theme.colors.deep_black
            )
            
            # Initialize components with dependency injection
            self.video_input = VideoInputComponent(
                parent=self.main_container,
                theme=self.glass_theme,
                state_manager=self.state_manager,
                error_handler=self.error_handler
            )
            
            self.settings_panel = SettingsComponent(
                parent=self.main_container,
                theme=self.glass_theme,
                state_manager=self.state_manager,
                error_handler=self.error_handler
            )
            
            self.control_panel = ControlComponent(
                parent=self.main_container,
                theme=self.glass_theme,
                state_manager=self.state_manager,
                analysis_service=self.analysis_service,
                error_handler=self.error_handler
            )
            
            self.status_display = StatusComponent(
                parent=self.main_container,
                theme=self.glass_theme,
                state_manager=self.state_manager,
                error_handler=self.error_handler
            )
            
            self.logger.info("All GUI components initialized successfully")
            
        except Exception as e:
            self.error_handler.handle_component_initialization_error(e)
            raise
    
    def setup_layout(self):
        """Set up the main window layout."""
        try:
            # Configure main container
            self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            self.main_container.columnconfigure(0, weight=1)
            
            # Layout components
            self.video_input.widget.grid(
                row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 16)
            )
            
            self.settings_panel.widget.grid(
                row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 16)
            )
            
            self.control_panel.widget.grid(
                row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 16)
            )
            
            self.status_display.widget.grid(
                row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0)
            )
            
            # Configure row weights for responsive layout
            self.main_container.rowconfigure(3, weight=1)  # Status display expands
            
            self.logger.info("Main window layout configured")
            
        except Exception as e:
            self.error_handler.handle_layout_error(e)
            raise
    
    def bind_events(self):
        """Bind application-level events."""
        try:
            # State change events
            self.state_manager.subscribe("analysis_state_changed", self.on_analysis_state_changed)
            self.state_manager.subscribe("video_path_changed", self.on_video_path_changed)
            
            # Window events
            self.root.bind("<Configure>", self.on_window_configure)
            
            # Keyboard shortcuts
            self.root.bind("<Control-o>", lambda e: self.video_input.browse_file())
            self.root.bind("<Control-Return>", lambda e: self.control_panel.start_analysis())
            self.root.bind("<F5>", lambda e: self.control_panel.analyze_reference())
            self.root.bind("<Escape>", lambda e: self._stop_current_analysis())  # Emergency stop
            
            self.logger.info("Event bindings configured")
            
        except Exception as e:
            self.error_handler.handle_event_binding_error(e)
    
    def on_analysis_state_changed(self, data):
        """Handle analysis state changes."""
        is_analyzing = data["new_state"]
        
        # Update window title
        if is_analyzing:
            self.root.title("M0 Clipper - Analyzing...")
        else:
            self.root.title("M0 Clipper - Professional Highlight Generator")
    
    def on_video_path_changed(self, data):
        """Handle video path changes."""
        new_path = data["new_path"]
        if new_path:
            self.logger.info(f"Video file selected: {new_path}")
    
    def on_window_configure(self, event):
        """Handle window configuration changes."""
        if event.widget == self.root:
            # Save window geometry to state
            geometry = self.root.geometry()
            self.state_manager.state.window_geometry = geometry
    
    def _stop_current_analysis(self):
        """Emergency stop for current analysis (triggered by Escape key)."""
        if self._analysis_service:
            self._analysis_service.stop_analysis()
            self.logger.info("Analysis stopped by user (Escape key)")
    
    def on_closing(self):
        """Handle application closing with proper cleanup."""
        try:
            self.logger.info("Application closing...")
            
            # Stop any running analysis
            if self._analysis_service:
                self._analysis_service.stop_analysis()
            
            # Schedule cleanup for background operations
            if not self._cleanup_scheduled:
                self._cleanup_scheduled = True
                self.root.after(100, self._perform_cleanup)
            
        except Exception as e:
            self.logger.error(f"Error during application closing: {e}")
            # Force close if cleanup fails
            self.root.destroy()
    
    def _perform_cleanup(self):
        """Perform final cleanup of resources."""
        try:
            # Stop animations
            if hasattr(self, 'animation_manager'):
                self.animation_manager.stop_all_animations()
            
            # Clean up services
            if self._analysis_service:
                self._analysis_service.stop_analysis()
            
            # Save state
            if hasattr(self, 'state_manager'):
                self.state_manager.save_state()
            
            self.logger.info("Cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
        finally:
            # Force destroy to prevent hanging
            self.root.destroy()
    
    def run(self):
        """Start the main application event loop."""
        try:
            self.logger.info("Starting M0 Clipper GUI application")
            
            # Show startup notification
            self.notification_service.show_startup_notification()
            
            # Start the main event loop
            self.root.mainloop()
            
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
            self.on_closing()
        except Exception as e:
            self.error_handler.handle_application_error(e)
            raise


def main():
    """Entry point for the modular GUI application."""
    try:
        app = MainApplication()
        app.run()
    except Exception as e:
        # Final error handler if everything else fails
        import traceback
        print(f"Fatal error starting M0 Clipper: {e}")
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()