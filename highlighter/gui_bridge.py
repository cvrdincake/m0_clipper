#!/usr/bin/env python3
"""
Legacy GUI module bridge for M0 Clipper.

This module provides backward compatibility for the refactored GUI system.
The monolithic GUI has been converted to a professional modular architecture.

DEPRECATED: Use the new modular GUI system in highlighter.gui package.
"""

import warnings
import sys

# Import the new modular GUI system
try:
    from highlighter.gui import main as new_gui_main, MainApplication
    NEW_GUI_AVAILABLE = True
except ImportError as e:
    NEW_GUI_AVAILABLE = False
    import_error = e

def main():
    """
    Main entry point for the GUI application.
    
    Routes to the new modular GUI architecture if available,
    otherwise falls back to legacy GUI or shows error.
    """
    if NEW_GUI_AVAILABLE:
        # Show deprecation warning for legacy usage
        warnings.warn(
            "Direct import from highlighter.gui is deprecated. "
            "Use 'from highlighter.gui import main' for the new modular architecture.",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Route to new modular GUI
        return new_gui_main()
    else:
        # Try to import and use legacy GUI as fallback
        try:
            from highlighter import gui_legacy
            warnings.warn(
                "Using legacy GUI fallback. The new modular architecture is recommended.",
                UserWarning,
                stacklevel=2
            )
            return gui_legacy.main()
        except ImportError:
            # Final fallback error message
            print("ERROR: GUI system not available.")
            print(f"Modular GUI import error: {import_error}")
            print("\nPlease ensure all GUI components are properly installed.")
            raise RuntimeError("GUI system initialization failed. Please check your installation.")


# Legacy class reference for backward compatibility
class ModernHighlighterGUI:
    """
    DEPRECATED: Legacy GUI class bridge.
    
    This class provides backward compatibility for the refactored GUI system.
    New development should use the modular architecture directly.
    """
    
    def __init__(self):
        warnings.warn(
            "ModernHighlighterGUI class is deprecated. "
            "Use MainApplication from highlighter.gui package.",
            DeprecationWarning,
            stacklevel=2
        )
        
        if NEW_GUI_AVAILABLE:
            # Use new modular architecture
            self._app = MainApplication()
        else:
            # Fallback to legacy GUI
            try:
                from highlighter import gui_legacy
                self._legacy_app = gui_legacy.ModernHighlighterGUI()
            except ImportError:
                raise ImportError("No GUI system available")
    
    def run(self):
        """Run the application using available GUI system."""
        if hasattr(self, '_app'):
            return self._app.run()
        elif hasattr(self, '_legacy_app'):
            return self._legacy_app.run()
        else:
            raise RuntimeError("No GUI application initialized")


if __name__ == "__main__":
    main()