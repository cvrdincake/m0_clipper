"""
GUI Components package for M0 Clipper.

Provides modular, reusable UI components following professional
software engineering principles.
"""

from highlighter.gui.components.base_component import BaseComponent
from highlighter.gui.components.video_input import VideoInputComponent
from highlighter.gui.components.settings_panel import SettingsComponent
from highlighter.gui.components.control_panel import ControlComponent
from highlighter.gui.components.status_display import StatusComponent

__all__ = [
    "BaseComponent",
    "VideoInputComponent", 
    "SettingsComponent",
    "ControlComponent",
    "StatusComponent"
]