# Auto Highlighter GUI Client

A simple, clean graphical interface for the Auto Highlighter tool that allows you to drag and drop VOD video files to automatically generate highlight clips.

## Features

- **Drag and Drop Interface**: Simply drag a video file onto the application window
- **Visual Settings Panel**: Easy-to-use controls for configuring analysis parameters
- **Real-time Progress**: Watch the analysis progress and see results as they happen
- **Reference Analysis**: Analyze your video to find the optimal decibel threshold
- **One-Click Output Access**: Open the generated clips folder directly from the app

## Requirements

- Python 3.10+
- FFmpeg (installed and available on PATH)
- All Python dependencies (automatically installed)

## Installation

1. Install dependencies:
```bash
pip install tkinterdnd2 ffmpeg-python librosa loguru numpy rich scikit-learn typer
```

2. Or install everything from the project:
```bash
pip install -e .
```

## Usage

### Option 1: From Command Line
```bash
python -m highlighter gui
```

### Option 2: Direct Launch
```bash
python launch_gui.py
```

## How to Use

1. **Launch the Application**: Use one of the commands above
2. **Load Video File**: 
   - Drag and drop a video file onto the gray area, OR
   - Click "Browse..." to select a file
3. **Configure Settings** (optional):
   - **Output Directory**: Where clips will be saved (default: `./highlights`)
   - **Decibel Threshold**: How loud a moment needs to be to become a clip (default: -5.0 dB)
   - **Clip Length**: How many seconds before/after the highlight moment to include
4. **Find Optimal Settings** (recommended):
   - Click "📊 Analyze Reference" to get statistics about your video
   - Use the recommended threshold value for best results
5. **Generate Highlights**:
   - Click "🎬 Generate Highlights" to start analysis
   - Watch the progress and results in the status area
6. **Access Results**:
   - Click "📁 Open Output Folder" to see your generated clips
   - Review and use the clips as needed

## Settings Explained

### Decibel Threshold
- **Lower values** (e.g., -20.0 dB): More sensitive, captures more moments, may include quieter highlights
- **Higher values** (e.g., -5.0 dB): Less sensitive, only captures very loud moments, fewer clips
- **Recommended approach**: 
  1. Use "Analyze Reference" to get tailored recommendations
  2. Start with the "Balanced" option (usually works best for gaming content)
  3. Adjust based on results - if too many clips, go more Conservative; if too few, go more Aggressive
- **Gaming content tip**: The old recommendation of `max_dB - 1.4` was too conservative. The new balanced approach typically works much better.

### Clip Length
- **Before**: Seconds to include before the highlight moment (default: 20)
- **After**: Seconds to include after the highlight moment (default: 20)
- **Total clip length**: Before + After seconds (default: 40 seconds total)

### Output Directory
- Where generated clips will be saved
- Creates the directory if it doesn't exist
- Each clip is named with a unique ID and timestamp

## Supported Video Formats

- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WMV (.wmv)
- FLV (.flv)
- WebM (.webm)
- M4V (.m4v)

## Troubleshooting

### "No highlights found"
- Try lowering the decibel threshold
- Use "Analyze Reference" to find better settings
- Check if your video has varying audio levels

### "FFmpeg not found"
- Make sure FFmpeg is installed and available on your system PATH
- Test with: `ffmpeg -version` in your terminal

### GUI won't start
- Check that tkinter is available: `python -c "import tkinter"`
- Install missing dependencies: `pip install tkinterdnd2`

### Large video files
- The tool can handle large files, but processing time increases with file size
- Consider using a shorter test video first to verify settings

## Generated Files

The tool creates several files in your output directory:

- **Video clips**: `[ID] - [timestamp].mp4` - The actual highlight clips
- **index.json**: Metadata about all found highlights (timestamps, decibel levels)

## Tips for Best Results

1. **Use Reference Analysis**: Always run this first to understand your video's audio characteristics
2. **Start Conservative**: Begin with a higher threshold and lower it if you need more clips
3. **Test with Shorter Videos**: Verify your settings work before processing very long videos
4. **Check Audio Quality**: Videos with consistent audio levels work best
5. **Adjust Clip Length**: Shorter clips for social media, longer clips for more context

## Command Line Alternative

If you prefer the command line interface:

```bash
# Analyze reference
python -m highlighter reference "path/to/video.mp4"

# Generate highlights
python -m highlighter analyze "path/to/video.mp4" "./highlights" --decibel_threshold -5.0
```