"""
Core infrastructure for M0 Clipper.

This module provides the foundational infrastructure for error handling,
validation, and logging across the M0 Clipper application.
"""

from highlighter.core.exceptions import (
    M0ClipperException,
    ValidationError,
    ConfigurationError,
    AudioProcessingError,
    VideoProcessingError,
    FileSystemError,
    DependencyError,
    NetworkError,
    SystemResourceError,
    ErrorCategory,
    ErrorSeverity,
    ErrorContext
)

from highlighter.core.error_handler import (
    ErrorHandler,
    RecoveryStrategy,
    get_error_handler,
    handle_error,
    safe_execute
)

from highlighter.core.validation import (
    Validator,
    PathValidator,
    ConfigValidator,
    NetworkValidator,
    validate_video_input,
    validate_output_directory,
    validate_analysis_parameters,
    validate_batch_input
)

from highlighter.core.logging_config import setup_logging


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
    "ErrorCategory",
    "ErrorSeverity",
    "ErrorContext",

    # Core services & error handling
    "ErrorHandler",
    "RecoveryStrategy",
    "get_error_handler",
    "handle_error",
    "safe_execute",

    # Validation
    "Validator",
    "PathValidator",
    "ConfigValidator",
    "NetworkValidator",
    "validate_video_input",
    "validate_output_directory",
    "validate_analysis_parameters",
    "validate_batch_input",
    
    # Logging
    "setup_logging"
]
