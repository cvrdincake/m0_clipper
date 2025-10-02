"""
Application state management for M0 Clipper GUI.

This module provides centralized state management for the application,
implementing the Observer pattern for reactive state updates.
"""

import tkinter as tk
from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass, field
from pathlib import Path
import os

from highlighter.core.exceptions import ValidationError
from highlighter.core.error_handler import ErrorHandler
from highlighter.core.validation import PathValidator


@dataclass
class ApplicationState:
    """Central application state container."""
    
    # Video processing state
    current_video_path: str = ""
    output_directory: str = field(default_factory=lambda: os.path.join(os.getcwd(), "highlights"))
    
    # Analysis parameters
    decibel_threshold: float = -10.0
    clip_length: int = 30
    use_streaming: bool = True
    verbose_logging: bool = False
    
    # Application state
    is_analyzing: bool = False
    is_initialized: bool = False
    
    # UI state
    window_geometry: str = "1000x800"
    window_position: Optional[str] = None
    theme_mode: str = "glassmorphism"
    
    # Analysis results
    last_analysis_results: Optional[Dict[str, Any]] = None
    analysis_history: List[Dict[str, Any]] = field(default_factory=list)


class StateManager:
    """Professional state management with observer pattern and validation."""
    
    def __init__(self):
        self.state = ApplicationState()
        self.observers: Dict[str, List[Callable]] = {}
        self.error_handler = ErrorHandler()
        self.path_validator = PathValidator()
        
    def subscribe(self, event: str, callback: Callable):
        """Subscribe to state change events."""
        if event not in self.observers:
            self.observers[event] = []
        self.observers[event].append(callback)
    
    def unsubscribe(self, event: str, callback: Callable):
        """Unsubscribe from state change events."""
        if event in self.observers and callback in self.observers[event]:
            self.observers[event].remove(callback)
    
    def notify(self, event: str, data: Any = None):
        """Notify all observers of a state change."""
        if event in self.observers:
            for callback in self.observers[event]:
                try:
                    callback(data)
                except Exception as e:
                    self.error_handler.handle_observer_error(e, event, callback)
    
    def set_video_path(self, path: str) -> bool:
        """Set the current video path with validation."""
        try:
            if path and not self.path_validator.validate_video_file(path):
                raise ValidationError(f"Invalid video file: {path}")
            
            old_path = self.state.current_video_path
            self.state.current_video_path = path
            
            self.notify("video_path_changed", {
                "old_path": old_path,
                "new_path": path
            })
            return True
            
        except ValidationError as e:
            self.error_handler.handle_validation_error(e)
            return False
    
    def set_output_directory(self, directory: str) -> bool:
        """Set the output directory with validation."""
        try:
            if directory and not self.path_validator.validate_output_directory(directory):
                raise ValidationError(f"Invalid output directory: {directory}")
            
            old_dir = self.state.output_directory
            self.state.output_directory = directory
            
            self.notify("output_directory_changed", {
                "old_directory": old_dir,
                "new_directory": directory
            })
            return True
            
        except ValidationError as e:
            self.error_handler.handle_validation_error(e)
            return False
    
    def set_analysis_parameters(self, 
                              decibel_threshold: Optional[float] = None,
                              clip_length: Optional[int] = None,
                              use_streaming: Optional[bool] = None,
                              verbose_logging: Optional[bool] = None) -> bool:
        """Set analysis parameters with validation."""
        try:
            changes = {}
            
            if decibel_threshold is not None:
                if not -60 <= decibel_threshold <= 0:
                    raise ValidationError("Decibel threshold must be between -60 and 0")
                changes["decibel_threshold"] = (self.state.decibel_threshold, decibel_threshold)
                self.state.decibel_threshold = decibel_threshold
            
            if clip_length is not None:
                if not 5 <= clip_length <= 300:
                    raise ValidationError("Clip length must be between 5 and 300 seconds")
                changes["clip_length"] = (self.state.clip_length, clip_length)
                self.state.clip_length = clip_length
            
            if use_streaming is not None:
                changes["use_streaming"] = (self.state.use_streaming, use_streaming)
                self.state.use_streaming = use_streaming
            
            if verbose_logging is not None:
                changes["verbose_logging"] = (self.state.verbose_logging, verbose_logging)
                self.state.verbose_logging = verbose_logging
            
            if changes:
                self.notify("analysis_parameters_changed", changes)
            
            return True
            
        except ValidationError as e:
            self.error_handler.handle_validation_error(e)
            return False
    
    def set_analysis_state(self, is_analyzing: bool):
        """Set the analysis state."""
        if self.state.is_analyzing != is_analyzing:
            old_state = self.state.is_analyzing
            self.state.is_analyzing = is_analyzing
            
            self.notify("analysis_state_changed", {
                "old_state": old_state,
                "new_state": is_analyzing
            })
    
    def save_analysis_results(self, results: Dict[str, Any]):
        """Save analysis results to state and history."""
        self.state.last_analysis_results = results
        self.state.analysis_history.append({
            **results,
            "timestamp": Path(results.get("video_path", "")).name if results.get("video_path") else "unknown"
        })
        
        # Limit history size
        if len(self.state.analysis_history) > 10:
            self.state.analysis_history = self.state.analysis_history[-10:]
        
        self.notify("analysis_results_saved", results)
    
    def get_state(self) -> ApplicationState:
        """Get the current application state (read-only access)."""
        return self.state
    
    def validate_current_state(self) -> List[str]:
        """Validate the current state and return any issues."""
        issues = []
        
        if self.state.current_video_path:
            if not Path(self.state.current_video_path).exists():
                issues.append("Selected video file does not exist")
        
        if not Path(self.state.output_directory).exists():
            try:
                Path(self.state.output_directory).mkdir(parents=True, exist_ok=True)
            except Exception:
                issues.append("Cannot create output directory")
        
        return issues
    
    def reset_to_defaults(self):
        """Reset state to default values."""
        old_state = self.state
        self.state = ApplicationState()
        
        self.notify("state_reset", {
            "old_state": old_state,
            "new_state": self.state
        })


# Global state manager instance
_state_manager: Optional[StateManager] = None

def get_state_manager() -> StateManager:
    """Get the global state manager instance."""
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager