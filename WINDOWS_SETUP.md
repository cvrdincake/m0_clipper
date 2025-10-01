# Windows Installation Guide for Auto Highlighter GUI

## Quick Fix for Your Error

You're getting an error because `tkinterdnd2` is not installed. Here's how to fix it:

### Option 1: Install tkinterdnd2 (Recommended)
```cmd
pip install tkinterdnd2
```

After installation, run the GUI again:
```cmd
python launch_gui.py
```

### Option 2: Use Without Drag-and-Drop
If you can't install tkinterdnd2, the GUI will still work! You just won't have drag-and-drop functionality, but you can still browse for files using the "Browse..." button.

## Complete Windows Setup

### 1. Install Python Dependencies
```cmd
pip install ffmpeg-python librosa loguru numpy rich scikit-learn typer tkinterdnd2
```

### 2. Install FFmpeg
1. Download FFmpeg from: https://ffmpeg.org/download.html#build-windows
2. Extract to a folder like `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your Windows PATH:
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Click "Environment Variables"
   - Under "System Variables", find and select "Path", click "Edit"
   - Click "New" and add `C:\ffmpeg\bin`
   - Click "OK" on all windows

### 3. Verify Installation
Open a new Command Prompt and test:
```cmd
ffmpeg -version
python -c "import tkinterdnd2; print('tkinterdnd2 works!')"
```

### 4. Run the GUI
```cmd
python launch_gui.py
```

## Alternative: Use Chocolatey (Easier)

If you have Chocolatey installed:
```cmd
choco install ffmpeg
pip install ffmpeg-python librosa loguru numpy rich scikit-learn typer tkinterdnd2
```

## Troubleshooting

### "FFmpeg not found"
- Make sure FFmpeg is in your PATH
- Restart Command Prompt after adding to PATH
- Test with: `ffmpeg -version`

### "Module not found" errors
- Make sure you're using the right Python environment
- Try: `python -m pip install [package_name]` instead of just `pip install`

### GUI won't start
- Check if you're running from the correct directory
- Make sure all Python files are in the right location

### Still having issues?
- Use the command line version instead: `python -m highlighter analyze`
- Or try the alternative launcher: `python -m highlighter gui`

## Performance Tips for Windows

1. **Close other programs** during analysis to free up CPU
2. **Use SSD storage** for faster video processing if available
3. **Test with shorter videos first** to verify everything works
4. **Keep videos on local drives** rather than network drives for better performance