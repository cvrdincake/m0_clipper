"""
Services package for M0 Clipper GUI.

Provides business logic services that coordinate between
UI components and core application functionality.
"""

from highlighter.gui.services.analysis_service import AnalysisService
from highlighter.gui.services.notification_service import NotificationService, NotificationType

__all__ = [
    "AnalysisService",
    "NotificationService", 
    "NotificationType"
]