import datetime
import subprocess
import numpy as np
import time
import json
import os
import asyncio
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Dict, Optional, Callable, Generator
from pathlib import Path

from rich.progress import Progress
from rich.panel import Panel

from loguru import logger

from . import processor, common, console
from .animations import CyberLoadingAnimation, create_clip_processing_animation

@dataclass
class BatchJob:
    """Represents a single video processing job in a batch."""
    video_path: str
    output_path: str
    decibel_threshold: float = -5.0
    clip_length: int = 30
    use_streaming: bool = True
    progress_callback: Optional[Callable] = None
    job_id: Optional[str] = None
    
    def __post_init__(self):
        if self.job_id is None:
            self.job_id = common.unique_id()


class BatchProcessor:
    """Handles batch processing of multiple videos with parallel execution."""
    
    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers
        self.active_jobs: Dict[str, BatchJob] = {}
        self.completed_jobs: Dict[str, dict] = {}
        self.failed_jobs: Dict[str, str] = {}
        
    def add_job(self, job: BatchJob) -> str:
        """Add a job to the processing queue."""
        self.active_jobs[job.job_id] = job
        logger.info(f"Added batch job {job.job_id}: {os.path.basename(job.video_path)}")
        return job.job_id
    
    def process_batch(self, jobs: List[BatchJob], progress_callback: Optional[Callable] = None) -> Dict[str, dict]:
        """Process multiple videos concurrently."""
        logger.info(f"Starting batch processing of {len(jobs)} videos with {self.max_workers} workers")
        
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            future_to_job = {
                executor.submit(self._process_single_video, job): job 
                for job in jobs
            }
            
            # Process completed jobs as they finish
            completed_count = 0
            for future in as_completed(future_to_job):
                job = future_to_job[future]
                completed_count += 1
                
                try:
                    result = future.result()
                    results[job.job_id] = {
                        'status': 'completed',
                        'video_path': job.video_path,
                        'result': result,
                        'highlights_generated': result.get('highlights_generated', 0)
                    }
                    self.completed_jobs[job.job_id] = results[job.job_id]
                    logger.info(f"Completed job {job.job_id} ({completed_count}/{len(jobs)})")
                    
                except Exception as e:
                    error_msg = str(e)
                    results[job.job_id] = {
                        'status': 'failed',
                        'video_path': job.video_path,
                        'error': error_msg
                    }
                    self.failed_jobs[job.job_id] = error_msg
                    logger.error(f"Failed job {job.job_id}: {error_msg}")
                
                # Call progress callback if provided
                if progress_callback:
                    progress_callback(completed_count, len(jobs), job.job_id, results[job.job_id])
                
                # Clean up active job
                if job.job_id in self.active_jobs:
                    del self.active_jobs[job.job_id]
        
        logger.info(f"Batch processing completed: {len(self.completed_jobs)} successful, {len(self.failed_jobs)} failed")
        return results
    
    def _process_single_video(self, job: BatchJob) -> dict:
        """Process a single video job."""
        try:
            # Create output directory
            output_path = Path(job.output_path)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Extract audio
            temp_audio = processor.extract_audio_from_video(job.video_path, str(output_path))
            
            # Create analyzer with streaming or legacy processor
            if job.use_streaming:
                audio_processor = processor.StreamingAudioProcessor(temp_audio)
                analyzer = StreamingAudioAnalysis(
                    video_path=job.video_path,
                    audio_processor=audio_processor,
                    output_path=job.output_path,
                    decibel_threshold=job.decibel_threshold
                )
            else:
                audio_processor = processor.AudioProcessor(temp_audio)
                analyzer = AudioAnalysis(
                    video_path=job.video_path,
                    audio_path=temp_audio,
                    output_path=job.output_path,
                    decibel_threshold=job.decibel_threshold
                )
            
            # Set clip length
            analyzer.start_point = job.clip_length // 2
            analyzer.end_point = job.clip_length - analyzer.start_point
            
            # Run analysis
            if job.use_streaming:
                analyzer.streaming_crest_ceiling_algorithm()
            else:
                analyzer.crest_ceiling_algorithm()
            
            # Export results
            analyzer.export()
            
            # Generate clips
            completed_count, failed_count = analyzer.generate_all_highlights()
            
            return {
                'highlights_found': len(analyzer._captured_result),
                'highlights_generated': completed_count,
                'highlights_failed': failed_count,
                'output_path': job.output_path,
                'processing_time': time.time()
            }
            
        except Exception as e:
            logger.error(f"Error processing video {job.video_path}: {e}")
            raise


class StreamingAudioAnalysis:
    """Memory-efficient audio analysis using streaming processing."""
    
    def __init__(self, video_path: str, audio_processor, output_path: str, decibel_threshold=-5.0):
        self.video_path = video_path
        self.audio_processor = audio_processor
        self.output_path = output_path
        self.decibel_threshold = decibel_threshold
        
        self.start_point = 20
        self.end_point = 20
        
        # Internal use
        self._captured_result = {}
        self._subprocesses = []
        
    def _already_captured(self, pos: int) -> bool:
        """Check if this position would overlap with existing clips."""
        min_gap = max(30, self.start_point + self.end_point)
        
        for existing_pos in self._captured_result.keys():
            if abs(int(existing_pos) - pos) < min_gap:
                return True
        return False
    
    def _add_highlight(self, position: int, decibel: float):
        """Add a highlight to the results."""
        highlight = common.HighlightedMoment(
            position=str(datetime.timedelta(seconds=position)), 
            decibel=decibel
        )
        self._captured_result[position] = highlight
    
    def streaming_crest_ceiling_algorithm(self):
        """Enhanced streaming algorithm with intelligent detection."""
        logger.info("Starting streaming audio analysis...")
        
        # Enhanced parameters
        sustained_threshold_duration = 3
        rolling_window = []
        rolling_window_size = 5
        
        t0 = time.time()
        total_duration = self.audio_processor.duration
        processed_duration = 0.0
        
        with AudioAnalysisProgress(console=console, transient=True, refresh_per_second=30) as progress:
            task = progress.add_task('[dim]streaming analysis...', total=total_duration)
            
            for decibel_data, position in self.audio_processor.decibel_iter():
                if not decibel_data:
                    continue
                    
                max_decibel = max(decibel_data) if decibel_data else -60.0
                avg_decibel = sum(decibel_data) / len(decibel_data) if decibel_data else -60.0
                
                # Update rolling window
                rolling_window.append({
                    'position': position,
                    'max_db': max_decibel,
                    'avg_db': avg_decibel
                })
                
                if len(rolling_window) > rolling_window_size:
                    rolling_window.pop(0)
                
                # Enhanced detection logic
                if max_decibel >= self.decibel_threshold:
                    if not self._already_captured(int(position)):
                        # Check for sustained loud moments
                        sustained_count = sum(1 for w in rolling_window if w['max_db'] >= self.decibel_threshold)
                        
                        highlight_detected = False
                        
                        if sustained_count >= sustained_threshold_duration:
                            # Strong highlight: sustained loud moment
                            self._add_highlight(int(position), max_decibel)
                            highlight_detected = True
                            logger.debug(f"Sustained highlight at {position}s: {max_decibel:.1f}dB")
                        elif max_decibel >= (self.decibel_threshold + 3):
                            # Spike highlight: very loud brief moment
                            self._add_highlight(int(position), max_decibel)
                            highlight_detected = True
                            logger.debug(f"Spike highlight at {position}s: {max_decibel:.1f}dB")
                        elif len(rolling_window) >= 3:
                            # Dynamic highlight: above rolling average
                            rolling_avg = sum(w['avg_db'] for w in rolling_window) / len(rolling_window)
                            if max_decibel >= (rolling_avg + 6):
                                self._add_highlight(int(position), max_decibel)
                                highlight_detected = True
                                logger.debug(f"Dynamic highlight at {position}s: {max_decibel:.1f}dB")
                        
                        if highlight_detected:
                            progress.update(task, description=f'[dim]captured[/] [yellow bold]{len(self._captured_result)}[/] [dim]highlights so far...')
                
                # Update progress
                processed_duration = position
                progress.update(task, completed=min(processed_duration, total_duration))
                
                # Log memory usage periodically
                if int(position) % 60 == 0:  # Every minute
                    memory_mb = self.audio_processor.get_memory_usage()
                    logger.debug(f"Memory usage at {position}s: {memory_mb:.1f} MB")
            
            progress.update(task, completed=total_duration)
        
        t1 = time.time()
        memory_mb = self.audio_processor.get_memory_usage()
        logger.info(f'streaming analysis completed in {t1 - t0:.1f}s with {len(self._captured_result)} highlights')
        logger.info(f'peak memory usage: {memory_mb:.1f} MB')
    
    def export(self):
        """Export analysis results to JSON."""
        filename = os.path.join(self.output_path, 'index.json')
        with open(filename, 'w') as f:
            json.dump(self._captured_result, f, indent=4, default=common.json_encoder)
        logger.info(f'exported to {filename}')
    
    def generate_all_highlights(self):
        """Generate all highlight clips using optimized parallel processing."""
        highlights = list(self._captured_result.keys())
        
        if not highlights:
            logger.warning("No highlights found to generate clips")
            return 0, 0
        
        logger.info(f"Starting parallel generation of {len(highlights)} highlight clips")
        
        # Use optimized parallel clip generation
        clip_generator = OptimizedClipGenerator(max_workers=4)
        completed_count, failed_count = clip_generator.generate_clips_parallel(
            self._captured_result,
            self.video_path,
            self.output_path,
            self.start_point,
            self.end_point
        )
        
        logger.info(f"Clip generation completed: {completed_count} successful, {failed_count} failed")
        return completed_count, failed_count


class OptimizedClipGenerator:
    """Optimized parallel clip generation with better resource management and futuristic UI."""
    
    def __init__(self, max_workers: int = 4, use_animations: bool = True):
        self.max_workers = max_workers
        self.use_animations = use_animations
        self._animation = None
        
    def generate_clips_parallel(self, highlights: dict, video_path: str, output_path: str, 
                               start_point: int, end_point: int) -> tuple:
        """Generate multiple clips in parallel with progress tracking and animations."""
        
        total_clips = len(highlights)
        
        # Start futuristic animation if enabled
        if self.use_animations:
            self._animation = create_clip_processing_animation()
            self._animation.start_clip_processing_animation(total_clips)
            # Brief initialization phase
            self._animation.update_progress(0, "initializing")
            time.sleep(0.5)
            self._animation.update_progress(0, "generating")
        
        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all clip generation tasks
                future_to_position = {}
                
                for position, highlight in highlights.items():
                    future = executor.submit(
                        self._generate_single_clip,
                        video_path, position, highlight, output_path, start_point, end_point
                    )
                    future_to_position[future] = position
                
                # Wait for completion with progress tracking
                completed_count = 0
                failed_count = 0
                
                for future in as_completed(future_to_position, timeout=600):  # 10 minute timeout
                    position = future_to_position[future]
                    
                    try:
                        result = future.result(timeout=60)  # 1 minute per clip timeout
                        if result:
                            completed_count += 1
                            logger.debug(f"Generated clip for position {position}s")
                        else:
                            failed_count += 1
                            logger.warning(f"Failed to generate clip for position {position}s")
                            
                    except concurrent.futures.TimeoutError:
                        failed_count += 1
                        logger.error(f"Timeout generating clip for position {position}s")
                        
                    except Exception as e:
                        failed_count += 1
                        logger.error(f"Error generating clip for position {position}s: {e}")
                    
                    # Update animation progress
                    if self.use_animations and self._animation:
                        total_processed = completed_count + failed_count
                        if total_processed >= total_clips * 0.9:  # 90% complete
                            self._animation.update_progress(total_processed, "finalizing")
                        else:
                            self._animation.update_progress(total_processed, "generating")
                    
                    # Log progress periodically
                    total_processed = completed_count + failed_count
                    if total_processed % 5 == 0 or total_processed == len(highlights):
                        logger.info(f"Clip generation progress: {total_processed}/{len(highlights)} ({completed_count} successful, {failed_count} failed)")
            
            # Stop animation with success/failure message
            if self.use_animations and self._animation:
                if failed_count == 0:
                    success_msg = f"All {completed_count} clips forged successfully! Your highlight arsenal is ready!"
                    self._animation.stop_animation(success=True, final_message=success_msg)
                elif completed_count > 0:
                    partial_msg = f"Partial success: {completed_count} clips created, {failed_count} failed. Check logs for details."
                    self._animation.stop_animation(success=True, final_message=partial_msg)
                else:
                    error_msg = f"Mission failed: No clips were generated. Check FFmpeg installation and logs."
                    self._animation.stop_animation(success=False, final_message=error_msg)
        
        except Exception as e:
            if self.use_animations and self._animation:
                error_msg = f"Critical error in clip generation system: {str(e)}"
                self._animation.stop_animation(success=False, final_message=error_msg)
            raise
        
        return completed_count, failed_count
    
    def _generate_single_clip(self, video_path: str, position: int, highlight, 
                             output_path: str, start_point: int, end_point: int) -> bool:
        """Generate a single clip with improved error handling."""
        try:
            start = max(0, int(position) - start_point)
            end = int(position) + end_point
            
            # Better naming with timestamp and unique ID
            timestamp = str(datetime.timedelta(seconds=int(position))).replace(':', 'h', 1).replace(':', 'm', 1) + 's'
            decibel_str = f"{highlight.decibel:.1f}dB"
            unique_id = common.unique_id()
            
            output_file = os.path.join(output_path, f'{timestamp}_{decibel_str}_{unique_id}.mp4')
            
            # Optimized FFmpeg command
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-ss', str(start),
                '-to', str(end),
                '-c', 'copy',  # Stream copy for speed
                '-avoid_negative_ts', 'make_zero',
                '-y',  # Overwrite
                '-loglevel', 'error',  # Reduce logging
                output_file
            ]
            
            # Run with timeout and proper error handling
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,  # 1 minute timeout per clip
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            if result.returncode == 0:
                # Verify file was created and has reasonable size
                if os.path.exists(output_file) and os.path.getsize(output_file) > 1024:  # At least 1KB
                    return True
                else:
                    logger.warning(f"Clip generated but file is too small: {output_file}")
                    return False
            else:
                logger.error(f"FFmpeg failed for position {position}: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout generating clip for position {position}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error generating clip for position {position}: {e}")
            return False


class AudioAnalysisProgress(Progress):
    def get_renderables(self):
        yield Panel.fit(self.make_tasks_table(self.tasks))

class AudioAnalysis:
    def __init__(self, video_path: str, audio_path: str, output_path: str, decibel_threshold=-5.0):
        self.video_path = video_path
        self.audio_path = audio_path
        self.output_path = output_path
        self.decibel_threshold = decibel_threshold
        
        self.start_point = 20
        self.end_point = 20
        
        # internal use
        self._processor = processor.AudioProcessor(audio_path)
        self._captured_result = {}
        self._recent = np.array([])
        self._subprocesses = []
    
    def _already_captured(self, pos: int):
        """
        Check if this position would overlap with existing clips.
        Uses dynamic gap calculation based on clip length.
        """
        min_gap = max(30, self.start_point + self.end_point)  # Minimum gap between clips
        
        # Check if any existing highlight is too close
        for existing_pos in self._captured_result.keys():
            if abs(int(existing_pos) - pos) < min_gap:
                return True
        return False
    
    def _add_highlight(self, position: int, decibel: float):
        highlight = common.HighlightedMoment(position=str(datetime.timedelta(seconds=position)), decibel=decibel)
        self._captured_result[position] = highlight
        
    def _add_dynamic_highlight(self, start: int, end: int, decibel: float):
        highlight = common.DynamicHighlightedMoment(start=start, end=end, position=str(datetime.timedelta(seconds=start)), decibel=decibel)
        self._captured_result[start] = highlight
    
    def dynamic_crest_ceiling_algorithm(self):
        data = iter(self._processor.decibel_iter())
        
        t_from = 0
        t_to = 0
        
        t0 = time.time()
        with AudioAnalysisProgress(console=console, transient=True, refresh_per_second=60) as progress:
            task = progress.add_task('[dim]analyzing audio...', total=self._processor.duration)
            
            for point in data:
                decibel_array = point[0]
                position = point[1]
                
                max_decibel = np.max(decibel_array)
                
                if max_decibel >= self.decibel_threshold:
                    if t_from == 0:
                        t_from = position
                    else:
                        t_to = position
                        if not self._already_captured(int(t_from)):
                            self._add_dynamic_highlight(int(t_from), int(t_to), max_decibel)
                            progress.update(task, description=f'[dim]captured[/] [yellow bold]{len(self._captured_result)}[/] [dim]highlights so far ...')
                        t_from = 0
                progress.update(task, advance=1.0)
            progress.update(task, completed=True)
            progress.remove_task(task)
        t1 = time.time()
        logger.info(f'analysis completed in {t1 - t0}s')
                
    
    def crest_ceiling_algorithm(self):
        """
        Enhanced clipping algorithm with better intelligence.
        Features:
        - Prevents overlapping clips
        - Considers sustained loud moments vs brief spikes
        - Uses rolling average for better noise rejection
        """
        data = iter(self._processor.decibel_iter())
        
        # Enhanced parameters for better detection
        min_gap_between_clips = max(30, self.start_point + self.end_point)  # Minimum gap between clips
        sustained_threshold_duration = 3  # Require 3+ seconds above threshold for sustained moments
        rolling_window = []
        rolling_window_size = 5  # 5-second rolling window
        
        t0 = time.time()
        with AudioAnalysisProgress(console=console, transient=True, refresh_per_second=60) as progress:
            task = progress.add_task('[dim]analyzing audio...', total=self._processor.duration)
            
            for point in data:
                decibel_array = point[0]
                position = point[1]
                
                max_decibel = np.max(decibel_array)
                avg_decibel = np.mean(decibel_array)
                
                # Update rolling window
                rolling_window.append({
                    'position': position,
                    'max_db': max_decibel,
                    'avg_db': avg_decibel
                })
                
                # Keep rolling window at specified size
                if len(rolling_window) > rolling_window_size:
                    rolling_window.pop(0)
                
                # Check if current moment exceeds threshold
                if max_decibel >= self.decibel_threshold:
                    if not self._already_captured(int(position)):
                        # Enhanced detection: check for sustained loud moments
                        sustained_count = sum(1 for w in rolling_window if w['max_db'] >= self.decibel_threshold)
                        
                        # Decide highlight strength
                        if sustained_count >= sustained_threshold_duration:
                            # Strong highlight: sustained loud moment
                            self._add_highlight(int(position), max_decibel)
                            logger.debug(f"Strong highlight at {position}s: {max_decibel:.1f}dB (sustained)")
                        elif max_decibel >= (self.decibel_threshold + 3):
                            # Spike highlight: very loud brief moment
                            self._add_highlight(int(position), max_decibel)
                            logger.debug(f"Spike highlight at {position}s: {max_decibel:.1f}dB (spike)")
                        else:
                            # Potential highlight: check if it's significantly above rolling average
                            if len(rolling_window) >= 3:
                                rolling_avg = np.mean([w['avg_db'] for w in rolling_window])
                                if max_decibel >= (rolling_avg + 6):  # 6dB above rolling average
                                    self._add_highlight(int(position), max_decibel)
                                    logger.debug(f"Dynamic highlight at {position}s: {max_decibel:.1f}dB (above rolling avg)")
                        
                        progress.update(task, description=f'[dim]captured[/] [yellow bold]{len(self._captured_result)}[/] [dim]highlights so far ...')
                
                progress.update(task, advance=1.0)
                
            progress.update(task, completed=True)
            progress.remove_task(task)
        t1 = time.time()
        logger.info(f'enhanced analysis completed in {t1 - t0}s with {len(self._captured_result)} highlights')
            
    def export(self):
        filename = os.path.join(self.output_path, 'index.json')
        with open(filename, 'w') as f:
            json.dump(self._captured_result, f, indent=4, default=common.json_encoder)
        logger.info(f'exported to {filename}')
        
    def generate_all_highlights(self):
        highlights = list(self._captured_result.keys())
        
        if not highlights:
            logger.warning("No highlights found to generate clips")
            return 0, 0
            
        logger.info(f"Starting optimized parallel generation of {len(highlights)} highlight clips")
        
        # Use optimized parallel clip generation
        clip_generator = OptimizedClipGenerator(max_workers=4)
        completed_count, failed_count = clip_generator.generate_clips_parallel(
            self._captured_result,
            self.video_path,
            self.output_path,
            self.start_point,
            self.end_point
        )
        
        if failed_count > 0:
            logger.warning(f"Clip generation completed: {completed_count} successful, {failed_count} failed out of {len(highlights)} total")
        else:
            logger.info(f"All {completed_count} clips generated successfully")
        
        return completed_count, failed_count
    
    def generate_from_highlight(self, position):
        highlight = self._captured_result[position]
        point = str(highlight.position).replace(':', ' ')
        
        start = int(position - self.start_point)
        end = int(position + self.end_point)
        
        # Better naming: timestamp + decibel + unique ID
        timestamp = str(datetime.timedelta(seconds=int(position))).replace(':', 'h', 1).replace(':', 'm', 1) + 's'
        decibel_str = f"{highlight.decibel:.1f}dB"
        unique_id = common.unique_id()
        
        output = os.path.join(self.output_path, f'{timestamp}_{decibel_str}_{unique_id}.mp4')
        
        if start < 0:
            start = 0
        
        if end > self._processor.duration:
            end = int(self._processor.duration)
        
        logger.debug(f"Generating clip: {start}s to {end}s -> {os.path.basename(output)}")
        
        # Use proper subprocess with better error handling
        try:
            cmd = [
                'ffmpeg',
                '-i', self.video_path,
                '-ss', str(start),
                '-to', str(end),
                '-c', 'copy',
                '-avoid_negative_ts', 'make_zero',
                '-y',  # Overwrite output files
                output
            ]
            
            p = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            self._subprocesses.append(p)
            
        except Exception as e:
            logger.error(f"Failed to start clip generation for position {position}: {e}")
        