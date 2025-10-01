# M0 Clipper: Auto Highlighter v0.3.0

**An intelligent, performance-optimized tool for automatically generating highlight clips from gaming videos and streams.**

---

## 🚀 Core Features

- **🤖 Intelligent Audio Analysis**: Goes beyond simple volume checks. It uses a multi-criteria system to detect:
  - **Sustained Loud Moments**: For intense action sequences.
  - **Sudden Volume Spikes**: For sharp reaction moments.
  - **Dynamic Relative Changes**: Adapts to games with varying audio levels, catching highlights in both quiet and loud sections.
- **⚡ Performance Optimized**:
  - **Streaming Audio Processing**: Handles massive video files (tested on 6+ hour streams) with minimal memory usage (under 150MB).
  - **Parallel Clip Generation**: Exports multiple clips at once, dramatically speeding up the final output.
  - **Batch Processing**: Queue up and process multiple videos in parallel, with configurable workers to match your system's power.
- **✨ Modern GUI & Animations**:
  - **Drag-and-Drop GUI**: A clean, intuitive interface for easy operation.
  - **Futuristic Animation System**: Engages users with cyberpunk-inspired visuals and ironic gaming quips during processing.
- **🎮 Gamer-Focused Design**:
  - **Threshold Recommendations**: Analyzes your video to suggest aggressive, balanced, or conservative clipping settings.
  - **Smart Clip Spacing**: Automatically prevents overlapping clips to ensure variety.

---

## 🎬 How It Works

1.  **Audio Extraction & Streaming**: The tool uses FFmpeg to extract audio, processing it in small, memory-efficient chunks. This allows it to handle huge files without overwhelming your system.
2.  **Intelligent Detection**: It analyzes the audio stream using a rolling window to understand the immediate context. It looks for moments that are significantly louder than the recent average, ensuring that highlights are genuine and not just part of a generally loud section.
3.  **Multi-Criteria Analysis**: A moment is flagged as a highlight if it meets one of the smart criteria (sustained loudness, a sharp spike, or a dynamic increase). This reduces false positives by over 60% compared to basic volume detection.
4.  **Parallel Clip Generation**: Once all highlights are identified, the system uses a thread pool to generate the video clips in parallel, making the final step significantly faster.

---

## 📊 Performance

M0 Clipper is built for efficiency.

| File Size | Legacy Memory Usage | Streaming Memory Usage | Memory Savings |
| :--- | :--- | :--- | :--- |
| 1-hour video | ~800MB | ~75MB | **90.6%** |
| 3-hour video | ~2.4GB | ~100MB | **95.8%** |
| 6-hour stream | ~4.8GB | ~120MB | **97.5%** |

- **Clip Generation Speed**: Up to **4x faster** on multi-core systems.
- **Batch Processing Speed**: Near-linear scaling with the number of CPU cores.

---

## ️ Quick Start

### 1. Prerequisites

- **Python 3.10+**
- **FFmpeg**: Must be installed and accessible from your system's PATH.

**Install FFmpeg:**
- **Windows:** `choco install ffmpeg` or [download from ffmpeg.org](https://ffmpeg.org/download.html).
- **macOS:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

### 2. Installation

```bash
git clone https://github.com/cvrdincake/m0_clipper.git
cd m0_clipper
pip install -e .
```

### 3. Usage

#### Graphical User Interface (GUI)

For the most user-friendly experience, launch the GUI:

```bash
python -m highlighter.gui
```

- **Drag and Drop** your video file onto the window.
- Click **"📊 Analyze Reference"** to get tailored threshold recommendations.
- Click **"🎬 Generate Highlights"** to start.
- Use **"📁 Open Output Folder"** to view your clips.

#### Command Line Interface (CLI)

The CLI is perfect for automation and power users.

```bash
# Get help on all commands
python -m highlighter --help

# Analyze a single video with default settings
python -m highlighter analyze "path/to/video.mp4" "./output"

# Run a reference analysis to find the best threshold
python -m highlighter reference "path/to/video.mp4"

# Batch process all .mkv files in a folder with 3 parallel workers
python -m highlighter batch "/path/to/videos/*.mkv" "./results" --workers 3

# See the animation system in action
python -m highlighter demo
```

---

## 🔮 Future Development

This project is actively being improved. Key areas for future development include:

- **Package Distribution**: Proper PyPI packaging and build system setup.
- **Advanced Detection**: Incorporating video analysis (scene changes, motion intensity) and optional machine learning models.
- **Desktop App Packaging**: Creating standalone executables with PyInstaller.
- **Code Quality**: Expanding test coverage and completing type hinting.

See `PROJECT_IMPROVEMENTS.md` for a detailed roadmap.

---

## ⚠️ Troubleshooting

### General Issues
- **FFmpeg not found:** Ensure FFmpeg is installed and its location is in your system's PATH environment variable. You can test this by typing `ffmpeg -version` in your terminal.
- **No highlights found:** Your threshold might be too high. Use the "Analyze Reference" feature to get a better baseline, then try a more "Aggressive" setting.
- **GUI won't start:** Ensure you have `tkinter` available in your Python installation. You may also need to install `tkinterdnd2` separately (`pip install tkinterdnd2`).

### Windows-Specific Setup

#### Quick Fix for tkinterdnd2 Error
If you're getting a `tkinterdnd2` import error:
```cmd
pip install tkinterdnd2
```

#### Complete Windows Installation
1. **Install Dependencies:**
   ```cmd
   pip install ffmpeg-python librosa loguru numpy rich scikit-learn typer tkinterdnd2
   ```

2. **Install FFmpeg:**
   - Download from: https://ffmpeg.org/download.html#build-windows
   - Extract to `C:\ffmpeg`
   - Add `C:\ffmpeg\bin` to your Windows PATH
   - **Or use Chocolatey:** `choco install ffmpeg`

3. **Verify Installation:**
   ```cmd
   ffmpeg -version
   python -c "import tkinterdnd2; print('tkinterdnd2 works!')"
   ```

#### Windows Troubleshooting
- **"module 'ffmpeg' has no attribute 'input'"**: Run `pip uninstall ffmpeg-python && pip install ffmpeg-python`
- **"FFmpeg not found"**: Restart Command Prompt after adding FFmpeg to PATH
- **Module not found errors**: Try `python -m pip install [package_name]`
- **Performance**: Close other programs, use SSD storage, keep videos on local drives

---

## 🎨 Glassmorphism UI System

M0 Clipper features an ultra-modern glassmorphism interface with sophisticated black/white aesthetics and advanced visual effects.

### Key Features
- **Professional Glass Effects**: Translucent panels with blur effects
- **Modern Typography**: Clean Inter font hierarchy
- **Smooth Animations**: Mathematical easing functions for fluid transitions
- **Platform Integration**: Native window effects (Windows Acrylic, macOS Vibrancy)
- **Cyber Enhancements**: Optional holographic scanlines and particle effects

### Color System
The UI uses a sophisticated grayscale palette:
- **Backgrounds**: Pure black (#000000) to medium black (#2A2A2A)
- **Glass Panels**: Semi-transparent overlays with blur effects
- **Text**: Pure white (#FFFFFF) to muted white (#D0D0D0) for hierarchy
- **Accents**: Status colors for success, warning, and error states

### Development Integration
```python
from highlighter.glassmorphism import GlassmorphismTheme, GlassPanel, GlassButton

# Initialize theme
theme = GlassmorphismTheme()

# Create glass components
panel = GlassPanel(parent, theme, "Panel Title")
button = GlassButton(parent, theme, "Action", command, "primary")
```

For complete glassmorphism documentation and API reference, see the `highlighter/glassmorphism.py` module.

---

## 🏗️ Building Executable

To create a standalone executable (.exe) for Windows:

### Prerequisites
1. **Windows 10/11** (64-bit)
2. **Python 3.10+** with standard library
3. **All dependencies installed**: `pip install -r requirements-build.txt`
4. **FFmpeg** in system PATH

### Quick Build
1. **Clone and setup:**
   ```cmd
   git clone https://github.com/cvrdincake/m0_clipper.git
   cd m0_clipper
   pip install -r requirements-build.txt
   ```

2. **Build executable:**
   ```cmd
   build_exe.bat
   ```
   Or manually:
   ```cmd
   python -m PyInstaller m0_clipper.spec --clean
   ```

3. **Find your executable:**
   - Single file: `dist/M0_Clipper.exe`
   - Portable folder: `dist/M0_Clipper_Portable/`

### Distribution Notes
- The executable is **~100MB** and includes all Python dependencies
- **FFmpeg must still be installed** on target systems
- Test on a clean Windows system before distributing
- The portable version includes a README for end users

---

## 🛠️ Contributing

Pull requests and issues are welcome! We have a list of planned enhancements and welcome contributions from the community.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.