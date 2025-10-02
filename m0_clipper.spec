# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

block_cipher = None

# Find tbb libraries
tbb_libs = []
if sys.platform == "win32":
    # Look for tbb libraries in the standard library path
    for path in sys.path:
        if "Lib" in path and "site-packages" in path:
            tbb_path = Path(path) / "numba"
            if tbb_path.exists():
                for f in tbb_path.glob("tbb*.dll"):
                    tbb_libs.append((str(f), "."))
                break

a = Analysis(
    ['launch_gui.py'],
    pathex=[],
    binaries=tbb_libs,
    datas=[
        ('highlighter', 'highlighter'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk', 
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinterdnd2',
        'librosa',
        'soundfile',
        'numpy',
        'rich',
        'loguru',
        'typer',
        'psutil',
        'ffmpeg',
        'highlighter.gui',
        'highlighter.gui.main_window',
        'highlighter.gui.components',
        'highlighter.gui.components.video_input',
        'highlighter.gui.components.settings_panel',
        'highlighter.gui.components.control_panel',
        'highlighter.gui.components.status_display',
        'highlighter.gui.services',
        'highlighter.gui.services.analysis_service',
        'highlighter.gui.services.notification_service',
        'highlighter.gui.state',
        'highlighter.gui.state.app_state',
        'highlighter.core',
        'highlighter.core.exceptions',
        'highlighter.core.error_handler',
        'highlighter.core.validation',
        'highlighter.core.logging_config',
        'highlighter.analyzer',
        'highlighter.processor',
        'highlighter.common',
        'highlighter.animations',
        'highlighter.glassmorphism',
        'highlighter.window_effects',
        'highlighter.cyber_effects',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='M0_Clipper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app, True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='simplified-icon.ico',  # Uncomment when you have an ICO file
)