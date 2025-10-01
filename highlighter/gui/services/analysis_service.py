"""
Analysis service for M0 Clipper GUI.

Coordinates analysis workflows and integrates with the existing
processor and analyzer modules while maintaining clean architecture.
"""

import threading
import tempfile
import time
from typing import Optional, Dict, Any, Callable
from pathlib import Path

from ...core import ErrorHandler, AudioProcessingError, VideoProcessingError, ValidationError
from ..state import StateManager
from ... import processor, analyzer


class AnalysisService:
    """
    Professional analysis service that coordinates highlight analysis workflows.
    
    Integrates with existing processor and analyzer modules while providing
    clean separation of concerns and proper error handling.
    """
    
    def __init__(self, state_manager: StateManager):
        """Initialize the analysis service."""
        self.state_manager = state_manager
        self.error_handler = ErrorHandler()
        
        # Analysis state
        self.current_analysis_thread: Optional[threading.Thread] = None
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Callbacks for UI updates
        self.progress_callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
        self.log_callback: Optional[Callable] = None
        
    def set_callbacks(self, 
                      progress_callback: Optional[Callable] = None,
                      status_callback: Optional[Callable] = None,
                      log_callback: Optional[Callable] = None):
        """Set callbacks for UI updates."""
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.log_callback = log_callback
    
    def start_reference_analysis(self) -> bool:
        """Start reference analysis to determine optimal threshold."""
        try:
            if self.state_manager.state.is_analyzing:
                return False
            
            # Validate video file
            video_path = self.state_manager.state.current_video_path
            if not video_path or not Path(video_path).exists():
                raise ValidationError("No valid video file selected")
            
            # Start reference analysis in background thread
            self.current_analysis_thread = threading.Thread(
                target=self._run_reference_analysis,
                args=(video_path,),
                daemon=True
            )
            self.current_analysis_thread.start()
            
            return True
            
        except Exception as e:
            self.error_handler.handle_reference_analysis_start_error(e)
            return False
    
    def start_highlight_analysis(self) -> bool:
        """Start the main highlight analysis workflow."""
        try:
            if self.state_manager.state.is_analyzing:
                return False
            
            # Validate state
            issues = self.state_manager.validate_current_state()
            if issues:
                raise ValidationError(f"State validation failed: {'; '.join(issues)}")
            
            # Update analysis state
            self.state_manager.set_analysis_state(True)
            
            # Start analysis in background thread
            self.current_analysis_thread = threading.Thread(
                target=self._run_highlight_analysis,
                daemon=True
            )
            self.current_analysis_thread.start()
            
            return True
            
        except Exception as e:
            self.error_handler.handle_analysis_start_error(e)
            self.state_manager.set_analysis_state(False)
            return False
    
    def stop_analysis(self):
        """Stop any running analysis."""
        try:
            if self.current_analysis_thread and self.current_analysis_thread.is_alive():
                # Note: Thread stopping would require more sophisticated implementation
                # For now, we just mark the state as not analyzing
                self.state_manager.set_analysis_state(False)
                self._log("Analysis stopped by user")
                
        except Exception as e:
            self.error_handler.handle_analysis_stop_error(e)
    
    def _run_reference_analysis(self, video_path: str):
        """Run reference analysis in background thread."""
        try:
            self._log("Starting reference analysis...")
            self._status("Extracting audio from video...")
            
            # Extract audio
            audio_path = processor.extract_audio_from_video(
                video_path, 
                self.temp_dir.name
            )
            
            self._log("Analyzing audio characteristics...")
            self._status("Analyzing audio characteristics...")
            
            # Use streaming or legacy processor based on setting
            if self.state_manager.state.use_streaming:
                self._log("Using streaming processing (memory efficient)...")
                audio_processor = processor.StreamingAudioProcessor(audio_path)
            else:
                self._log("Using legacy processing (faster but more memory)...")
                audio_processor = processor.AudioProcessor(audio_path)
            
            # Get audio statistics
            avg_db = audio_processor.get_avg_decibel()
            max_db = audio_processor.get_max_decibel()
            
            # Calculate threshold recommendations
            recommended_threshold = avg_db + 5
            conservative_threshold = avg_db + 3
            balanced_threshold = avg_db + 5
            aggressive_threshold = avg_db + 8
            
            # Show results
            self._show_reference_results(
                avg_db, max_db, recommended_threshold,
                conservative_threshold, balanced_threshold, aggressive_threshold
            )
            
            self._log(f"Reference analysis complete. Average: {avg_db:.1f} dB")
            self._status("Reference analysis complete")
            
        except Exception as e:
            self.error_handler.handle_reference_analysis_error(e)
            self._log(f"Reference analysis failed: {str(e)}")
            self._status("Reference analysis failed")
    
    def _run_highlight_analysis(self):
        """Run highlight analysis in background thread."""
        start_time = time.time()
        
        try:
            state = self.state_manager.state
            
            self._log(f"🎬 Video: {Path(state.current_video_path).name}")
            self._log(f"📁 Output: {state.output_directory}")
            self._log(f"🎯 Threshold: {state.decibel_threshold:.1f} dB")
            self._log(f"🔄 Mode: {'Streaming (Memory Efficient)' if state.use_streaming else 'Legacy (Faster)'}")
            
            # Extract audio
            self._log("Extracting audio from video...")
            self._status("Extracting audio...")
            
            audio_path = processor.extract_audio_from_video(
                state.current_video_path,
                self.temp_dir.name
            )
            
            # Create analyzer based on processing mode
            self._log("Initializing analyzer...")
            self._status("Initializing analyzer...")
            
            if state.use_streaming:
                # Use streaming processing
                audio_processor = processor.StreamingAudioProcessor(audio_path)
                audio_analyzer = analyzer.StreamingAudioAnalysis(
                    video_path=state.current_video_path,
                    audio_processor=audio_processor,
                    output_path=state.output_directory,
                    decibel_threshold=state.decibel_threshold
                )
            else:
                # Use legacy processing
                audio_analyzer = analyzer.AudioAnalysis(
                    video_path=state.current_video_path,
                    audio_path=audio_path,
                    output_path=state.output_directory,
                    decibel_threshold=state.decibel_threshold
                )
            
            # Run analysis with progress updates
            self._log("Finding highlights...")
            self._status("Finding highlights...")
            
            results = audio_analyzer.find_highlights(
                clip_length=state.clip_length,
                verbose=state.verbose_logging
            )
            
            # Generate clips
            self._log("Generating highlight clips...")
            self._status("Generating clips...")
            
            clips_generated = audio_analyzer.generate_clips()
            
            # Calculate results
            processing_time = time.time() - start_time
            total_size_mb = self._calculate_total_size(state.output_directory)
            
            # Save results to state
            results_data = {
                "video_path": state.current_video_path,
                "clips_generated": clips_generated,
                "processing_time": processing_time,
                "total_size_mb": total_size_mb,
                "threshold_used": state.decibel_threshold,
                "clip_length": state.clip_length,
                "output_directory": state.output_directory
            }
            
            self.state_manager.save_analysis_results(results_data)
            
            if clips_generated > 0:
                self._log(f"✅ Analysis complete! Generated {clips_generated} highlight clips")
                self._status(f"Complete - {clips_generated} clips generated")
            else:
                self._log("⚠️ No highlights found with current settings")
                self._status("No highlights found")
            
        except Exception as e:
            self.error_handler.handle_highlight_analysis_error(e)
            self._log(f"❌ Analysis failed: {str(e)}")
            self._status("Analysis failed")
        
        finally:
            # Always reset analysis state
            self.state_manager.set_analysis_state(False)
    
    def _calculate_total_size(self, output_dir: str) -> float:
        """Calculate total size of generated clips in MB."""
        try:
            total_size = 0
            output_path = Path(output_dir)
            
            if output_path.exists():
                for file_path in output_path.glob("*.mp4"):
                    total_size += file_path.stat().st_size
            
            return total_size / (1024 * 1024)  # Convert to MB
            
        except Exception:
            return 0.0
    
    def _show_reference_results(self, avg_db, max_db, recommended_threshold,
                               conservative_threshold, balanced_threshold, aggressive_threshold):
        """Show reference analysis results dialog."""
        try:
            from tkinter import messagebox, simpledialog
            
            # Create results message
            message = f"""Reference Analysis Results:

Average Volume: {avg_db:.1f} dB
Maximum Volume: {max_db:.1f} dB

Recommended Thresholds:
• Conservative: {conservative_threshold:.1f} dB (fewer clips)
• Balanced: {balanced_threshold:.1f} dB (recommended)
• Aggressive: {aggressive_threshold:.1f} dB (more clips)

Would you like to use the balanced threshold?"""
            
            # Show dialog
            use_recommended = messagebox.askyesno(
                "Reference Analysis Complete",
                message
            )
            
            if use_recommended:
                self.state_manager.set_analysis_parameters(
                    decibel_threshold=balanced_threshold
                )
                self._log(f"Threshold updated to {balanced_threshold:.1f} dB")
            
        except Exception as e:
            self.error_handler.handle_results_display_error(e)
    
    def _log(self, message: str):
        """Log a message through callback if available."""
        if self.log_callback:
            try:
                self.log_callback(message)
            except Exception:
                pass  # Ignore callback errors
    
    def _status(self, status: str):
        """Update status through callback if available."""
        if self.status_callback:
            try:
                self.status_callback(status)
            except Exception:
                pass  # Ignore callback errors
    
    def _progress(self, value: float, maximum: float = 100.0):
        """Update progress through callback if available."""
        if self.progress_callback:
            try:
                self.progress_callback(value, maximum)
            except Exception:
                pass  # Ignore callback errors
    
    def cleanup(self):
        """Clean up resources."""
        try:
            if self.temp_dir:
                self.temp_dir.cleanup()
        except Exception:
            pass  # Ignore cleanup errors