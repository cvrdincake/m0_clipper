#!/usr/bin/env python3
"""
Futuristic loading animations and UI effects for M0 Clipper.
Urban videogame-inspired visual feedback with ironic quips.
"""

import time
import random
import threading
from typing import List, Optional, Callable
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, SpinnerColumn
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich import box


class CyberQuips:
    """Collection of ironic and witty status messages for different processing stages."""
    
    INITIALIZING = [
        "Initializing neural pathways...",
        "Booting up the highlight matrix...",
        "Calibrating audio receptors...",
        "Loading cybernetic enhancement protocols...",
        "Establishing connection to the highlight grid...",
        "Warming up the bass cannons...",
        "Synchronizing with the beat...",
        "Activating highlight detection arrays..."
    ]
    
    ANALYZING = [
        "Scanning for epic moments...",
        "Detecting peak gaming energy...",
        "Analyzing audio DNA for highlights...",
        "Searching for those 'poggers' moments...",
        "Calculating hype levels...",
        "Hunting for clip-worthy content...",
        "Processing digital dopamine spikes...",
        "Isolating moments of pure gaming bliss...",
        "Detecting audience engagement peaks...",
        "Mapping the emotional landscape...",
        "Extracting essence of gaming excellence...",
        "Identifying viewer retention magnets..."
    ]
    
    GENERATING = [
        "Crafting highlight masterpieces...",
        "Rendering moments of glory...",
        "Compiling your greatest hits...",
        "Manufacturing viral content...",
        "Assembling clip collection...",
        "Producing streaming gold...",
        "Forging content creator ammunition...",
        "Building your highlight reel empire...",
        "Constructing fame-inducing segments...",
        "Synthesizing pure entertainment...",
        "Creating tomorrow's viral clips...",
        "Weaponizing your best moments..."
    ]
    
    FINALIZING = [
        "Applying final polish...",
        "Adding that special sauce...",
        "Optimizing for maximum impact...",
        "Injecting viral potential...",
        "Calibrating engagement factors...",
        "Fine-tuning perfection...",
        "Ensuring peak performance...",
        "Maximizing clip effectiveness..."
    ]
    
    COMPLETE = [
        "Mission accomplished, commander!",
        "Highlight extraction complete!",
        "Your content arsenal is ready!",
        "Success! Viral potential: MAXIMUM",
        "Operation successful - highlights deployed!",
        "Achievement unlocked: Clip Master!",
        "Highlight synthesis: 100% complete!",
        "Your streaming empire awaits!"
    ]
    
    ERROR = [
        "Houston, we have a problem...",
        "Something went sideways in the matrix...",
        "Error in the highlight dimension...",
        "The algorithm had a bad day...",
        "Technical difficulties detected...",
        "System malfunction in sector 7...",
        "The AI needs a coffee break...",
        "Plot twist: unexpected error!"
    ]


class CyberProgressBar:
    """Futuristic progress bar with cyberpunk aesthetics."""
    
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self._current_quip = ""
        self._quip_timer = 0
        self._quip_interval = 3.0  # Change quip every 3 seconds
        self._last_update = time.time()
        
    def create_cyber_progress(self, description: str = "Processing") -> Progress:
        """Create a cyberpunk-styled progress bar."""
        return Progress(
            SpinnerColumn(spinner_style="cyan"),
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(
                bar_width=None,
                style="cyan",
                complete_style="bright_cyan",
                finished_style="bright_green",
                pulse_style="bright_cyan"
            ),
            TextColumn("[bold cyan]{task.percentage:>3.1f}%"),
            TimeElapsedColumn(),
            console=self.console,
            refresh_per_second=10
        )
    
    def get_rotating_quip(self, quips: List[str]) -> str:
        """Get a rotating quip that changes periodically."""
        current_time = time.time()
        
        if current_time - self._last_update > self._quip_interval:
            self._current_quip = random.choice(quips)
            self._last_update = current_time
        
        if not self._current_quip:
            self._current_quip = random.choice(quips)
        
        return self._current_quip
    
    def create_status_panel(self, title: str, quip: str, style: str = "cyan") -> Panel:
        """Create a futuristic status panel."""
        # Create cyberpunk-style border characters
        cyber_chars = "▓▒░"
        border_style = f"bright_{style}"
        
        # Format the quip with some style
        styled_quip = Text(quip, style=f"italic {style}")
        centered_quip = Align.center(styled_quip)
        
        return Panel(
            centered_quip,
            title=f"[bold {border_style}]⚡ {title} ⚡[/]",
            border_style=border_style,
            box=box.HEAVY,
            padding=(1, 2)
        )


class HolographicSpinner:
    """Advanced spinner with holographic effects."""
    
    CYBER_FRAMES = [
        "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"
    ]
    
    MATRIX_FRAMES = [
        "▰▱▱▱▱", "▰▰▱▱▱", "▰▰▰▱▱", "▰▰▰▰▱", "▰▰▰▰▰",
        "▱▰▰▰▰", "▱▱▰▰▰", "▱▱▱▰▰", "▱▱▱▱▰", "▱▱▱▱▱"
    ]
    
    NEON_FRAMES = [
        "◐", "◓", "◑", "◒"
    ]
    
    def __init__(self, style: str = "cyber"):
        self.frames = {
            "cyber": self.CYBER_FRAMES,
            "matrix": self.MATRIX_FRAMES,
            "neon": self.NEON_FRAMES
        }.get(style, self.CYBER_FRAMES)
        
        self.frame_index = 0
    
    def next_frame(self) -> str:
        """Get the next frame in the animation."""
        frame = self.frames[self.frame_index]
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        return frame


class CyberLoadingAnimation:
    """Main loading animation system with cyberpunk aesthetics."""
    
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.progress_bar = CyberProgressBar(self.console)
        self.spinner = HolographicSpinner("cyber")
        self._is_running = False
        self._animation_thread = None
        self._current_stage = "initializing"
        self._progress = 0.0
        self._total_items = 0
        self._completed_items = 0
        
    def start_clip_processing_animation(self, total_clips: int, 
                                      progress_callback: Optional[Callable] = None):
        """Start the main clip processing animation."""
        self._total_items = total_clips
        self._completed_items = 0
        self._is_running = True
        self._current_stage = "initializing"
        
        # Start animation in separate thread
        self._animation_thread = threading.Thread(
            target=self._run_animation,
            args=(progress_callback,),
            daemon=True
        )
        self._animation_thread.start()
    
    def update_progress(self, completed: int, stage: str = None):
        """Update the progress of clip processing."""
        self._completed_items = completed
        self._progress = (completed / self._total_items * 100) if self._total_items > 0 else 0
        
        if stage:
            self._current_stage = stage
    
    def stop_animation(self, success: bool = True, final_message: str = None):
        """Stop the animation and show final result."""
        self._is_running = False
        
        if self._animation_thread and self._animation_thread.is_alive():
            self._animation_thread.join(timeout=1.0)
        
        # Show final result
        if success:
            final_quip = final_message or random.choice(CyberQuips.COMPLETE)
            panel = self.progress_bar.create_status_panel(
                "MISSION COMPLETE", final_quip, "green"
            )
        else:
            final_quip = final_message or random.choice(CyberQuips.ERROR)
            panel = self.progress_bar.create_status_panel(
                "SYSTEM ERROR", final_quip, "red"
            )
        
        self.console.print(panel)
    
    def _run_animation(self, progress_callback: Optional[Callable] = None):
        """Run the main animation loop."""
        with Live(console=self.console, refresh_per_second=10) as live:
            while self._is_running:
                # Get current stage quips
                quips = self._get_stage_quips()
                
                # Create the main display
                display = self._create_main_display(quips)
                
                # Update live display
                live.update(display)
                
                # Call progress callback if provided
                if progress_callback:
                    progress_callback(self._completed_items, self._total_items, self._progress)
                
                time.sleep(0.1)
    
    def _get_stage_quips(self) -> List[str]:
        """Get quips for the current stage."""
        stage_map = {
            "initializing": CyberQuips.INITIALIZING,
            "analyzing": CyberQuips.ANALYZING,
            "generating": CyberQuips.GENERATING,
            "finalizing": CyberQuips.FINALIZING
        }
        return stage_map.get(self._current_stage, CyberQuips.ANALYZING)
    
    def _create_main_display(self, quips: List[str]):
        """Create the main animated display."""
        # Get rotating quip
        current_quip = self.progress_bar.get_rotating_quip(quips)
        
        # Create progress visualization
        progress_text = self._create_progress_text()
        
        # Create spinner
        spinner_char = self.spinner.next_frame()
        
        # Combine all elements
        title = f"{spinner_char} HIGHLIGHT FORGE v3.0 {spinner_char}"
        
        content = Text()
        content.append(progress_text, style="bold cyan")
        content.append("\n\n")
        content.append(current_quip, style="italic bright_blue")
        
        return Panel(
            Align.center(content),
            title=f"[bold bright_cyan]{title}[/]",
            border_style="bright_cyan",
            box=box.DOUBLE,
            padding=(1, 3)
        )
    
    def _create_progress_text(self) -> str:
        """Create visual progress representation."""
        if self._total_items == 0:
            return "Initializing systems..."
        
        # Create a visual progress bar
        bar_width = 30
        filled = int((self._completed_items / self._total_items) * bar_width)
        empty = bar_width - filled
        
        bar = "█" * filled + "░" * empty
        percentage = (self._completed_items / self._total_items) * 100
        
        stage_emoji = {
            "initializing": "🔄",
            "analyzing": "🔍",
            "generating": "⚡",
            "finalizing": "✨"
        }.get(self._current_stage, "🔄")
        
        return f"{stage_emoji} [{bar}] {percentage:.1f}%\nClips: {self._completed_items}/{self._total_items}"


class RetroTerminalEffect:
    """Retro terminal boot-up effect for initialization."""
    
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
    
    def boot_sequence(self):
        """Display a retro boot sequence."""
        boot_lines = [
            "[green]HIGHLIGHT EXTRACTION SYSTEM v3.0[/]",
            "[dim]Booting neural networks...[/]",
            "[dim]Loading audio analysis modules...[/]",
            "[dim]Initializing clip generation engine...[/]",
            "[dim]Establishing quantum entanglement with FFmpeg...[/]",
            "[bright_green]✓ All systems online[/]",
            "",
            "[bold cyan]Ready to extract highlights![/]"
        ]
        
        for line in boot_lines:
            self.console.print(line)
            time.sleep(0.3)
    
    def glitch_effect(self, text: str, duration: float = 2.0):
        """Create a glitch effect on text."""
        glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        original_text = text
        
        start_time = time.time()
        
        with Live(console=self.console, refresh_per_second=20) as live:
            while time.time() - start_time < duration:
                # Create glitched version
                glitched = ""
                for char in original_text:
                    if random.random() < 0.1:  # 10% chance to glitch
                        glitched += random.choice(glitch_chars)
                    else:
                        glitched += char
                
                live.update(Text(glitched, style="bold red"))
                time.sleep(0.05)
        
        # Show final clean text
        self.console.print(Text(original_text, style="bold green"))


# Convenience functions for easy integration
def create_clip_processing_animation(console: Optional[Console] = None) -> CyberLoadingAnimation:
    """Create a new clip processing animation instance."""
    return CyberLoadingAnimation(console)

def show_boot_sequence(console: Optional[Console] = None):
    """Show the retro boot sequence."""
    effect = RetroTerminalEffect(console)
    effect.boot_sequence()

def show_glitch_effect(text: str, console: Optional[Console] = None, duration: float = 2.0):
    """Show a glitch effect on text."""
    effect = RetroTerminalEffect(console)
    effect.glitch_effect(text, duration)


# Example usage and testing
if __name__ == "__main__":
    # Demo the animation system
    console = Console()
    
    console.print("[bold cyan]🎮 M0 Clipper Animation Demo 🎮[/]")
    console.print()
    
    # Show boot sequence
    show_boot_sequence(console)
    
    # Demo clip processing animation
    animation = create_clip_processing_animation(console)
    
    # Simulate clip processing
    total_clips = 10
    animation.start_clip_processing_animation(total_clips)
    
    # Simulate progress updates
    for i in range(total_clips + 1):
        if i < 3:
            stage = "analyzing"
        elif i < 8:
            stage = "generating"
        else:
            stage = "finalizing"
        
        animation.update_progress(i, stage)
        time.sleep(1)
    
    animation.stop_animation(success=True)
    
    # Demo glitch effect
    time.sleep(1)
    show_glitch_effect("HIGHLIGHT EXTRACTION COMPLETE!", console, 1.5)