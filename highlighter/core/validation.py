"""
Input validation utilities for M0 Clipper.
Provides comprehensive validation for user inputs, file paths, and configuration values.
"""

import os
import re
from pathlib import Path
from typing import Union, List, Optional, Any, Dict
from urllib.parse import urlparse

from .exceptions import ValidationError, FileSystemError


class Validator:
    """Base validator class with common validation methods."""
    
    @staticmethod
    def is_not_empty(value: Any, field_name: str = "value") -> Any:
        """Validate that a value is not empty or None."""
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError(f"{field_name} cannot be empty", field=field_name)
        return value
    
    @staticmethod
    def is_string(value: Any, field_name: str = "value") -> str:
        """Validate that a value is a string."""
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string", field=field_name)
        return value
    
    @staticmethod
    def is_number(value: Any, field_name: str = "value") -> Union[int, float]:
        """Validate that a value is a number."""
        if not isinstance(value, (int, float)):
            try:
                return float(value)
            except (ValueError, TypeError):
                raise ValidationError(f"{field_name} must be a number", field=field_name)
        return value
    
    @staticmethod
    def is_positive(value: Union[int, float], field_name: str = "value") -> Union[int, float]:
        """Validate that a number is positive."""
        if value <= 0:
            raise ValidationError(f"{field_name} must be positive", field=field_name)
        return value
    
    @staticmethod
    def is_in_range(
        value: Union[int, float], 
        min_val: Union[int, float], 
        max_val: Union[int, float], 
        field_name: str = "value"
    ) -> Union[int, float]:
        """Validate that a number is within a specified range."""
        if not (min_val <= value <= max_val):
            raise ValidationError(
                f"{field_name} must be between {min_val} and {max_val}",
                field=field_name
            )
        return value
    
    @staticmethod
    def is_in_choices(value: Any, choices: List[Any], field_name: str = "value") -> Any:
        """Validate that a value is in a list of allowed choices."""
        if value not in choices:
            raise ValidationError(
                f"{field_name} must be one of: {', '.join(map(str, choices))}",
                field=field_name
            )
        return value


class PathValidator(Validator):
    """Validator for file and directory paths."""
    
    SUPPORTED_VIDEO_EXTENSIONS = {
        '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v',
        '.mpg', '.mpeg', '.3gp', '.asf', '.rm', '.rmvb', '.ts', '.mts'
    }
    
    SUPPORTED_AUDIO_EXTENSIONS = {
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'
    }
    
    @classmethod
    def validate_file_path(
        cls, 
        path: Union[str, Path], 
        must_exist: bool = True,
        field_name: str = "file_path"
    ) -> Path:
        """Validate a file path."""
        cls.is_not_empty(path, field_name)
        
        try:
            path_obj = Path(path)
        except Exception as e:
            raise ValidationError(f"Invalid path format: {e}", field=field_name)
        
        if must_exist:
            if not path_obj.exists():
                raise FileSystemError(
                    f"File does not exist: {path}",
                    path=str(path),
                    suggested_actions=[
                        "Check the file path for typos",
                        "Ensure the file hasn't been moved or deleted",
                        "Verify you have read permissions for the file"
                    ]
                )
            
            if not path_obj.is_file():
                raise FileSystemError(
                    f"Path exists but is not a file: {path}",
                    path=str(path)
                )
        
        return path_obj
    
    @classmethod
    def validate_directory_path(
        cls, 
        path: Union[str, Path], 
        must_exist: bool = False,
        create_if_missing: bool = False,
        field_name: str = "directory_path"
    ) -> Path:
        """Validate a directory path."""
        cls.is_not_empty(path, field_name)
        
        try:
            path_obj = Path(path)
        except Exception as e:
            raise ValidationError(f"Invalid path format: {e}", field=field_name)
        
        if path_obj.exists():
            if not path_obj.is_dir():
                raise FileSystemError(
                    f"Path exists but is not a directory: {path}",
                    path=str(path)
                )
        elif must_exist:
            raise FileSystemError(
                f"Directory does not exist: {path}",
                path=str(path),
                suggested_actions=[
                    "Check the directory path for typos",
                    "Create the directory manually",
                    "Use a different output directory"
                ]
            )
        elif create_if_missing:
            try:
                path_obj.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                raise FileSystemError(
                    f"Permission denied creating directory: {path}",
                    path=str(path),
                    suggested_actions=[
                        "Check write permissions for the parent directory",
                        "Run as administrator if necessary",
                        "Choose a different directory"
                    ]
                )
            except Exception as e:
                raise FileSystemError(
                    f"Failed to create directory: {e}",
                    path=str(path)
                )
        
        return path_obj
    
    @classmethod
    def validate_video_file(
        cls, 
        path: Union[str, Path],
        field_name: str = "video_file"
    ) -> Path:
        """Validate a video file path."""
        path_obj = cls.validate_file_path(path, must_exist=True, field_name=field_name)
        
        if path_obj.suffix.lower() not in cls.SUPPORTED_VIDEO_EXTENSIONS:
            raise ValidationError(
                f"Unsupported video format: {path_obj.suffix}",
                field=field_name,
                suggested_actions=[
                    f"Use one of the supported formats: {', '.join(sorted(cls.SUPPORTED_VIDEO_EXTENSIONS))}",
                    "Convert the video to a supported format"
                ]
            )
        
        return path_obj
    
    @classmethod
    def validate_audio_file(
        cls, 
        path: Union[str, Path],
        field_name: str = "audio_file"
    ) -> Path:
        """Validate an audio file path."""
        path_obj = cls.validate_file_path(path, must_exist=True, field_name=field_name)
        
        if path_obj.suffix.lower() not in cls.SUPPORTED_AUDIO_EXTENSIONS:
            raise ValidationError(
                f"Unsupported audio format: {path_obj.suffix}",
                field=field_name,
                suggested_actions=[
                    f"Use one of the supported formats: {', '.join(sorted(cls.SUPPORTED_AUDIO_EXTENSIONS))}",
                    "Convert the audio to a supported format"
                ]
            )
        
        return path_obj


class ConfigValidator(Validator):
    """Validator for configuration and parameter values."""
    
    @classmethod
    def validate_decibel_threshold(
        cls, 
        threshold: Union[int, float],
        field_name: str = "decibel_threshold"
    ) -> float:
        """Validate decibel threshold parameter."""
        threshold = cls.is_number(threshold, field_name)
        
        # Reasonable range for audio decibel thresholds
        if not (-60.0 <= threshold <= 20.0):
            raise ValidationError(
                f"Decibel threshold should be between -60.0 and 20.0 dB",
                field=field_name,
                suggested_actions=[
                    "Use the 'reference' command to analyze your video and get recommended thresholds",
                    "Typical values: -10 dB (balanced), -5 dB (aggressive), -15 dB (conservative)"
                ]
            )
        
        return float(threshold)
    
    @classmethod
    def validate_clip_length(
        cls, 
        length: Union[int, float],
        field_name: str = "clip_length"
    ) -> int:
        """Validate clip length parameter."""
        length = cls.is_number(length, field_name)
        length = cls.is_positive(length, field_name)
        
        # Reasonable range for clip lengths
        if not (5 <= length <= 300):  # 5 seconds to 5 minutes
            raise ValidationError(
                f"Clip length should be between 5 and 300 seconds",
                field=field_name,
                suggested_actions=[
                    "Use 30 seconds for typical gaming highlights",
                    "Use 60-120 seconds for longer narrative moments",
                    "Use 10-15 seconds for quick reaction clips"
                ]
            )
        
        return int(length)
    
    @classmethod
    def validate_worker_count(
        cls, 
        workers: Union[int, float],
        field_name: str = "workers"
    ) -> int:
        """Validate worker count for parallel processing."""
        workers = cls.is_number(workers, field_name)
        workers = cls.is_positive(workers, field_name)
        
        import psutil
        cpu_count = psutil.cpu_count()
        
        if workers > cpu_count * 2:
            raise ValidationError(
                f"Worker count ({workers}) is too high for your system ({cpu_count} CPUs)",
                field=field_name,
                suggested_actions=[
                    f"Use at most {cpu_count} workers for optimal performance",
                    f"Consider {max(1, cpu_count // 2)} for balanced system usage"
                ]
            )
        
        return int(workers)


class NetworkValidator(Validator):
    """Validator for network-related inputs."""
    
    @classmethod
    def validate_url(
        cls, 
        url: str,
        allowed_schemes: Optional[List[str]] = None,
        field_name: str = "url"
    ) -> str:
        """Validate a URL."""
        cls.is_not_empty(url, field_name)
        cls.is_string(url, field_name)
        
        try:
            parsed = urlparse(url)
        except Exception as e:
            raise ValidationError(f"Invalid URL format: {e}", field=field_name)
        
        if not parsed.scheme:
            raise ValidationError("URL must include a scheme (http, https, etc.)", field=field_name)
        
        if allowed_schemes and parsed.scheme not in allowed_schemes:
            raise ValidationError(
                f"URL scheme must be one of: {', '.join(allowed_schemes)}",
                field=field_name
            )
        
        if not parsed.netloc:
            raise ValidationError("URL must include a domain name", field=field_name)
        
        return url


# Convenience functions for common validations
def validate_video_input(video_path: Union[str, Path]) -> Path:
    """Validate video file input."""
    return PathValidator.validate_video_file(video_path)


def validate_output_directory(output_path: Union[str, Path], create: bool = True) -> Path:
    """Validate output directory."""
    return PathValidator.validate_directory_path(
        output_path, 
        create_if_missing=create
    )


def validate_analysis_parameters(
    decibel_threshold: Union[int, float],
    clip_length: Union[int, float],
    workers: Optional[Union[int, float]] = None
) -> Dict[str, Union[int, float]]:
    """Validate analysis parameters."""
    validated = {
        'decibel_threshold': ConfigValidator.validate_decibel_threshold(decibel_threshold),
        'clip_length': ConfigValidator.validate_clip_length(clip_length)
    }
    
    if workers is not None:
        validated['workers'] = ConfigValidator.validate_worker_count(workers)
    
    return validated


def validate_batch_input(
    video_pattern: str,
    output_directory: Union[str, Path],
    **analysis_params
) -> Dict[str, Any]:
    """Validate batch processing inputs."""
    import glob
    
    # Validate pattern produces results
    if not video_pattern.strip():
        raise ValidationError("Video pattern cannot be empty", field="video_pattern")
    
    video_files = glob.glob(video_pattern)
    if not video_files:
        raise ValidationError(
            f"No video files found matching pattern: {video_pattern}",
            field="video_pattern",
            suggested_actions=[
                "Check the glob pattern syntax",
                "Verify files exist in the specified location",
                "Use absolute paths if relative paths aren't working"
            ]
        )
    
    # Validate each found file
    for video_file in video_files[:5]:  # Check first 5 for efficiency
        try:
            PathValidator.validate_video_file(video_file)
        except (ValidationError, FileSystemError) as e:
            raise ValidationError(
                f"Invalid video file in pattern: {video_file} - {e}",
                field="video_pattern"
            )
    
    # Validate output directory
    output_dir = validate_output_directory(output_directory, create=True)
    
    # Validate analysis parameters
    validated_params = validate_analysis_parameters(**analysis_params)
    
    return {
        'video_files': video_files,
        'output_directory': output_dir,
        **validated_params
    }