#!/usr/bin/env python3
"""
Simple test script to demonstrate the futuristic loading animations.
Run this to see the animations in action without processing any videos.
"""

import sys
import time
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from highlighter.animations import (
    show_boot_sequence, 
    create_clip_processing_animation, 
    show_glitch_effect,
    RetroTerminalEffect
)
from rich.console import Console


def main():
    """Run animation demos."""
    console = Console()
    
    # Title
    console.print("\n" + "="*60)
    console.print("[bold cyan]🎮 M0 CLIPPER: CYBER ANIMATION SHOWCASE 🎮[/]", justify="center")
    console.print("="*60 + "\n")
    
    # Demo 1: Boot sequence
    console.print("[bold yellow]🚀 Demo 1: System Boot Sequence[/]")
    console.print("-" * 40)
    show_boot_sequence(console)
    
    time.sleep(1)
    
    # Demo 2: Clip processing animation
    console.print("\n[bold yellow]⚡ Demo 2: Clip Processing Animation[/]")
    console.print("-" * 40)
    
    animation = create_clip_processing_animation(console)
    total_clips = 10
    
    console.print(f"[dim]Simulating processing of {total_clips} clips...[/]\n")
    
    animation.start_clip_processing_animation(total_clips)
    
    # Simulate different processing stages
    stages = ["analyzing", "analyzing", "generating", "generating", "generating", 
              "generating", "generating", "finalizing", "finalizing", "finalizing"]
    
    for i, stage in enumerate(stages):
        animation.update_progress(i, stage)
        time.sleep(0.7)  # Slow enough to see the animation
    
    # Final update
    animation.update_progress(total_clips, "finalizing")
    time.sleep(0.5)
    
    animation.stop_animation(success=True, final_message="All systems nominal! Highlight arsenal ready for deployment!")
    
    time.sleep(1)
    
    # Demo 3: Glitch effects
    console.print("\n[bold yellow]💥 Demo 3: Glitch Effects[/]")
    console.print("-" * 40)
    
    effect = RetroTerminalEffect(console)
    
    messages = [
        "PROCESSING COMPLETE",
        "HIGHLIGHTS EXTRACTED", 
        "MISSION ACCOMPLISHED"
    ]
    
    for msg in messages:
        effect.glitch_effect(msg, duration=1.5)
        time.sleep(0.5)
    
    # Final showcase
    console.print("\n" + "="*60)
    console.print("[bold green]✨ ANIMATION SHOWCASE COMPLETE ✨[/]", justify="center")
    console.print("[dim]These animations will enhance your M0 Clipper experience![/]", justify="center")
    console.print("="*60)
    
    # Usage instructions
    console.print("\n[bold cyan]🎯 How to Use:[/]")
    console.print("• [bold]GUI:[/] Animations appear automatically during processing")
    console.print("• [bold]CLI:[/] Use 'highlighter demo' to see animations anytime")
    console.print("• [bold]Processing:[/] Animations activate during actual clip generation")
    
    console.print("\n[dim]Press Ctrl+C to exit at any time during real processing[/]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[yellow]Demo interrupted by user[/]")
    except Exception as e:
        console = Console()
        console.print(f"\n[red]Demo error: {e}[/]")