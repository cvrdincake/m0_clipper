import typer
import tempfile
import pathlib
import glob
import time

from rich.console import Console
from rich.prompt import Prompt
from rich.markdown import Markdown

from loguru import logger
from typing_extensions import Annotated

console = Console()

__all__ = ['processor', 'common', 'analyzer', 'gui']
from . import processor, common, analyzer, gui

DEFAULT_TEMP_DIR = tempfile.TemporaryDirectory()

app = typer.Typer(
    help="Auto Highlighter - Automatically extract highlight clips from VOD videos",
    add_completion=False
)

@app.command()
def reference(
    path_to_video: Annotated[str, typer.Argument(help='path to the video file to use as a reference.'),],
    use_streaming: Annotated[bool, typer.Option('--streaming', help='use streaming processing for large files.')] = True):
    
    video_as_path = pathlib.Path(path_to_video)
    
    if not video_as_path.exists():
        logger.error(f'file does not exist: {path_to_video}')
        exit(1)
    
    # Extract audio first
    audio_path = processor.extract_audio_from_video(path_to_video, DEFAULT_TEMP_DIR.name)
    
    if use_streaming:
        audio = processor.StreamingAudioProcessor(audio_path)
    else:
        audio = processor.AudioProcessor(audio_path)
    
    markdown = f"""
# Reference Audio Analysis

Using this command can provide insight on what decibel threshold to use for the analyze command.
Here are some statistics from the reference video:

- **Duration**: {audio.duration}s
- **Processing Mode**: {'Streaming (Memory Efficient)' if use_streaming else 'Legacy (Full Load)'}

## Decibel Analysis

- **Average Decibel**: {audio.get_avg_decibel():.1f} dB
- **Maximum Decibel**: {audio.get_max_decibel():.1f} dB
- **Dynamic Range**: {audio.get_max_decibel() - audio.get_avg_decibel():.1f} dB

## Threshold Recommendations

The original recommendation of `max_db - 1.4` tends to be too conservative for gaming content.
Here are better options based on your audio characteristics:

- **🎯 Balanced (Recommended)**: *{audio.get_avg_decibel() + (audio.get_max_decibel() - audio.get_avg_decibel()) * 0.6:.1f}* dB
  - Good balance for most gaming content
  - Catches significant moments without too much noise

- **🔒 Conservative**: *{audio.get_max_decibel() - 2.0:.1f}* dB  
  - Fewer clips, only very loud moments
  - Use if you want only the most dramatic highlights

- **🔓 Aggressive**: *{audio.get_avg_decibel() + (audio.get_max_decibel() - audio.get_avg_decibel()) * 0.4:.1f}* dB
  - More clips, catches quieter highlights  
  - Use if you want to catch subtle but important moments

**Tip**: Start with the Balanced setting and adjust based on results!

## Performance Info

- **Memory Usage**: {'~50-100MB (streaming)' if use_streaming else f'~{(audio.duration * 48000 * 4 / 1024 / 1024):.0f}MB (full load)'}
- **Processing Speed**: {'Slower but memory efficient' if use_streaming else 'Faster but memory intensive'}
    """
    console.print(Markdown(markdown))
    

@app.command()
def gui():
    """Launch the graphical user interface."""
    try:
        gui.main()
    except ImportError as e:
        console.print(f"[red]Error:[/] GUI dependencies not available: {e}")
        console.print("[yellow]Install GUI dependencies with:[/] pip install tkinterdnd2")
    except Exception as e:
        console.print(f"[red]Error starting GUI:[/] {e}")


@app.command()
def batch(
    videos_pattern: Annotated[str, typer.Argument(help='glob pattern for video files to process (e.g., "*.mp4" or "/path/to/videos/*.mkv")')],
    output_directory: Annotated[str, typer.Argument(help='base output directory for all processed videos')],
    decibel_threshold: Annotated[float, typer.Option('--decibel_threshold', '-t', help='decibel threshold to use for analysis.')] = -5.0,
    max_workers: Annotated[int, typer.Option('--workers', '-w', help='maximum number of videos to process in parallel.')] = 3,
    use_streaming: Annotated[bool, typer.Option('--streaming', help='use streaming processing for large files.')] = True,
    verbose: Annotated[bool, typer.Option(help='enable verbose logging.')] = False,
):
    """Process multiple videos in parallel batch mode."""
    
    if not verbose:
        logger.disable('highlighter')
    
    # Find video files matching pattern
    video_files = glob.glob(videos_pattern)
    
    if not video_files:
        console.print(f"[red]No video files found matching pattern: {videos_pattern}[/red]")
        exit(1)
    
    console.print(f"[green]Found {len(video_files)} video files to process[/green]")
    
    # Create batch jobs
    jobs = []
    for video_file in video_files:
        video_name = pathlib.Path(video_file).stem
        job_output_path = pathlib.Path(output_directory) / f"{video_name}_highlights"
        
        job = analyzer.BatchJob(
            video_path=video_file,
            output_path=str(job_output_path),
            decibel_threshold=decibel_threshold,
            use_streaming=use_streaming
        )
        jobs.append(job)
        
        console.print(f"  📹 {pathlib.Path(video_file).name} → {job_output_path.name}/")
    
    # Process batch
    batch_processor = analyzer.BatchProcessor(max_workers=max_workers)
    
    def progress_callback(completed, total, job_id, result):
        status = result.get('status', 'unknown')
        video_name = pathlib.Path(result.get('video_path', '')).name
        
        if status == 'completed':
            highlights = result.get('highlights_generated', 0)
            console.print(f"[green]✅ {completed}/{total} completed: {video_name} ({highlights} clips)[/green]")
        else:
            error = result.get('error', 'unknown error')
            console.print(f"[red]❌ {completed}/{total} failed: {video_name} - {error}[/red]")
    
    console.print(f"\n[blue]🚀 Starting batch processing with {max_workers} workers...[/blue]")
    
    start_time = time.time()
    results = batch_processor.process_batch(jobs, progress_callback)
    end_time = time.time()
    
    # Summary
    successful = sum(1 for r in results.values() if r['status'] == 'completed')
    failed = len(results) - successful
    total_highlights = sum(r.get('result', {}).get('highlights_generated', 0) for r in results.values() if r['status'] == 'completed')
    
    console.print(f"\n[bold]📊 Batch Processing Summary[/bold]")
    console.print(f"  ⏱️  Total time: {end_time - start_time:.1f} seconds")
    console.print(f"  ✅ Successful: {successful}/{len(video_files)} videos")
    console.print(f"  ❌ Failed: {failed}/{len(video_files)} videos")
    console.print(f"  🎬 Total highlights generated: {total_highlights}")
    console.print(f"  📁 Output directory: {output_directory}")
    
    if failed > 0:
        console.print(f"\n[yellow]⚠️  {failed} videos failed to process. Check logs for details.[/yellow]")


@app.command()
def demo():
    """Show a demo of the futuristic loading animations."""
    try:
        from .animations import show_boot_sequence, create_clip_processing_animation, show_glitch_effect
        
        console.print("[bold cyan]🎮 M0 Clipper: Cyber Animation Demo 🎮[/]")
        console.print()
        
        # Show boot sequence
        show_boot_sequence()
        
        # Demo clip processing animation
        console.print("\n[bold]Demonstrating clip processing animation...[/]")
        animation = create_clip_processing_animation()
        
        # Simulate clip processing
        total_clips = 8
        animation.start_clip_processing_animation(total_clips)
        
        # Simulate progress updates with different stages
        import time
        for i in range(total_clips + 1):
            if i < 2:
                stage = "analyzing"
            elif i < 6:
                stage = "generating"
            else:
                stage = "finalizing"
            
            animation.update_progress(i, stage)
            time.sleep(0.8)  # Slightly faster for demo
        
        animation.stop_animation(success=True)
        
        # Demo glitch effect
        time.sleep(1)
        show_glitch_effect("HIGHLIGHT EXTRACTION COMPLETE!", duration=1.5)
        
        console.print("\n[bold green]✨ Demo complete! These animations will appear during actual processing.[/]")
        
    except ImportError as e:
        console.print(f"[red]Animation dependencies not available: {e}[/]")
    except Exception as e:
        console.print(f"[red]Demo failed: {e}[/]")


@app.command()
def analyze(
    path_to_video: Annotated[str, typer.Argument(help='path to the video file to analyze.'),], 
    output_directory: Annotated[str, typer.Argument(help='path to the output directory.'),], 
    decibel_threshold: Annotated[float, typer.Option('--decibel_threshold', '-t', help='decibel threshold to use for analysis.')] = -5.0,
    use_streaming: Annotated[bool, typer.Option('--streaming', help='use streaming processing for large files.')] = True,
    clip_length: Annotated[int, typer.Option('--clip_length', '-l', help='total length of each clip in seconds.')] = 30,
    verbose: Annotated[bool, typer.Option(help='enable verbose logging.')] = False,
    ):
    
    if not verbose:
        logger.disable('highlighter')
    
    video_as_path = pathlib.Path(path_to_video)
    output_as_path = pathlib.Path(output_directory)
    
    if not video_as_path.exists():
        logger.error(f'File does not exist: {path_to_video}')
        
        files_in_video_path = glob.glob(f'{video_as_path.parent}/*')
        related_file = None
        
        for file in files_in_video_path:
            if common.similarity(file, path_to_video) > 0.90:
                console.print(f'Found similar file: [bold green]"{file}"')
                confirm = Prompt.ask('Did you mean this file? ([italic]skip if this is a mistake.[/])', choices=['yes', 'no', 'skip'])
                if confirm == 'yes':
                    related_file = file
                    break
                elif confirm == 'skip':
                    break
                else:
                    logger.critical('no related file found. exiting...')
                    exit(1)
                    
        if related_file:
            logger.info(f'Using related file: {related_file}')
            path_to_video = related_file
        else:
            exit(1)
            
    if not output_as_path.exists():
        logger.info(f'Creating output directory: {output_directory}')
        output_as_path.mkdir(parents=True, exist_ok=True)
    
    # Extract audio
    audio_path = processor.extract_audio_from_video(path_to_video, DEFAULT_TEMP_DIR.name)
    
    # Choose processor type
    if use_streaming:
        console.print(f"[blue]🔄 Using streaming processing (memory efficient)[/blue]")
        audio_processor = processor.StreamingAudioProcessor(audio_path)
        _a = analyzer.StreamingAudioAnalysis(
            video_path=path_to_video,
            audio_processor=audio_processor,
            output_path=output_directory,
            decibel_threshold=decibel_threshold
        )
    else:
        console.print(f"[blue]⚡ Using legacy processing (faster but more memory)[/blue]")
        audio_processor = processor.AudioProcessor(audio_path)
        _a = analyzer.AudioAnalysis(
            video_path=path_to_video,
            audio_path=audio_path,
            output_path=output_directory,
            decibel_threshold=decibel_threshold
        )
    
    # Set clip length
    _a.start_point = clip_length // 2
    _a.end_point = clip_length - _a.start_point
    
    # Run analysis
    start_time = time.time()
    if use_streaming:
        _a.streaming_crest_ceiling_algorithm()
    else:
        _a.crest_ceiling_algorithm()
    
    _a.export()
    completed_count, failed_count = _a.generate_all_highlights()
    end_time = time.time()
    
    # Report results
    console.print(f"\n[bold]📊 Analysis Complete[/bold]")
    console.print(f"  ⏱️  Processing time: {end_time - start_time:.1f} seconds")
    console.print(f"  🎯 Threshold used: {decibel_threshold:.1f} dB")
    console.print(f"  🔍 Processing mode: {'Streaming' if use_streaming else 'Legacy'}")
    
    if failed_count > 0:
        console.print(f"[yellow]⚠️  {failed_count} clips failed to generate[/yellow]")
    
    if completed_count > 0:
        console.print(f"[green]✅ Generated {completed_count} highlight clips successfully![/green]")
        console.print(f"[green]📁 Clips saved to: {output_directory}[/green]")
    else:
        console.print(f"[yellow]⚠️  No highlights found. Try lowering the threshold or use 'reference' command.[/yellow]")

def cli():
    app()
    
if __name__ == "__main__":
    cli()