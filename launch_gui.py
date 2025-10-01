#!/usr/bin/env python3
"""
Standalone launcher for the Auto Highlighter GUI.
Run this script to launch the graphical interface.
"""

import sys
import os

# Add the parent directory to Python path so we can import highlighter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from highlighter.gui import main
    main()
except ImportError as e:
    print(f"Error: Required dependencies not found: {e}")
    print("Please install dependencies with: pip install -r requirements.txt")
    print("Or install the package: pip install -e .")
    sys.exit(1)
except Exception as e:
    print(f"Error starting GUI: {e}")
    sys.exit(1)