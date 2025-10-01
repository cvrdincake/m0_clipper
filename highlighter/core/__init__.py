"""
Core infrastructure for M0 Clipper.

This module provides the foundational infrastructure for error handling,
validation, and logging across the M0 Clipper application.
"""

from .exceptions import (
    M0ClipperException,
    ValidationError,
    ConfigurationError,
    AudioProcessingError,
    VideoProcessingError,
    FileSystemError,
    DependencyError,
    NetworkError,
    SystemResourceError
)

from .error_handler import ErrorHandler
from .validation import PathValidator, ConfigValidator
from .logging_config import setup_logging

__all__ = [
    # Exception classes
    "M0ClipperException",
    "ValidationError", 
    "ConfigurationError",
    "AudioProcessingError",
    "VideoProcessingError", 
    "FileSystemError",
    "DependencyError",
    "NetworkError",
    "SystemResourceError",
    # Core services
    "ErrorHandler",
    "PathValidator",
    "ConfigValidator",
    "setup_logging"
]

from .exceptions import (
    M0ClipperException,
    ValidationError,
    FileSystemError,
    AudioProcessingError,
    VideoProcessingError,
    DependencyError,
    ConfigurationError,
    NetworkError,
    SystemResourceError,
    ErrorCategory,
    ErrorSeverity,
    ErrorContext
)

from .error_handler import (
    ErrorHandler,
    RecoveryStrategy,
    get_error_handler,
    handle_error,
    safe_execute
)

from .validation import (
    Validator,
    PathValidator,
    ConfigValidator,
    NetworkValidator,
    validate_video_input,
    validate_output_directory,
    validate_analysis_parameters,
    validate_batch_input
)

__all__ = [
    # Exceptions
    'M0ClipperException',
    'ValidationError',
    'FileSystemError', 
    'AudioProcessingError',
    'VideoProcessingError',
    'DependencyError',
    'ConfigurationError',
    'NetworkError',
    'SystemResourceError',
    'ErrorCategory',
    'ErrorSeverity',
    'ErrorContext',
    
    # Error handling
    'ErrorHandler',
    'RecoveryStrategy',
    'get_error_handler',
    'handle_error',
    'safe_execute',
    
    # Validation
    'Validator',
    'PathValidator',
    'ConfigValidator',
    'NetworkValidator',
    'validate_video_input',
    'validate_output_directory',
    'validate_analysis_parameters',
    'validate_batch_input'
]