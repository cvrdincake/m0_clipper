"""
Notification service for M0 Clipper GUI.

Handles user notifications, feedback, and system messages.
Provides a clean interface for displaying various types of notifications.
"""

import tkinter as tk
from tkinter import messagebox
from typing import Optional, Dict, Any
from enum import Enum

from ...core import ErrorHandler


class NotificationType(Enum):
    """Types of notifications supported by the service."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    QUESTION = "question"


class NotificationService:
    """
    Professional notification service for user feedback.
    
    Provides consistent, user-friendly notifications across the application
    with proper error handling and theme integration.
    """
    
    def __init__(self):
        """Initialize the notification service."""
        self.error_handler = ErrorHandler()
        
        # Notification configuration
        self.notification_icons = {
            NotificationType.INFO: "ℹ️",
            NotificationType.SUCCESS: "✅",
            NotificationType.WARNING: "⚠️",
            NotificationType.ERROR: "❌",
            NotificationType.QUESTION: "❓"
        }
    
    def show_startup_notification(self):
        """Show application startup notification."""
        try:
            # Simple startup message - could be enhanced with custom dialog
            self.show_info(
                "M0 Clipper Ready",
                "Welcome to M0 Clipper! Select a video file to get started."
            )
        except Exception as e:
            self.error_handler.handle_startup_notification_error(e)
    
    def show_info(self, title: str, message: str, details: Optional[str] = None):
        """Show an informational notification."""
        try:
            full_message = self._format_message(message, details)
            messagebox.showinfo(title, full_message)
        except Exception as e:
            self.error_handler.handle_notification_error(e, "info")
    
    def show_success(self, title: str, message: str, details: Optional[str] = None):
        """Show a success notification."""
        try:
            full_message = self._format_message(message, details)
            messagebox.showinfo(title, full_message)
        except Exception as e:
            self.error_handler.handle_notification_error(e, "success")
    
    def show_warning(self, title: str, message: str, details: Optional[str] = None):
        """Show a warning notification."""
        try:
            full_message = self._format_message(message, details)
            messagebox.showwarning(title, full_message)
        except Exception as e:
            self.error_handler.handle_notification_error(e, "warning")
    
    def show_error(self, title: str, message: str, details: Optional[str] = None):
        """Show an error notification."""
        try:
            full_message = self._format_message(message, details)
            messagebox.showerror(title, full_message)
        except Exception as e:
            self.error_handler.handle_notification_error(e, "error")
    
    def ask_question(self, title: str, message: str, details: Optional[str] = None) -> bool:
        """Show a yes/no question dialog."""
        try:
            full_message = self._format_message(message, details)
            return messagebox.askyesno(title, full_message)
        except Exception as e:
            self.error_handler.handle_notification_error(e, "question")
            return False
    
    def show_analysis_complete(self, clips_count: int, processing_time: float, output_dir: str):
        """Show analysis completion notification with results."""
        try:
            if clips_count > 0:
                self.show_success(
                    "Analysis Complete!",
                    f"Successfully generated {clips_count} highlight clips",
                    f"Processing time: {processing_time:.1f} seconds\nOutput directory: {output_dir}"
                )
            else:
                self.show_warning(
                    "No Highlights Found",
                    "No highlights were found with the current settings.",
                    "Try lowering the decibel threshold or use 'Analyze Reference' to find a better threshold."
                )
        except Exception as e:
            self.error_handler.handle_analysis_notification_error(e)
    
    def show_reference_results(self, avg_db: float, max_db: float, 
                             recommended_threshold: float) -> bool:
        """Show reference analysis results and ask if user wants to apply."""
        try:
            message = f"""Reference Analysis Results:

Average Volume: {avg_db:.1f} dB
Maximum Volume: {max_db:.1f} dB
Recommended Threshold: {recommended_threshold:.1f} dB

Would you like to use the recommended threshold?"""
            
            return self.ask_question("Reference Analysis Complete", message)
            
        except Exception as e:
            self.error_handler.handle_reference_results_error(e)
            return False
    
    def show_file_validation_error(self, file_path: str, error_details: str):
        """Show file validation error notification."""
        try:
            self.show_error(
                "File Validation Error",
                f"The selected file could not be validated: {file_path}",
                error_details
            )
        except Exception as e:
            self.error_handler.handle_file_validation_notification_error(e)
    
    def show_analysis_error(self, error_message: str, suggestions: Optional[str] = None):
        """Show analysis error notification with suggestions."""
        try:
            details = None
            if suggestions:
                details = f"Suggestions:\n{suggestions}"
            
            self.show_error(
                "Analysis Error",
                f"Analysis failed: {error_message}",
                details
            )
        except Exception as e:
            self.error_handler.handle_analysis_error_notification_error(e)
    
    def show_ffmpeg_error(self, error_message: str):
        """Show FFmpeg-specific error notification with guidance."""
        try:
            suggestions = """Please check:
• Video file is not corrupted
• File format is supported
• You have sufficient disk space
• FFmpeg is properly installed"""
            
            self.show_error(
                "Video Processing Error",
                f"Failed to process video file:\n\n{error_message}",
                suggestions
            )
        except Exception as e:
            self.error_handler.handle_ffmpeg_error_notification_error(e)
    
    def show_dependency_error(self, dependency: str, install_command: Optional[str] = None):
        """Show dependency error notification with installation guidance."""
        try:
            details = None
            if install_command:
                details = f"To install: {install_command}"
            
            self.show_error(
                "Missing Dependency",
                f"Required dependency not found: {dependency}",
                details
            )
        except Exception as e:
            self.error_handler.handle_dependency_error_notification_error(e)
    
    def _format_message(self, message: str, details: Optional[str] = None) -> str:
        """Format a notification message with optional details."""
        if details:
            return f"{message}\n\n{details}"
        return message
    
    def show_custom_notification(self, 
                               notification_type: NotificationType,
                               title: str, 
                               message: str, 
                               details: Optional[str] = None) -> Optional[bool]:
        """Show a custom notification of the specified type."""
        try:
            if notification_type == NotificationType.INFO:
                self.show_info(title, message, details)
                return None
            elif notification_type == NotificationType.SUCCESS:
                self.show_success(title, message, details)
                return None
            elif notification_type == NotificationType.WARNING:
                self.show_warning(title, message, details)
                return None
            elif notification_type == NotificationType.ERROR:
                self.show_error(title, message, details)
                return None
            elif notification_type == NotificationType.QUESTION:
                return self.ask_question(title, message, details)
            else:
                self.show_info(title, message, details)
                return None
                
        except Exception as e:
            self.error_handler.handle_custom_notification_error(e)