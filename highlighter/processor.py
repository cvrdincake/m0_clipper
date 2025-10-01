import os
import librosa
import numpy as np
import subprocess
import sys
import psutil
from typing import Generator, Tuple, Optional

from loguru import logger

# Try to import ffmpeg-python, fall back to subprocess if not available
try:
    import ffmpeg
    FFMPEG_PYTHON_AVAILABLE = True
except ImportError:
    FFMPEG_PYTHON_AVAILABLE = False
    logger.warning("ffmpeg-python not available, falling back to subprocess")

BITRATE = '160k'
SAMPLING_RATE = 48000
CHANNELS = 1 # 1 = mono, 2 = stereo
SPLIT_FRAMES = 1000

def extract_audio_from_video(video_path: str, output_path: str):
    """Convert a video file to an audio file.

    Args:
        video_path (str): path to the video file
        output_path (str): path to the output audio file
    """
    file_base = os.path.splitext(os.path.basename(video_path))[0].replace(':', ' ')
    audio_path = os.path.join(output_path, f'{file_base}.wav')
    
    if FFMPEG_PYTHON_AVAILABLE:
        try:
            # Try using ffmpeg-python first
            (
                ffmpeg
                .input(video_path)
                .output(audio_path, **{'ab': BITRATE, 'ar': SAMPLING_RATE, 'ac': CHANNELS})
                .overwrite_output()
                .run(quiet=True, capture_stdout=True)
            )
            logger.info(f'audio extracted from {video_path} to {audio_path} using ffmpeg-python')
            return audio_path
        except Exception as e:
            logger.warning(f'ffmpeg-python failed: {e}, falling back to subprocess')
    
    # Fallback to subprocess
    try:
        cmd = [
            'ffmpeg', '-i', video_path,
            '-ab', BITRATE,
            '-ar', str(SAMPLING_RATE),
            '-ac', str(CHANNELS),
            '-y',  # Overwrite output file
            audio_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(f'audio extracted from {video_path} to {audio_path} using subprocess')
        return audio_path
        
    except subprocess.CalledProcessError as e:
        error_msg = f"FFmpeg failed: {e.stderr if e.stderr else str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    except FileNotFoundError:
        error_msg = "FFmpeg not found. Please install FFmpeg and ensure it's in your PATH."
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    

class StreamingAudioProcessor:
    """Memory-efficient audio processor that streams chunks instead of loading entire file."""
    
    def __init__(self, audio_path: str, chunk_duration: float = 30.0):
        self.audio_path = audio_path
        self.chunk_duration = chunk_duration
        
        # Get metadata without loading the full file
        self.sample_rate = librosa.get_samplerate(audio_path)
        self.duration = librosa.get_duration(path=audio_path)
        self.chunk_samples = int(chunk_duration * self.sample_rate)
        
        # Internal state
        self._current_offset = 0.0
        
        logger.info(f'streaming audio processor initialized for {audio_path}')
        logger.info(f'duration: {self.duration}s, chunk size: {chunk_duration}s')
        logger.debug(f'sample rate: {self.sample_rate}, chunk samples: {self.chunk_samples}')
    
    def stream_chunks(self) -> Generator[Tuple[np.ndarray, float], None, None]:
        """Generator that yields audio chunks without loading full file into memory."""
        offset = 0.0
        
        while offset < self.duration:
            # Calculate chunk duration (handle last chunk)
            remaining_duration = self.duration - offset
            current_chunk_duration = min(self.chunk_duration, remaining_duration)
            
            try:
                # Load only this chunk
                chunk, sr = librosa.load(
                    self.audio_path,
                    offset=offset,
                    duration=current_chunk_duration,
                    mono=True,
                    sr=self.sample_rate
                )
                
                if chunk.size > 0:  # Only yield non-empty chunks
                    yield chunk, offset
                
                offset += current_chunk_duration
                
            except Exception as e:
                logger.warning(f"Error loading chunk at offset {offset}s: {e}")
                offset += current_chunk_duration
                continue
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except Exception:
            return 0.0
    
    def decibel_iter(self) -> Generator[Tuple[list, float], None, None]:
        """Iterate over audio chunks and convert to decibel readings."""
        for chunk, offset in self.stream_chunks():
            if chunk.size == 0:
                continue
                
            # Split chunk into smaller segments for analysis
            segments = np.array_split(chunk, SPLIT_FRAMES)
            decibels = self._into_decibels(segments)
            
            # Yield decibel data for each second in the chunk
            samples_per_second = self.sample_rate
            for i, segment in enumerate(segments):
                if len(decibels) > i:
                    segment_offset = offset + (i * len(chunk) / len(segments)) / self.sample_rate
                    yield [decibels[i]], segment_offset
    
    def _into_decibels(self, segments):
        """Convert audio segments into decibels."""
        decibels = []
        for segment in segments:
            if segment.size == 0:
                decibels.append(-60.0)
                continue
                
            rms = np.sqrt(np.mean(segment ** 2))
            if rms > 0:
                db = 20 * np.log10(rms)
            else:
                db = -60.0  # Very low dB for silence
            decibels.append(db)
        return decibels
    
    def get_max_decibel(self) -> float:
        """Get maximum decibel across entire file (streaming)."""
        max_db = -np.inf
        for chunk, _ in self.stream_chunks():
            if chunk.size > 0:
                chunk_db = 20 * np.log10(np.maximum(np.sqrt(np.mean(chunk ** 2)), 1e-10))
                max_db = max(max_db, chunk_db)
        return max_db
    
    def get_avg_decibel(self) -> float:
        """Get average decibel across entire file (streaming)."""
        total_rms = 0.0
        chunk_count = 0
        
        for chunk, _ in self.stream_chunks():
            if chunk.size > 0:
                chunk_rms = np.sqrt(np.mean(chunk ** 2))
                total_rms += chunk_rms
                chunk_count += 1
        
        if chunk_count == 0:
            return -60.0
            
        avg_rms = total_rms / chunk_count
        return 20 * np.log10(max(avg_rms, 1e-10))


class AudioProcessor:
    """Legacy audio processor - loads entire file into memory."""
    
    def __init__(self, audio_path):
        self.audio, self.sample_rate = librosa.load(audio_path, mono=True, sr=None)
        self.duration = librosa.get_duration(y=self.audio, sr=self.sample_rate)
        
        # internal use
        self._pos = 0
        
        logger.info(f'audio loaded from {audio_path} with duration {self.duration}s')
        logger.debug(f'frames: {self.audio.size}, sample rate: {self.sample_rate}')
    
    def _seek(self, pos):
        self._pos += pos
    
    def _read(self):
        """read a second of audio data.

        Returns:
            np.array: second of audio data
        """
        frames = self.audio[self._pos:self._pos + self.sample_rate]
        self._seek(self.sample_rate)
        return frames
    
    def _split(self, f):
        """split an array into multiple arrays.

        Args:
            f (np.array): array to split.

        Returns:
            np.array[np.array]: array of split arrays.
        """
        return np.array_split(f, SPLIT_FRAMES)
    
    def _into_decibels(self, c):
        """convert an array of audio data into decibels.

        Args:
            c (np.array): array of audio data.

        Returns:
            np.array: array of decibels.
        """
        decibels = []
        for chunk in c:
            rms = np.sqrt(np.mean(chunk ** 2))
            if rms > 0:
                db = 20 * np.log10(rms)
            else:
                db = -60.0  # Assign a very low dB value for silence
            decibels.append(db)
        return decibels
    
    def get_max_decibel(self):
        as_decibels = librosa.amplitude_to_db(self.audio)
        return np.max(as_decibels)
    
    def get_avg_decibel(self):
        as_decibels = librosa.amplitude_to_db(self.audio)
        return np.mean(as_decibels)
    
    def amp_iter(self):
        self._pos = 0
        while True:
            frames = self._read()
            
            if frames.size == 0:
                break
            
            current = 0
            
            try:
                current = self._pos / self.sample_rate
                current = current - 1
            except ZeroDivisionError:
                pass
            
            yield frames, current
    
    def decibel_iter(self):
        self._pos = 0
        while True:
            frames = self._read()
            
            if frames.size == 0:
                break
            
            chunks = self._split(frames)
            decibels = self._into_decibels(chunks)
            current = 0
            
            try:
                current = self._pos / self.sample_rate
                current = current - 1
            except ZeroDivisionError:
                pass
            
            yield decibels, current