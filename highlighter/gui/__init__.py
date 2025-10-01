"""
Modular GUI package for M0 Clipper.

This package implements a professional modular architecture for the M0 Clipper GUI,
breaking down the monolithic design into focused, maintainable components.

Architecture Overview:
- components/: Reusable UI components
- layouts/: Layout management system  
- events/: Event handling system
- state/: Application state management
- services/: Business logic services
- utils/: GUI utilities and helpers

This design follows professional software engineering principles:
- Single Responsibility Principle
- Dependency Injection
- Event-Driven Architecture
- Comprehensive Error Handling
"""

# Import core infrastructure
from ..core import ErrorHandler, ValidationError, setup_logging

# Main GUI entry point
from .main_window import MainApplication

# Initialize logging for GUI package
logger = setup_logging()

def main():
    """Main entry point for the modular GUI application."""
    try:
        app = MainApplication()
        app.run()
    except Exception as e:
        error_handler = ErrorHandler()
        error_handler.handle_startup_error(e)
        raise

__all__ = ["MainApplication", "main"]