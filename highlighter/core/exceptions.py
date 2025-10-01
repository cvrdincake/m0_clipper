"""
Core error handling and exception framework for M0 Clipper.
Provides centralized error management, recovery strategies, and user-friendly error reporting.
"""

from typing import Optional, Dict, Any, Callable, Type
from dataclasses import dataclass
from enum import Enum
import traceback
import logging


class ErrorSeverity(Enum):
    """Error severity levels for classification and handling."""
    LOW = "low"           # Non-critical issues that don't affect core functionality
    MEDIUM = "medium"     # Issues that affect some functionality but allow continuation
    HIGH = "high"         # Critical issues that require immediate attention
    CRITICAL = "critical" # Fatal errors that require application termination


class ErrorCategory(Enum):
    """Categories of errors for better classification and handling."""
    USER_INPUT = "user_input"       # Invalid user input or configuration
    FILE_SYSTEM = "file_system"     # File I/O operations, permissions, paths
    AUDIO_PROCESSING = "audio"      # Audio analysis and processing errors
    VIDEO_PROCESSING = "video"      # Video manipulation and FFmpeg errors
    NETWORK = "network"             # Network connectivity and external services
    SYSTEM = "system"               # System resources, memory, CPU
    CONFIGURATION = "configuration" # Application settings and environment
    DEPENDENCY = "dependency"       # External library or tool issues
    INTERNAL = "internal"           # Internal application logic errors


@dataclass
class ErrorContext:
    """Context information for error incidents."""
    error_id: str
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    user_message: str
    technical_details: Optional[str] = None
    suggested_actions: Optional[list] = None
    recoverable: bool = True
    metadata: Optional[Dict[str, Any]] = None


class M0ClipperException(Exception):
    """Base exception class for all M0 Clipper errors."""
    
    def __init__(
        self,
        message: str,
        category: ErrorCategory = ErrorCategory.INTERNAL,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        user_message: Optional[str] = None,
        technical_details: Optional[str] = None,
        suggested_actions: Optional[list] = None,
        recoverable: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.category = category
        self.severity = severity
        self.user_message = user_message or self._generate_user_message()
        self.technical_details = technical_details
        self.suggested_actions = suggested_actions or []
        self.recoverable = recoverable
        self.metadata = metadata or {}
        
    def _generate_user_message(self) -> str:
        """Generate user-friendly message based on category."""
        messages = {
            ErrorCategory.USER_INPUT: "Please check your input and try again.",
            ErrorCategory.FILE_SYSTEM: "There was a problem accessing the file or directory.",
            ErrorCategory.AUDIO_PROCESSING: "An error occurred while processing the audio.",
            ErrorCategory.VIDEO_PROCESSING: "An error occurred while processing the video.",
            ErrorCategory.NETWORK: "A network error occurred. Please check your internet connection.",
            ErrorCategory.SYSTEM: "A system resource error occurred.",
            ErrorCategory.CONFIGURATION: "There's an issue with the application configuration.",
            ErrorCategory.DEPENDENCY: "A required component is missing or not working properly.",
            ErrorCategory.INTERNAL: "An internal error occurred. Please try again."
        }
        return messages.get(self.category, "An unexpected error occurred.")


class ValidationError(M0ClipperException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field: str = None, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.USER_INPUT,
            severity=ErrorSeverity.LOW,
            **kwargs
        )
        if field:
            self.metadata['field'] = field


class FileSystemError(M0ClipperException):
    """Raised for file system related errors."""
    
    def __init__(self, message: str, path: str = None, **kwargs):
        super().__init__(
            message,
            category=ErrorCategory.FILE_SYSTEM,
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )
        if path:
            self.metadata['path'] = path


class AudioProcessingError(M0ClipperException):
    """Raised for audio processing errors."""
    
    def __init__(self, message: str, **kwargs):
        kwargs.setdefault('category', ErrorCategory.AUDIO_PROCESSING)
        kwargs.setdefault('severity', ErrorSeverity.HIGH)
        super().__init__(message, **kwargs)


class VideoProcessingError(M0ClipperException):
    """Raised for video processing errors (FFmpeg, etc.)."""
    
    def __init__(self, message: str, **kwargs):
        kwargs.setdefault('category', ErrorCategory.VIDEO_PROCESSING)
        kwargs.setdefault('severity', ErrorSeverity.HIGH)
        super().__init__(message, **kwargs)


class DependencyError(M0ClipperException):
    """Raised when external dependencies are missing or broken."""
    
    def __init__(self, message: str, dependency: str = None, **kwargs):
        kwargs.setdefault('category', ErrorCategory.DEPENDENCY)
        kwargs.setdefault('severity', ErrorSeverity.HIGH)
        kwargs.setdefault('recoverable', False)
        super().__init__(message, **kwargs)
        if dependency:
            self.metadata['dependency'] = dependency


class ConfigurationError(M0ClipperException):
    """Raised for configuration and environment errors."""
    
    def __init__(self, message: str, **kwargs):
        kwargs.setdefault('category', ErrorCategory.CONFIGURATION)
        kwargs.setdefault('severity', ErrorSeverity.MEDIUM)
        super().__init__(message, **kwargs)


class NetworkError(M0ClipperException):
    """Raised for network-related errors."""
    
    def __init__(self, message: str, **kwargs):
        kwargs.setdefault('category', ErrorCategory.NETWORK)
        kwargs.setdefault('severity', ErrorSeverity.MEDIUM)
        super().__init__(message, **kwargs)


class SystemResourceError(M0ClipperException):
    """Raised when system resources are insufficient."""
    
    def __init__(self, message: str, **kwargs):
        kwargs.setdefault('category', ErrorCategory.SYSTEM)
        kwargs.setdefault('severity', ErrorSeverity.HIGH)
        super().__init__(message, **kwargs)


# Error handler registry for custom handling strategies
ErrorHandler = Callable[[M0ClipperException], Optional[Any]]
_error_handlers: Dict[Type[M0ClipperException], ErrorHandler] = {}


def register_error_handler(exception_type: Type[M0ClipperException], handler: ErrorHandler):
    """Register a custom error handler for specific exception types."""
    _error_handlers[exception_type] = handler


def handle_error(exception: M0ClipperException) -> Optional[Any]:
    """Handle an error using registered handlers or default behavior."""
    # Try specific handler first
    handler = _error_handlers.get(type(exception))
    if handler:
        return handler(exception)
    
    # Try base class handlers
    for exc_type, handler in _error_handlers.items():
        if isinstance(exception, exc_type):
            return handler(exception)
    
    # Default handling
    logging.error(f"Unhandled {exception.__class__.__name__}: {exception}")
    return None


def create_error_context(exception: Exception, error_id: str = None) -> ErrorContext:
    """Create an ErrorContext from any exception."""
    import uuid
    
    if isinstance(exception, M0ClipperException):
        return ErrorContext(
            error_id=error_id or str(uuid.uuid4())[:8],
            category=exception.category,
            severity=exception.severity,
            message=str(exception),
            user_message=exception.user_message,
            technical_details=exception.technical_details,
            suggested_actions=exception.suggested_actions,
            recoverable=exception.recoverable,
            metadata=exception.metadata
        )
    else:
        # Convert standard exceptions to our format
        return ErrorContext(
            error_id=error_id or str(uuid.uuid4())[:8],
            category=ErrorCategory.INTERNAL,
            severity=ErrorSeverity.MEDIUM,
            message=str(exception),
            user_message="An unexpected error occurred. Please try again.",
            technical_details=traceback.format_exc(),
            recoverable=True
        )