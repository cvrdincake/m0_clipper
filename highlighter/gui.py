#!/usr/bin/env python3
"""
Simple GUI client for the auto-highlighter tool.
Provides drag-and-drop functionality for VOD video files.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import pathlib
import tempfile
from typing import Optional

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    print("Warning: tkinterdnd2 not available. Drag-and-drop functionality will be disabled.")

from . import analyzer, processor
from .common import similarity


class HighlighterGUI:
    def __init__(self):
        # Create main window with drag-and-drop support if available
        if DND_AVAILABLE:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()
            
        self.root.title("Auto Highlighter - VOD Clip Generator")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.current_video_path = tk.StringVar()
        self.output_directory = tk.StringVar(value=os.path.join(os.getcwd(), "highlights"))
        self.decibel_threshold = tk.DoubleVar(value=-15.0)  # More reasonable default for gaming
        self.clip_length = tk.IntVar(value=30)  # Total clip length in seconds
        self.verbose_logging = tk.BooleanVar(value=False)
        
        # Analysis state
        self.is_analyzing = False
        self.analysis_thread: Optional[threading.Thread] = None
        self.temp_dir = tempfile.TemporaryDirectory()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="⚡ Auto Highlighter ⚡", 
                               font=('TkDefaultFont', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Video file selection
        self.setup_video_selection(main_frame, row=1)
        
        # Settings section
        self.setup_settings_section(main_frame, row=2)
        
        # Control buttons
        self.setup_control_buttons(main_frame, row=3)
        
        # Progress and results
        self.setup_progress_section(main_frame, row=4)
        
    def setup_video_selection(self, parent, row):
        """Set up the video file selection area."""
        # Video file section
        video_frame = ttk.LabelFrame(parent, text="Video File", padding="10")
        video_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        video_frame.columnconfigure(1, weight=1)
        
        # Drag and drop area
        if DND_AVAILABLE:
            self.drop_frame = tk.Frame(video_frame, bg='lightgray', height=60, 
                                     relief=tk.RAISED, borderwidth=2)
            self.drop_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
            self.drop_frame.columnconfigure(0, weight=1)
            
            drop_label = tk.Label(self.drop_frame, text="📁 Drag and drop a video file here, or click Browse", 
                                bg='lightgray', font=('TkDefaultFont', 10))
            drop_label.grid(row=0, column=0, pady=20)
            
            # Register drop target
            self.drop_frame.drop_target_register(DND_FILES)
            self.drop_frame.dnd_bind('<<Drop>>', self.on_file_drop)
            
            # Make drop area clickable
            self.drop_frame.bind("<Button-1>", lambda e: self.browse_video_file())
            drop_label.bind("<Button-1>", lambda e: self.browse_video_file())
        else:
            # Fallback: just a button if DND not available
            fallback_frame = tk.Frame(video_frame, bg='lightblue', height=60, 
                                    relief=tk.RAISED, borderwidth=2)
            fallback_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
            fallback_frame.columnconfigure(0, weight=1)
            
            fallback_label = tk.Label(fallback_frame, text="📁 Click here to browse for a video file", 
                                    bg='lightblue', font=('TkDefaultFont', 10))
            fallback_label.grid(row=0, column=0, pady=20)
            
            # Make fallback area clickable
            fallback_frame.bind("<Button-1>", lambda e: self.browse_video_file())
            fallback_label.bind("<Button-1>", lambda e: self.browse_video_file())
        
        # File path display
        ttk.Label(video_frame, text="Selected file:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.file_entry = ttk.Entry(video_frame, textvariable=self.current_video_path, state='readonly')
        self.file_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=(5, 0))
        
        # Browse button
        browse_btn = ttk.Button(video_frame, text="Browse...", command=self.browse_video_file)
        browse_btn.grid(row=1, column=2, padx=(5, 0), pady=(5, 0))
        
    def setup_settings_section(self, parent, row):
        """Set up the settings configuration section."""
        settings_frame = ttk.LabelFrame(parent, text="Analysis Settings", padding="10")
        settings_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        current_row = 0
        
        # Output directory
        ttk.Label(settings_frame, text="Output directory:").grid(row=current_row, column=0, sticky=tk.W)
        output_frame = ttk.Frame(settings_frame)
        output_frame.grid(row=current_row, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(5, 0))
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_directory)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        output_browse_btn = ttk.Button(output_frame, text="Browse...", command=self.browse_output_directory)
        output_browse_btn.grid(row=0, column=1, padx=(5, 0))
        
        current_row += 1
        
        # Decibel threshold
        ttk.Label(settings_frame, text="Decibel threshold:").grid(row=current_row, column=0, sticky=tk.W, pady=(5, 0))
        threshold_frame = ttk.Frame(settings_frame)
        threshold_frame.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=(5, 0))
        
        threshold_scale = ttk.Scale(threshold_frame, from_=-20.0, to=10.0, 
                                  variable=self.decibel_threshold, orient=tk.HORIZONTAL)
        threshold_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        threshold_frame.columnconfigure(0, weight=1)
        
        self.threshold_label = ttk.Label(threshold_frame, text=f"{self.decibel_threshold.get():.1f} dB")
        self.threshold_label.grid(row=0, column=1, padx=(5, 0))
        
        # Update label when scale changes
        threshold_scale.configure(command=lambda val: self.threshold_label.configure(text=f"{float(val):.1f} dB"))
        
        current_row += 1
        
        # Clip length setting
        ttk.Label(settings_frame, text="Clip length:").grid(row=current_row, column=0, sticky=tk.W, pady=(5, 0))
        clip_frame = ttk.Frame(settings_frame)
        clip_frame.grid(row=current_row, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=(5, 0))
        
        clip_spin = ttk.Spinbox(clip_frame, from_=10, to=120, width=8, textvariable=self.clip_length)
        clip_spin.grid(row=0, column=0)
        
        ttk.Label(clip_frame, text="seconds (centered on highlight)").grid(row=0, column=1, padx=(5, 0))
        
        current_row += 1
        
        # Additional options
        verbose_check = ttk.Checkbutton(settings_frame, text="Verbose logging", variable=self.verbose_logging)
        verbose_check.grid(row=current_row, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
    def setup_control_buttons(self, parent, row):
        """Set up the control buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=2, pady=(0, 10))
        
        # Reference analysis button
        self.reference_btn = ttk.Button(button_frame, text="📊 Analyze Reference", 
                                      command=self.analyze_reference)
        self.reference_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Start analysis button
        self.analyze_btn = ttk.Button(button_frame, text="🎬 Generate Highlights", 
                                    command=self.start_analysis, style='Accent.TButton')
        self.analyze_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Open output folder button
        self.open_folder_btn = ttk.Button(button_frame, text="📁 Open Output Folder", 
                                        command=self.open_output_folder)
        self.open_folder_btn.grid(row=0, column=2)
        
    def setup_progress_section(self, parent, row):
        """Set up the progress and results section."""
        progress_frame = ttk.LabelFrame(parent, text="Progress", padding="10")
        progress_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        parent.rowconfigure(row, weight=1)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Status text
        self.status_text = tk.Text(progress_frame, height=8, wrap=tk.WORD, state='disabled')
        self.status_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        progress_frame.rowconfigure(1, weight=1)
        
        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(progress_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
    def on_file_drop(self, event):
        """Handle file drop event."""
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0]
            # Check if it's a video file (basic check)
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
            if pathlib.Path(file_path).suffix.lower() in video_extensions:
                self.current_video_path.set(file_path)
                self.log_message(f"Video file loaded: {os.path.basename(file_path)}")
            else:
                messagebox.showerror("Invalid File", "Please drop a video file.")
                
    def browse_video_file(self):
        """Open file dialog to select video file."""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.current_video_path.set(file_path)
            self.log_message(f"Video file selected: {os.path.basename(file_path)}")
            
    def browse_output_directory(self):
        """Open directory dialog to select output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_directory.set(directory)
            
    def log_message(self, message):
        """Add a message to the status text area."""
        self.status_text.configure(state='normal')
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.configure(state='disabled')
        self.status_text.see(tk.END)
        self.root.update_idletasks()
        
    def analyze_reference(self):
        """Analyze the reference video to get decibel information."""
        if not self.current_video_path.get():
            messagebox.showerror("No Video", "Please select a video file first.")
            return
            
        if not os.path.exists(self.current_video_path.get()):
            messagebox.showerror("File Not Found", "The selected video file does not exist.")
            return
            
        self.log_message("Starting reference analysis...")
        
        def run_reference_analysis():
            try:
                self.root.after(0, lambda: self.log_message("Extracting audio from video..."))
                
                # Extract audio
                audio_path = processor.extract_audio_from_video(
                    self.current_video_path.get(), 
                    self.temp_dir.name
                )
                
                self.root.after(0, lambda: self.log_message("Analyzing audio characteristics..."))
                
                # Analyze audio
                audio_processor = processor.AudioProcessor(audio_path)
                avg_db = audio_processor.get_avg_decibel()
                max_db = audio_processor.get_max_decibel()
                
                # Better threshold calculation for gaming content
                # Use multiple recommendations based on content type
                db_range = max_db - avg_db
                
                # Conservative (fewer clips, only very loud moments)
                conservative_threshold = max_db - 2.0
                
                # Balanced (good for most gaming content)
                balanced_threshold = avg_db + (db_range * 0.6)
                
                # Aggressive (more clips, catches quieter highlights)
                aggressive_threshold = avg_db + (db_range * 0.4)
                
                # Default to balanced
                recommended_threshold = balanced_threshold
                
                # Update UI in main thread
                self.root.after(0, lambda: self.show_reference_results(
                    avg_db, max_db, recommended_threshold, 
                    conservative_threshold, balanced_threshold, aggressive_threshold
                ))
                
            except RuntimeError as e:
                error_msg = str(e)
                self.root.after(0, lambda: self.show_ffmpeg_error(error_msg))
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self.log_message(f"Reference analysis failed: {error_msg}"))
                
        # Run in separate thread
        thread = threading.Thread(target=run_reference_analysis, daemon=True)
        thread.start()
        
    def show_reference_results(self, avg_db, max_db, recommended_threshold, 
                               conservative_threshold, balanced_threshold, aggressive_threshold):
        """Show reference analysis results with multiple threshold options."""
        self.log_message(f"Reference Analysis Complete:")
        self.log_message(f"  Average Decibel: {avg_db:.1f} dB")
        self.log_message(f"  Maximum Decibel: {max_db:.1f} dB")
        self.log_message(f"  Dynamic Range: {max_db - avg_db:.1f} dB")
        self.log_message("")
        self.log_message("Threshold Recommendations:")
        self.log_message(f"  🎯 Balanced (Recommended): {balanced_threshold:.1f} dB")
        self.log_message(f"  🔒 Conservative (Fewer clips): {conservative_threshold:.1f} dB") 
        self.log_message(f"  🔓 Aggressive (More clips): {aggressive_threshold:.1f} dB")
        
        # Create a custom dialog with multiple options
        self.show_threshold_options_dialog(
            balanced_threshold, conservative_threshold, aggressive_threshold
        )
            
    def show_threshold_options_dialog(self, balanced, conservative, aggressive):
        """Show dialog with multiple threshold options."""
        import tkinter as tk
        from tkinter import ttk
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Choose Threshold Setting")
        dialog.geometry("450x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"450x300+{x}+{y}")
        
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Select Threshold Setting", 
                 font=('TkDefaultFont', 12, 'bold')).pack(pady=(0, 15))
        
        # Threshold options
        threshold_var = tk.StringVar(value="balanced")
        
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Balanced option (recommended)
        balanced_frame = ttk.Frame(options_frame)
        balanced_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(balanced_frame, text=f"🎯 Balanced: {balanced:.1f} dB (Recommended)", 
                       variable=threshold_var, value="balanced").pack(anchor=tk.W)
        ttk.Label(balanced_frame, text="Good balance for most gaming content", 
                 foreground="gray", font=('TkDefaultFont', 9)).pack(anchor=tk.W, padx=(20, 0))
        
        # Conservative option
        conservative_frame = ttk.Frame(options_frame)
        conservative_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(conservative_frame, text=f"🔒 Conservative: {conservative:.1f} dB", 
                       variable=threshold_var, value="conservative").pack(anchor=tk.W)
        ttk.Label(conservative_frame, text="Fewer clips, only very loud moments", 
                 foreground="gray", font=('TkDefaultFont', 9)).pack(anchor=tk.W, padx=(20, 0))
        
        # Aggressive option
        aggressive_frame = ttk.Frame(options_frame)
        aggressive_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(aggressive_frame, text=f"🔓 Aggressive: {aggressive:.1f} dB", 
                       variable=threshold_var, value="aggressive").pack(anchor=tk.W)
        ttk.Label(aggressive_frame, text="More clips, catches quieter highlights", 
                 foreground="gray", font=('TkDefaultFont', 9)).pack(anchor=tk.W, padx=(20, 0))
        
        # Manual option
        manual_frame = ttk.Frame(options_frame)
        manual_frame.pack(fill=tk.X, pady=5)
        ttk.Radiobutton(manual_frame, text="✏️ Keep current setting", 
                       variable=threshold_var, value="manual").pack(anchor=tk.W)
        ttk.Label(manual_frame, text=f"Use current threshold: {self.decibel_threshold.get():.1f} dB", 
                 foreground="gray", font=('TkDefaultFont', 9)).pack(anchor=tk.W, padx=(20, 0))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def apply_threshold():
            choice = threshold_var.get()
            if choice == "balanced":
                new_threshold = balanced
            elif choice == "conservative":
                new_threshold = conservative
            elif choice == "aggressive":
                new_threshold = aggressive
            else:  # manual
                dialog.destroy()
                return
                
            self.decibel_threshold.set(new_threshold)
            self.threshold_label.configure(text=f"{new_threshold:.1f} dB")
            self.log_message(f"✅ Threshold updated to {new_threshold:.1f} dB ({choice})")
            dialog.destroy()
        
        ttk.Button(button_frame, text="Apply", command=apply_threshold).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT)
            
    def show_ffmpeg_error(self, error_msg):
        """Show FFmpeg-specific error with helpful guidance."""
        self.log_message(f"❌ FFmpeg Error: {error_msg}")
        
        if "not found" in error_msg.lower():
            messagebox.showerror("FFmpeg Not Found", 
                               "FFmpeg is not installed or not in your PATH.\n\n"
                               "Please install FFmpeg:\n"
                               "• Windows: Download from https://ffmpeg.org or use 'choco install ffmpeg'\n"
                               "• macOS: 'brew install ffmpeg'\n"
                               "• Linux: 'sudo apt install ffmpeg' or similar\n\n"
                               "After installation, restart the application.")
        else:
            messagebox.showerror("FFmpeg Error", 
                               f"FFmpeg failed to process the video:\n\n{error_msg}\n\n"
                               "Please check:\n"
                               "• Video file is not corrupted\n"
                               "• You have write permissions to the output directory\n"
                               "• FFmpeg is properly installed")
            
    def start_analysis(self):
        """Start the highlight analysis process."""
        if self.is_analyzing:
            return
            
        if not self.current_video_path.get():
            messagebox.showerror("No Video", "Please select a video file first.")
            return
            
        if not os.path.exists(self.current_video_path.get()):
            messagebox.showerror("File Not Found", "The selected video file does not exist.")
            return
            
        # Create output directory if it doesn't exist
        output_path = pathlib.Path(self.output_directory.get())
        output_path.mkdir(parents=True, exist_ok=True)
        
        self.is_analyzing = True
        self.analyze_btn.configure(text="⏳ Analyzing...", state='disabled')
        self.progress_bar.start()
        
        self.log_message("Starting highlight analysis...")
        self.log_message(f"Video: {os.path.basename(self.current_video_path.get())}")
        self.log_message(f"Output: {self.output_directory.get()}")
        self.log_message(f"Threshold: {self.decibel_threshold.get():.1f} dB")
        
        # Run analysis in separate thread
        self.analysis_thread = threading.Thread(target=self.run_analysis, daemon=True)
        self.analysis_thread.start()
        
    def run_analysis(self):
        """Run the actual analysis in a background thread."""
        try:
            # Extract audio
            self.root.after(0, lambda: self.log_message("Extracting audio from video..."))
            audio_path = processor.extract_audio_from_video(
                self.current_video_path.get(), 
                self.temp_dir.name
            )
            
            # Create analyzer
            self.root.after(0, lambda: self.log_message("Initializing audio analyzer..."))
            audio_analyzer = analyzer.AudioAnalysis(
                video_path=self.current_video_path.get(),
                audio_path=audio_path,
                output_path=self.output_directory.get(),
                decibel_threshold=self.decibel_threshold.get()
            )
            
            # Set clip length settings (split total length around highlight moment)
            total_length = self.clip_length.get()
            audio_analyzer.start_point = total_length // 2  # Half before
            audio_analyzer.end_point = total_length - audio_analyzer.start_point  # Half after (handles odd numbers)
            
            # Run analysis
            self.root.after(0, lambda: self.log_message("Analyzing audio for highlights..."))
            audio_analyzer.crest_ceiling_algorithm()
            
            # Export results
            self.root.after(0, lambda: self.log_message("Exporting analysis results..."))
            audio_analyzer.export()
            
            # Generate highlight clips
            highlight_count = len(audio_analyzer._captured_result)
            self.root.after(0, lambda: self.log_message(f"Found {highlight_count} highlights to process"))
            
            if highlight_count == 0:
                self.root.after(0, lambda: self.log_message("⚠️ No highlights found! Try lowering the decibel threshold."))
                self.root.after(0, lambda: self.analysis_complete(0))
                return
            
            self.root.after(0, lambda: self.log_message(f"Generating {highlight_count} highlight clips..."))
            audio_analyzer.generate_all_highlights()
            
            # Verify clips were actually created
            self.root.after(0, lambda: self.verify_clips_generated(highlight_count))
            
        except RuntimeError as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.analysis_failed_ffmpeg(error_msg))
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.analysis_failed(error_msg))
            
    def verify_clips_generated(self, expected_count):
        """Verify that video clips were actually generated."""
        import time
        import glob
        
        # Wait a moment for file system to update
        time.sleep(1)
        
        # Count actual video files
        video_pattern = os.path.join(self.output_directory.get(), "*.mp4")
        video_files = glob.glob(video_pattern)
        actual_count = len(video_files)
        
        self.log_message(f"Verification: {actual_count} video files found out of {expected_count} expected")
        
        if actual_count == 0:
            self.log_message("❌ No video clips were generated!")
            self.log_message("This usually means FFmpeg failed to create the clips.")
            self.log_message("Check that FFmpeg is properly installed and in your PATH.")
        elif actual_count < expected_count:
            self.log_message(f"⚠️ Only {actual_count}/{expected_count} clips were generated")
            self.log_message("Some clips may have failed due to FFmpeg errors")
        
        # Complete analysis with actual count
        self.analysis_complete(actual_count)
        
    def analysis_complete(self, highlight_count):
        """Handle successful analysis completion."""
        self.is_analyzing = False
        self.progress_bar.stop()
        self.analyze_btn.configure(text="🎬 Generate Highlights", state='normal')
        
        self.log_message(f"✅ Analysis complete! Generated {highlight_count} highlight clips.")
        self.log_message(f"Clips saved to: {self.output_directory.get()}")
        
        if highlight_count > 0:
            messagebox.showinfo("Analysis Complete", 
                               f"Successfully generated {highlight_count} highlight clips!\n\n"
                               f"Clips saved to:\n{self.output_directory.get()}")
        else:
            messagebox.showwarning("No Highlights Found", 
                                  "No highlights were found with the current settings.\n\n"
                                  "Try lowering the decibel threshold or use 'Analyze Reference' "
                                  "to find a better threshold.")
            
    def analysis_failed(self, error_message):
        """Handle analysis failure."""
        self.is_analyzing = False
        self.progress_bar.stop()
        self.analyze_btn.configure(text="🎬 Generate Highlights", state='normal')
        
        self.log_message(f"❌ Analysis failed: {error_message}")
        messagebox.showerror("Analysis Failed", f"Analysis failed with error:\n\n{error_message}")
        
    def analysis_failed_ffmpeg(self, error_message):
        """Handle FFmpeg-specific analysis failure."""
        self.is_analyzing = False
        self.progress_bar.stop()
        self.analyze_btn.configure(text="🎬 Generate Highlights", state='normal')
        
        self.log_message(f"❌ FFmpeg Error: {error_message}")
        
        if "not found" in error_message.lower():
            messagebox.showerror("FFmpeg Not Found", 
                               "FFmpeg is required but not found on your system.\n\n"
                               "Please install FFmpeg:\n"
                               "• Windows: Download from https://ffmpeg.org or use 'choco install ffmpeg'\n"
                               "• macOS: 'brew install ffmpeg'\n"
                               "• Linux: 'sudo apt install ffmpeg'\n\n"
                               "After installation, restart the application.")
        else:
            messagebox.showerror("Video Processing Error", 
                               f"Failed to process video file:\n\n{error_message}\n\n"
                               "Please check:\n"
                               "• Video file is not corrupted\n"
                               "• File format is supported\n"
                               "• You have sufficient disk space")
        
    def open_output_folder(self):
        """Open the output folder in the file manager."""
        output_path = self.output_directory.get()
        if os.path.exists(output_path):
            # Cross-platform way to open folder
            import subprocess
            import sys
            
            if sys.platform == "win32":
                os.startfile(output_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", output_path])
            else:
                subprocess.run(["xdg-open", output_path])
        else:
            messagebox.showerror("Folder Not Found", "Output folder does not exist yet.")
            
    def run(self):
        """Start the GUI application."""
        self.log_message("Auto Highlighter GUI ready! Drop a video file or click Browse to get started.")
        self.root.mainloop()
        
    def __del__(self):
        """Clean up temporary directory."""
        if hasattr(self, 'temp_dir'):
            self.temp_dir.cleanup()


def main():
    """Main entry point for the GUI application."""
    app = HighlighterGUI()
    app.run()


if __name__ == "__main__":
    main()