#!/usr/bin/env python3
"""
Test script to verify the GUI can be imported and initialized without errors.
"""

import sys
import os

# Add the project to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#!/usr/bin/env python3
"""
Test script to verify the GUI can be imported and initialized without errors.
"""

import sys
import os
import pytest

# Add the project to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_gui_import_and_instantiation():
    """
    Tests that the GUI can be imported and instantiated.
    It expects instantiation to fail gracefully in a headless environment.
    """
    try:
        # Test importing the GUI module
        from highlighter.gui import ModernHighlighterGUI
        print("✅ GUI module imported successfully")
    except ImportError as e:
        pytest.fail(f"❌ GUI module import failed: {e}")

    # Test creating a GUI instance (should fail gracefully without a display)
    try:
        app = ModernHighlighterGUI()
        # If this succeeds, we must clean up
        app.root.destroy()
        pytest.fail("❌ GUI instantiation succeeded unexpectedly in a headless environment.")
    except Exception as e:
        if "no display" in str(e).lower() or "display" in str(e).lower():
            print("✅ GUI instantiation failed as expected in a headless environment.")
        else:
            pytest.fail(f"❌ GUI instantiation failed with an unexpected error: {e}")

def test_cli_integration():
    """
    Tests that the GUI command can be invoked via the CLI.
    """
    from typer.testing import CliRunner
    from unittest.mock import patch
    from highlighter import app as cli_app

    runner = CliRunner()

    with patch('highlighter.gui.main') as mock_gui_main:
        result = runner.invoke(cli_app, ["gui"])
        assert result.exit_code == 0, f"CLI command failed with exit code {result.exit_code}:\n{result.stdout}"
        mock_gui_main.assert_called_once()
        print("✅ 'gui' command successfully invoked the GUI main function.")
