"""
Centralized logging configuration for M0 Clipper.
Provides consistent, structured logging across all modules.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from loguru import logger as loguru_logger


class M0ClipperLogger:
    """Centralized logger for M0 Clipper with multiple output formats."""
    
    def __init__(self, log_dir: Optional[Path] = None, log_level: str = "INFO"):
        self.log_dir = log_dir or Path.cwd() / "logs"
        self.log_level = log_level.upper()
        self.loggers: Dict[str, logging.Logger] = {}
        self._setup_directories()
        self._setup_loguru()
        
    def _setup_directories(self):
        """Create necessary log directories."""
        self.log_dir.mkdir(exist_ok=True)
        
    def _setup_loguru(self):
        """Configure loguru for structured logging."""
        # Remove default handler
        loguru_logger.remove()
        
        # Console handler with colors
        loguru_logger.add(
            sys.stderr,
            level=self.log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                   "<level>{message}</level>",
            colorize=True
        )
        
        # File handler for all logs
        loguru_logger.add(
            self.log_dir / "m0_clipper.log",
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            rotation="10 MB",
            retention="1 month",
            compression="zip"
        )
        
        # Error-only file handler
        loguru_logger.add(
            self.log_dir / "errors.log",
            level="ERROR",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}\n{exception}",
            rotation="5 MB",
            retention="3 months",
            compression="zip"
        )
        
        # Performance log for timing information
        loguru_logger.add(
            self.log_dir / "performance.log",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {message}",
            filter=lambda record: "PERF" in record["extra"],
            rotation="5 MB",
            retention="1 week"
        )
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance for a specific module."""
        if name not in self.loggers:
            # Create standard logging logger that forwards to loguru
            standard_logger = logging.getLogger(name)
            standard_logger.setLevel(getattr(logging, self.log_level))
            
            # Add handler that forwards to loguru
            class LoguruHandler(logging.Handler):
                def emit(self, record):
                    try:
                        level = record.levelname
                        message = record.getMessage()
                        loguru_logger.opt(depth=1).log(level, message)
                    except Exception:
                        self.handleError(record)
            
            if not standard_logger.handlers:
                standard_logger.addHandler(LoguruHandler())
                standard_logger.propagate = False
            
            self.loggers[name] = standard_logger
        
        return self.loggers[name]
    
    def log_performance(self, operation: str, duration: float, metadata: Optional[Dict[str, Any]] = None):
        """Log performance metrics."""
        perf_data = {
            "operation": operation,
            "duration_seconds": duration,
            "timestamp": datetime.now().isoformat()
        }
        if metadata:
            perf_data.update(metadata)
        
        loguru_logger.bind(PERF=True).info(
            f"PERFORMANCE | {operation} | {duration:.3f}s | {metadata or {}}"
        )
    
    def log_user_action(self, action: str, details: Optional[Dict[str, Any]] = None):
        """Log user actions for analytics and debugging."""
        user_data = {
            "action": action,
            "timestamp": datetime.now().isoformat()
        }
        if details:
            user_data.update(details)
        
        loguru_logger.info(f"USER_ACTION | {action} | {details or {}}")
    
    def set_level(self, level: str):
        """Change logging level for all loggers."""
        self.log_level = level.upper()
        
        # Update loguru handlers
        loguru_logger.remove()
        self._setup_loguru()
        
        # Update standard loggers
        for logger_instance in self.loggers.values():
            logger_instance.setLevel(getattr(logging, self.log_level))


# Global logger instance
_global_logger: Optional[M0ClipperLogger] = None


def setup_logging(
    log_dir: Optional[Path] = None, 
    log_level: str = "INFO",
    enable_file_logging: bool = True
) -> M0ClipperLogger:
    """Setup global logging configuration."""
    global _global_logger
    
    if enable_file_logging:
        _global_logger = M0ClipperLogger(log_dir, log_level)
    else:
        # Console-only logging for testing
        loguru_logger.remove()
        loguru_logger.add(
            sys.stderr,
            level=log_level,
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            colorize=True
        )
        _global_logger = M0ClipperLogger(None, log_level)
    
    return _global_logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module."""
    if _global_logger is None:
        setup_logging()
    return _global_logger.get_logger(name)


def log_performance(operation: str, duration: float, metadata: Optional[Dict[str, Any]] = None):
    """Log performance metrics."""
    if _global_logger:
        _global_logger.log_performance(operation, duration, metadata)


def log_user_action(action: str, details: Optional[Dict[str, Any]] = None):
    """Log user actions."""
    if _global_logger:
        _global_logger.log_user_action(action, details)


class PerformanceTimer:
    """Context manager for timing operations."""
    
    def __init__(self, operation_name: str, metadata: Optional[Dict[str, Any]] = None):
        self.operation_name = operation_name
        self.metadata = metadata or {}
        self.start_time = None
        
    def __enter__(self):
        self.start_time = datetime.now()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            
            # Add exception info if one occurred
            if exc_type:
                self.metadata['exception'] = str(exc_val)
                self.metadata['exception_type'] = exc_type.__name__
            
            log_performance(self.operation_name, duration, self.metadata)


# Decorator for automatic performance logging
def log_performance_decorator(operation_name: Optional[str] = None):
    """Decorator to automatically log function performance."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            name = operation_name or f"{func.__module__}.{func.__name__}"
            with PerformanceTimer(name):
                return func(*args, **kwargs)
        return wrapper
    return decorator


# Module-specific logger setup
def setup_module_logger(module_name: str) -> logging.Logger:
    """Setup a logger for a specific module with appropriate configuration."""
    logger = get_logger(module_name)
    
    # Add module-specific configuration if needed
    if module_name.endswith('.gui'):
        # GUI modules might want less verbose logging by default
        logger.setLevel(logging.INFO)
    elif module_name.endswith('.processor'):
        # Processor modules might want detailed logging
        logger.setLevel(logging.DEBUG)
    elif module_name.endswith('.analyzer'):
        # Analyzer modules might want performance logging
        logger.setLevel(logging.DEBUG)
    
    return logger