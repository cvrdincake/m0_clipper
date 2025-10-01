import datetime
import subprocess
import numpy as np
import time
import json
import os

from rich.progress import Progress
from rich.panel import Panel

from loguru import logger

from . import processor, common, console

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
        highlights = self._captured_result.keys()
        
        if not highlights:
            logger.warning("No highlights found to generate clips")
            return
            
        logger.info(f"Starting generation of {len(highlights)} highlight clips")
        
        for h in highlights:
            self.generate_from_highlight(h)
        
        # Wait for all subprocesses to complete
        logger.info("Waiting for clip generation to complete...")
        completed_count = 0
        while self._subprocesses:
            for p in self._subprocesses:
                if p.poll() is not None:
                    self._subprocesses.remove(p)
                    completed_count += 1
                    logger.info(f"Clip {completed_count}/{len(highlights)} completed")
                    break
            # Small delay to prevent busy waiting
            time.sleep(0.1)
            
        logger.info(f"All {len(highlights)} clips generated successfully")
    
    def generate_from_highlight(self, position):
        highlight = self._captured_result[position]
        point = str(highlight.position).replace(':', ' ')
        
        start = int(position - self.start_point)
        end = int(position + self.end_point)
        
        output = os.path.join(self.output_path, f'{common.unique_id()} - {point}.mp4')
        
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
        