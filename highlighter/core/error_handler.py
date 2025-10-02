"""
Centralized error handling and recovery system for M0 Clipper.
Provides consistent error processing, logging, and user feedback.
"""

import logging
import traceback
from typing import Optional, Dict, Any, Callable, List
from dataclasses import dataclass
from pathlib import Path
import uuid

from highlighter.core.exceptions import (
    M0ClipperException, ErrorContext, ErrorSeverity, ErrorCategory,
    create_error_context
)


@dataclass
class RecoveryStrategy:
    """Defines a strategy for recovering from specific types of errors."""
    name: str
    description: str
    action: Callable[[ErrorContext], Optional[Any]]
    applicable_categories: List[ErrorCategory]
    applicable_severities: List[ErrorSeverity]


class ErrorHandler:
    """Centralized error handler for M0 Clipper application."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.error_history: List[ErrorContext] = []
        self.recovery_strategies: List[RecoveryStrategy] = []
        self.error_callbacks: List[Callable[[ErrorContext], None]] = []
        self._setup_default_strategies()
        
    def _setup_default_strategies(self):
        """Set up default error recovery strategies."""
        
        # File not found recovery
        def file_not_found_recovery(context: ErrorContext) -> Optional[str]:
            """Suggest alternative file paths or locations."""
            if 'path' in context.metadata:
                path = Path(context.metadata['path'])
                # Look for similar files in the same directory
                if path.parent.exists():
                    similar_files = [
                        f for f in path.parent.iterdir()
                        if f.is_file() and f.suffix == path.suffix
                    ]
                    if similar_files:
                        context.suggested_actions.append(
                            f"Found {len(similar_files)} similar files in the same directory"
                        )
                        return str(similar_files[0])  # Return first match
            return None
        
        self.add_recovery_strategy(RecoveryStrategy(
            name="file_not_found_recovery",
            description="Find alternative files when target file is missing",
            action=file_not_found_recovery,
            applicable_categories=[ErrorCategory.FILE_SYSTEM],
            applicable_severities=[ErrorSeverity.LOW, ErrorSeverity.MEDIUM]
        ))
        
        # FFmpeg path recovery
        def ffmpeg_recovery(context: ErrorContext) -> Optional[str]:
            """Try to locate FFmpeg in common locations."""
            import shutil
            ffmpeg_path = shutil.which('ffmpeg')
            if ffmpeg_path:
                context.suggested_actions.append(
                    f"FFmpeg found at: {ffmpeg_path}"
                )
                return ffmpeg_path
            else:
                context.suggested_actions.extend([
                    "Install FFmpeg from https://ffmpeg.org",
                    "Add FFmpeg to your system PATH",
                    "On Windows: Use 'choco install ffmpeg'",
                    "On macOS: Use 'brew install ffmpeg'",
                    "On Linux: Use 'sudo apt install ffmpeg'"
                ])
            return None
        
        self.add_recovery_strategy(RecoveryStrategy(
            name="ffmpeg_recovery",
            description="Locate or provide installation guidance for FFmpeg",
            action=ffmpeg_recovery,
            applicable_categories=[ErrorCategory.DEPENDENCY],
            applicable_severities=[ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]
        ))
        
        # Memory cleanup recovery
        def memory_recovery(context: ErrorContext) -> Optional[bool]:
            """Attempt to free up memory resources."""
            import gc
            gc.collect()  # Force garbage collection
            context.suggested_actions.append("Freed up memory resources")
            return True
        
        self.add_recovery_strategy(RecoveryStrategy(
            name="memory_recovery",
            description="Clean up memory resources",
            action=memory_recovery,
            applicable_categories=[ErrorCategory.SYSTEM],
            applicable_severities=[ErrorSeverity.MEDIUM, ErrorSeverity.HIGH]
        ))
    
    def add_recovery_strategy(self, strategy: RecoveryStrategy):
        """Add a new recovery strategy."""
        self.recovery_strategies.append(strategy)
        self.logger.debug(f"Added recovery strategy: {strategy.name}")
    
    def add_error_callback(self, callback: Callable[[ErrorContext], None]):
        """Add a callback to be notified of all errors."""
        self.error_callbacks.append(callback)
    
    def handle_exception(
        self,
        exception: Exception,
        context_data: Optional[Dict[str, Any]] = None,
        attempt_recovery: bool = True
    ) -> ErrorContext:
        """
        Handle any exception with optional recovery attempts.
        
        Args:
            exception: The exception to handle
            context_data: Additional context information
            attempt_recovery: Whether to attempt automatic recovery
            
        Returns:
            ErrorContext with handling results
        """
        # Create error context
        error_context = create_error_context(exception)
        if context_data:
            error_context.metadata.update(context_data)
        
        # Log the error
        self._log_error(error_context, exception)
        
        # Add to history
        self.error_history.append(error_context)
        
        # Attempt recovery if enabled and error is recoverable
        if attempt_recovery and error_context.recoverable:
            recovery_result = self._attempt_recovery(error_context)
            if recovery_result:
                error_context.metadata['recovery_attempted'] = True
                error_context.metadata['recovery_result'] = recovery_result
        
        # Notify callbacks
        for callback in self.error_callbacks:
            try:
                callback(error_context)
            except Exception as e:
                self.logger.error(f"Error in error callback: {e}")
        
        return error_context
    
    def _log_error(self, context: ErrorContext, exception: Exception):
        """Log error with appropriate level based on severity."""
        log_message = f"[{context.error_id}] {context.message}"
        
        if context.severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message, exc_info=exception)
        elif context.severity == ErrorSeverity.HIGH:
            self.logger.error(log_message, exc_info=exception)
        elif context.severity == ErrorSeverity.MEDIUM:
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
        
        if context.technical_details:
            self.logger.debug(f"Technical details: {context.technical_details}")
    
    def _attempt_recovery(self, context: ErrorContext) -> Optional[Any]:
        """Attempt to recover from an error using available strategies."""
        applicable_strategies = [
            strategy for strategy in self.recovery_strategies
            if (context.category in strategy.applicable_categories and
                context.severity in strategy.applicable_severities)
        ]
        
        for strategy in applicable_strategies:
            try:
                self.logger.debug(f"Attempting recovery strategy: {strategy.name}")
                result = strategy.action(context)
                if result is not None:
                    self.logger.info(f"Recovery successful with strategy: {strategy.name}")
                    return result
            except Exception as e:
                self.logger.warning(f"Recovery strategy {strategy.name} failed: {e}")
        
        return None
    
    def get_user_friendly_message(self, error_context: ErrorContext) -> str:
        """Generate a comprehensive user-friendly error message."""
        message_parts = [error_context.user_message]
        
        if error_context.suggested_actions:
            message_parts.append("\nSuggested actions:")
            for i, action in enumerate(error_context.suggested_actions, 1):
                message_parts.append(f"  {i}. {action}")
        
        if error_context.error_id:
            message_parts.append(f"\nError ID: {error_context.error_id}")
        
        return "\n".join(message_parts)
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get statistics about handled errors."""
        if not self.error_history:
            return {"total_errors": 0}
        
        total_errors = len(self.error_history)
        by_category = {}
        by_severity = {}
        recoverable_count = 0
        
        for error in self.error_history:
            # Count by category
            category = error.category.value
            by_category[category] = by_category.get(category, 0) + 1
            
            # Count by severity
            severity = error.severity.value
            by_severity[severity] = by_severity.get(severity, 0) + 1
            
            # Count recoverable
            if error.recoverable:
                recoverable_count += 1
        
        return {
            "total_errors": total_errors,
            "by_category": by_category,
            "by_severity": by_severity,
            "recoverable_percentage": (recoverable_count / total_errors) * 100,
            "most_common_category": max(by_category.items(), key=lambda x: x[1])[0] if by_category else None,
            "most_common_severity": max(by_severity.items(), key=lambda x: x[1])[0] if by_severity else None
        }
    
    def clear_error_history(self):
        """Clear the error history (useful for testing or cleanup)."""
        self.error_history.clear()
        self.logger.debug("Error history cleared")


# Global error handler instance
_global_error_handler: Optional[ErrorHandler] = None


def get_error_handler() -> ErrorHandler:
    """Get the global error handler instance."""
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = ErrorHandler()
    return _global_error_handler


def handle_error(
    exception: Exception,
    context_data: Optional[Dict[str, Any]] = None,
    attempt_recovery: bool = True
) -> ErrorContext:
    """Convenience function to handle errors using the global handler."""
    return get_error_handler().handle_exception(exception, context_data, attempt_recovery)


def safe_execute(
    func: Callable,
    *args,
    default_return: Any = None,
    context_data: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Any:
    """
    Safely execute a function with automatic error handling.
    
    Args:
        func: Function to execute
        *args: Arguments for the function
        default_return: Value to return if function fails
        context_data: Additional context for error handling
        **kwargs: Keyword arguments for the function
        
    Returns:
        Function result or default_return if error occurs
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        context = context_data or {}
        context.update({
            'function_name': func.__name__,
            'args': str(args)[:100],  # Limit length
            'kwargs': str(kwargs)[:100]
        })
        handle_error(e, context)
        return default_return