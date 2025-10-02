"""
State management package for M0 Clipper GUI.

Provides centralized state management with the Observer pattern
for reactive UI updates and validation.
"""

from highlighter.gui.state.app_state import StateManager, ApplicationState, get_state_manager

__all__ = ["StateManager", "ApplicationState", "get_state_manager"]