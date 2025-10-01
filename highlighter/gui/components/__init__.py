"""
GUI Components package for M0 Clipper.

Provides modular, reusable UI components following professional
software engineering principles.
"""

from .base_component import BaseComponent
from .video_input import VideoInputComponent
from .settings_panel import SettingsComponent
from .control_panel import ControlComponent
from .status_display import StatusComponent

__all__ = [
    "BaseComponent",
    "VideoInputComponent", 
    "SettingsComponent",
    "ControlComponent",
    "StatusComponent"
]