# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launch_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('simplified-icon.png', '.'),
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
        'highlighter.gui',
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
    icon='simplified-icon.png',  # Add icon to executable
)