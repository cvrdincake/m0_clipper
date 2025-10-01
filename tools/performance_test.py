#!/usr/bin/env python3
"""
Performance testing utility for M0 Clipper improvements.
Tests memory usage, processing speed, and scalability improvements.
"""

import time
import psutil
import tempfile
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from highlighter import processor, analyzer
from loguru import logger


class PerformanceMonitor:
    """Monitor system performance during video processing."""
    
    def __init__(self):
        self.process = psutil.Process()
        self.start_time = None
        self.peak_memory = 0
        self.measurements = []
        
    def start(self):
        """Start monitoring."""
        self.start_time = time.time()
        self.peak_memory = 0
        self.measurements = []
        
    def measure(self, label: str = ""):
        """Take a measurement."""
        if self.start_time is None:
            return
            
        current_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        self.peak_memory = max(self.peak_memory, current_memory)
        
        measurement = {
            'time': time.time() - self.start_time,
            'memory_mb': current_memory,
            'label': label
        }
        self.measurements.append(measurement)
        
    def get_stats(self) -> Dict:
        """Get performance statistics."""
        if not self.measurements:
            return {}
            
        total_time = time.time() - self.start_time if self.start_time else 0
        avg_memory = sum(m['memory_mb'] for m in self.measurements) / len(self.measurements)
        
        return {
            'total_time': total_time,
            'peak_memory_mb': self.peak_memory,
            'avg_memory_mb': avg_memory,
            'measurements': len(self.measurements)
        }


def create_test_audio(duration_seconds: int = 300) -> str:
    """Create a test audio file of specified duration."""
    import numpy as np
    import soundfile as sf
    
    # Generate 5 minutes of test audio with some variation
    sample_rate = 48000
    samples = duration_seconds * sample_rate
    
    # Create audio with some peaks for highlight detection
    t = np.linspace(0, duration_seconds, samples)
    
    # Base audio (quiet background)
    audio = 0.01 * np.sin(2 * np.pi * 440 * t)  # Quiet 440Hz tone
    
    # Add some "highlight" moments every 30 seconds
    for peak_time in range(30, duration_seconds, 30):
        start_sample = int(peak_time * sample_rate)
        end_sample = int((peak_time + 2) * sample_rate)  # 2-second peaks
        
        if end_sample < len(audio):
            # Add loud moment
            audio[start_sample:end_sample] += 0.5 * np.sin(2 * np.pi * 880 * t[start_sample:end_sample])
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    sf.write(temp_file.name, audio, sample_rate)
    temp_file.close()
    
    return temp_file.name


def test_processor_performance(test_audio_path: str) -> Dict:
    """Test performance of streaming vs legacy processor."""
    results = {}
    
    print("🧪 Testing Audio Processor Performance...")
    
    # Test legacy processor
    print("  Testing legacy processor (full load)...")
    monitor = PerformanceMonitor()
    monitor.start()
    
    try:
        legacy_processor = processor.AudioProcessor(test_audio_path)
        monitor.measure("after_load")
        
        avg_db = legacy_processor.get_avg_decibel()
        max_db = legacy_processor.get_max_decibel()
        monitor.measure("after_analysis")
        
        results['legacy'] = {
            'stats': monitor.get_stats(),
            'avg_db': avg_db,
            'max_db': max_db,
            'success': True
        }
        
    except Exception as e:
        results['legacy'] = {
            'error': str(e),
            'success': False
        }
    
    # Test streaming processor
    print("  Testing streaming processor (memory efficient)...")
    monitor = PerformanceMonitor()
    monitor.start()
    
    try:
        streaming_processor = processor.StreamingAudioProcessor(test_audio_path)
        monitor.measure("after_init")
        
        avg_db = streaming_processor.get_avg_decibel()
        max_db = streaming_processor.get_max_decibel()
        monitor.measure("after_analysis")
        
        results['streaming'] = {
            'stats': monitor.get_stats(),
            'avg_db': avg_db,
            'max_db': max_db,
            'success': True
        }
        
    except Exception as e:
        results['streaming'] = {
            'error': str(e),
            'success': False
        }
    
    return results


def test_analysis_performance(test_audio_path: str, test_video_path: str = None) -> Dict:
    """Test performance of streaming vs legacy analysis."""
    results = {}
    
    print("🧪 Testing Analysis Performance...")
    
    # Use test audio path as video path if no video provided
    if test_video_path is None:
        test_video_path = test_audio_path
    
    output_dir = tempfile.mkdtemp()
    
    # Test legacy analysis
    print("  Testing legacy analysis...")
    monitor = PerformanceMonitor()
    monitor.start()
    
    try:
        legacy_analyzer = analyzer.AudioAnalysis(
            video_path=test_video_path,
            audio_path=test_audio_path,
            output_path=output_dir,
            decibel_threshold=-15.0  # Lower threshold to find test highlights
        )
        monitor.measure("after_init")
        
        legacy_analyzer.crest_ceiling_algorithm()
        monitor.measure("after_analysis")
        
        highlights_found = len(legacy_analyzer._captured_result)
        
        results['legacy_analysis'] = {
            'stats': monitor.get_stats(),
            'highlights_found': highlights_found,
            'success': True
        }
        
    except Exception as e:
        results['legacy_analysis'] = {
            'error': str(e),
            'success': False
        }
    
    # Test streaming analysis
    print("  Testing streaming analysis...")
    monitor = PerformanceMonitor()
    monitor.start()
    
    try:
        streaming_processor = processor.StreamingAudioProcessor(test_audio_path)
        streaming_analyzer = analyzer.StreamingAudioAnalysis(
            video_path=test_video_path,
            audio_processor=streaming_processor,
            output_path=output_dir,
            decibel_threshold=-15.0
        )
        monitor.measure("after_init")
        
        streaming_analyzer.streaming_crest_ceiling_algorithm()
        monitor.measure("after_analysis")
        
        highlights_found = len(streaming_analyzer._captured_result)
        
        results['streaming_analysis'] = {
            'stats': monitor.get_stats(),
            'highlights_found': highlights_found,
            'success': True
        }
        
    except Exception as e:
        results['streaming_analysis'] = {
            'error': str(e),
            'success': False
        }
    
    # Cleanup
    import shutil
    shutil.rmtree(output_dir, ignore_errors=True)
    
    return results


def test_batch_processing() -> Dict:
    """Test batch processing performance with multiple small files."""
    results = {}
    
    print("🧪 Testing Batch Processing...")
    
    # Create multiple test files
    test_files = []
    try:
        for i in range(3):  # Create 3 small test files
            test_file = create_test_audio(60)  # 1 minute each
            test_files.append(test_file)
        
        output_dir = tempfile.mkdtemp()
        
        # Create batch jobs
        jobs = []
        for i, test_file in enumerate(test_files):
            job = analyzer.BatchJob(
                video_path=test_file,
                output_path=f"{output_dir}/test_{i}",
                decibel_threshold=-15.0,
                use_streaming=True
            )
            jobs.append(job)
        
        # Test batch processing
        monitor = PerformanceMonitor()
        monitor.start()
        
        batch_processor = analyzer.BatchProcessor(max_workers=2)
        
        def progress_callback(completed, total, job_id, result):
            monitor.measure(f"job_{completed}_completed")
        
        batch_results = batch_processor.process_batch(jobs, progress_callback)
        monitor.measure("batch_complete")
        
        successful = sum(1 for r in batch_results.values() if r['status'] == 'completed')
        
        results['batch_processing'] = {
            'stats': monitor.get_stats(),
            'jobs_completed': successful,
            'total_jobs': len(jobs),
            'success': True
        }
        
        # Cleanup
        import shutil
        shutil.rmtree(output_dir, ignore_errors=True)
        
    except Exception as e:
        results['batch_processing'] = {
            'error': str(e),
            'success': False
        }
    finally:
        # Cleanup test files
        for test_file in test_files:
            try:
                os.unlink(test_file)
            except:
                pass
    
    return results


def print_results(results: Dict):
    """Print formatted performance test results."""
    print("\n" + "="*60)
    print("📊 PERFORMANCE TEST RESULTS")
    print("="*60)
    
    for test_name, test_results in results.items():
        print(f"\n🔹 {test_name.upper().replace('_', ' ')}")
        print("-" * 40)
        
        if isinstance(test_results, dict) and test_results.get('success'):
            stats = test_results.get('stats', {})
            
            if 'total_time' in stats:
                print(f"  ⏱️  Total Time: {stats['total_time']:.2f} seconds")
            if 'peak_memory_mb' in stats:
                print(f"  🧠 Peak Memory: {stats['peak_memory_mb']:.1f} MB")
            if 'avg_memory_mb' in stats:
                print(f"  📊 Average Memory: {stats['avg_memory_mb']:.1f} MB")
            
            # Test-specific results
            if 'highlights_found' in test_results:
                print(f"  🎯 Highlights Found: {test_results['highlights_found']}")
            if 'avg_db' in test_results:
                print(f"  🔊 Average dB: {test_results['avg_db']:.1f}")
            if 'max_db' in test_results:
                print(f"  📈 Max dB: {test_results['max_db']:.1f}")
            if 'jobs_completed' in test_results:
                print(f"  ✅ Jobs Completed: {test_results['jobs_completed']}/{test_results.get('total_jobs', 0)}")
                
        elif isinstance(test_results, dict) and not test_results.get('success'):
            print(f"  ❌ FAILED: {test_results.get('error', 'Unknown error')}")
        else:
            print(f"  ⚠️  Invalid result format")


def main():
    """Run performance tests."""
    print("🚀 M0 Clipper Performance Testing Suite")
    print("="*60)
    
    # Check dependencies
    try:
        import soundfile
    except ImportError:
        print("❌ Missing dependency: soundfile")
        print("Install with: pip install soundfile")
        return
    
    all_results = {}
    
    # Create test audio file
    print("📁 Creating test audio file (5 minutes)...")
    test_audio = create_test_audio(300)  # 5 minutes
    
    try:
        # Run tests
        all_results.update(test_processor_performance(test_audio))
        all_results.update(test_analysis_performance(test_audio))
        all_results.update(test_batch_processing())
        
        # Print results
        print_results(all_results)
        
        # Performance comparison
        print("\n" + "="*60)
        print("📈 PERFORMANCE COMPARISON")
        print("="*60)
        
        # Memory comparison
        if 'legacy' in all_results and 'streaming' in all_results:
            legacy_mem = all_results['legacy']['stats'].get('peak_memory_mb', 0)
            streaming_mem = all_results['streaming']['stats'].get('peak_memory_mb', 0)
            
            if legacy_mem > 0 and streaming_mem > 0:
                memory_savings = ((legacy_mem - streaming_mem) / legacy_mem) * 100
                print(f"💾 Memory Savings: {memory_savings:.1f}% ({legacy_mem:.1f}MB → {streaming_mem:.1f}MB)")
        
        # Analysis comparison
        if 'legacy_analysis' in all_results and 'streaming_analysis' in all_results:
            legacy_time = all_results['legacy_analysis']['stats'].get('total_time', 0)
            streaming_time = all_results['streaming_analysis']['stats'].get('total_time', 0)
            
            if legacy_time > 0 and streaming_time > 0:
                if streaming_time > legacy_time:
                    time_diff = ((streaming_time - legacy_time) / legacy_time) * 100
                    print(f"⏱️  Processing Time: +{time_diff:.1f}% slower (trade-off for memory efficiency)")
                else:
                    time_savings = ((legacy_time - streaming_time) / legacy_time) * 100
                    print(f"⏱️  Processing Time: {time_savings:.1f}% faster")
        
        print("\n✅ Performance testing completed successfully!")
        
    finally:
        # Cleanup
        try:
            os.unlink(test_audio)
        except:
            pass


if __name__ == "__main__":
    main()