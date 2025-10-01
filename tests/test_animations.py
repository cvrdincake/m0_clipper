#!/usr/bin/env python3
"""
Test script for the futuristic loading animations.
"""

import sys
import os
import time
import pytest
from rich.console import Console

# Add project to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from highlighter.animations import (
    show_boot_sequence,
    create_clip_processing_animation,
    RetroTerminalEffect
)

# Create a console object for testing
console = Console()

def test_boot_sequence_animation():
    """
    Tests that the boot sequence animation runs without errors.
    """
    try:
        show_boot_sequence(console)
        print("✅ Boot sequence animation ran successfully.")
    except Exception as e:
        pytest.fail(f"❌ Boot sequence animation failed: {e}")

def test_clip_processing_animation():
    """
    Tests that the clip processing animation can be created and updated.
    """
    try:
        animation = create_clip_processing_animation(console)
        total_clips = 5
        
        animation.start_clip_processing_animation(total_clips)
        
        for i in range(total_clips):
            animation.update_progress(i, "simulating")
            time.sleep(0.1) # Brief pause
            
        animation.update_progress(total_clips, "finalizing")
        animation.stop_animation(success=True, final_message="Test complete.")
        print("✅ Clip processing animation ran successfully.")
    except Exception as e:
        pytest.fail(f"❌ Clip processing animation failed: {e}")

def test_glitch_effect_animation():
    """
    Tests that the glitch effect runs without errors.
    """
    try:
        effect = RetroTerminalEffect(console)
        effect.glitch_effect("TESTING GLITCH", duration=0.5)
        print("✅ Glitch effect animation ran successfully.")
    except Exception as e:
        pytest.fail(f"❌ Glitch effect animation failed: {e}")
