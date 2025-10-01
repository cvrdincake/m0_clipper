#!/usr/bin/env python3
"""
Advanced glassmorphism window effects for M0 Clipper.
Provides platform-specific blur effects, shadows, and modern window styling.
"""

import tkinter as tk
from tkinter import ttk
import platform
import sys
import subprocess
from typing import Optional, Tuple
import ctypes

if platform.system() == "Windows":
    from ctypes import wintypes, windll
else:
    wintypes = None
    windll = None


class WindowEffects:
    """Platform-specific window effects for glassmorphism aesthetics."""
    
    def __init__(self, window: tk.Tk):
        self.window = window
        self.platform = platform.system()
        self.is_blur_enabled = False
        
    def enable_blur_effect(self, blur_type: str = "acrylic") -> bool:
        """Enable platform-specific blur effects."""
        try:
            if self.platform == "Windows":
                return self._enable_windows_blur(blur_type)
            elif self.platform == "Darwin":  # macOS
                return self._enable_macos_blur()
            elif self.platform == "Linux":
                return self._enable_linux_blur()
            else:
                return False
        except Exception as e:
            print(f"Blur effect not available: {e}")
            return False
    
    def _enable_windows_blur(self, blur_type: str = "acrylic") -> bool:
        """Enable Windows 10/11 blur effects."""
        try:
            # Get window handle
            hwnd = self.window.winfo_id()
            
            # Define Windows API constants
            DWM_BB_ENABLE = 0x00000001
            DWM_BB_BLURREGION = 0x00000002
            DWM_BB_TRANSITIONONMAXIMIZED = 0x00000004
            
            class DWM_BLURBEHIND(ctypes.Structure):
                _fields_ = [
                    ("dwFlags", wintypes.DWORD),
                    ("fEnable", wintypes.BOOL),
                    ("hRgnBlur", wintypes.HRGN),
                    ("fTransitionOnMaximized", wintypes.BOOL)
                ]
            
            # Create blur behind structure
            blur_behind = DWM_BLURBEHIND()
            blur_behind.dwFlags = DWM_BB_ENABLE
            blur_behind.fEnable = True
            blur_behind.hRgnBlur = None
            blur_behind.fTransitionOnMaximized = False
            
            # Apply blur effect
            result = windll.dwmapi.DwmEnableBlurBehindWindow(
                hwnd, 
                ctypes.byref(blur_behind)
            )
            
            if result == 0:  # S_OK
                self.is_blur_enabled = True
                
                # Try to enable acrylic effect for Windows 10+
                if blur_type == "acrylic":
                    self._enable_windows_acrylic(hwnd)
                
                return True
            
        except Exception as e:
            print(f"Windows blur failed: {e}")
        
        return False
    
    def _enable_windows_acrylic(self, hwnd) -> bool:
        """Enable Windows 10+ acrylic effect."""
        try:
            # Windows 10 version 1903+ constants
            DWMWA_USE_HOSTBACKDROPBRUSH = 17
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            
            # Enable dark mode
            dark_mode = ctypes.c_int(1)
            windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(dark_mode),
                ctypes.sizeof(dark_mode)
            )
            
            # Enable backdrop brush
            backdrop = ctypes.c_int(1)
            windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_USE_HOSTBACKDROPBRUSH,
                ctypes.byref(backdrop),
                ctypes.sizeof(backdrop)
            )
            
            return True
            
        except Exception as e:
            print(f"Acrylic effect failed: {e}")
            return False
    
    def _enable_macos_blur(self) -> bool:
        """Enable macOS blur effects."""
        try:
            # macOS vibrancy effect (requires PyObjC for full implementation)
            # This is a simplified approach
            self.window.configure(bg='systemTransparent')
            return True
        except Exception:
            return False
    
    def _enable_linux_blur(self) -> bool:
        """Enable Linux blur effects (compositor-dependent)."""
        try:
            # Set window as transparent for compositors like Picom
            self.window.wm_attributes('-alpha', 0.95)
            return True
        except Exception:
            return False
    
    def set_window_transparency(self, alpha: float = 0.95):
        """Set window transparency level."""
        try:
            self.window.wm_attributes('-alpha', alpha)
            return True
        except Exception:
            return False
    
    def remove_title_bar_decorations(self):
        """Create borderless window with custom styling."""
        try:
            self.window.overrideredirect(True)
            return True
        except Exception:
            return False
    
    def add_drop_shadow(self) -> bool:
        """Add drop shadow to window."""
        try:
            if self.platform == "Windows":
                return self._add_windows_shadow()
            elif self.platform == "Darwin":
                return self._add_macos_shadow()
            else:
                return False
        except Exception:
            return False
    
    def _add_windows_shadow(self) -> bool:
        """Add Windows drop shadow."""
        try:
            hwnd = self.window.winfo_id()
            
            # Enable drop shadow
            CS_DROPSHADOW = 0x00020000
            GCL_STYLE = -26
            
            # Get current class style
            current_style = windll.user32.GetClassLongW(hwnd, GCL_STYLE)
            
            # Add drop shadow style
            new_style = current_style | CS_DROPSHADOW
            windll.user32.SetClassLongW(hwnd, GCL_STYLE, new_style)
            
            return True
        except Exception:
            return False
    
    def _add_macos_shadow(self) -> bool:
        """Add macOS drop shadow."""
        try:
            # macOS automatically handles shadows for most windows
            return True
        except Exception:
            return False


class ModernWindowFrame:
    """Custom modern window frame with glassmorphism styling."""
    
    def __init__(self, parent: tk.Tk, title: str = "Modern App"):
        self.parent = parent
        self.title = title
        self.is_maximized = False
        self.normal_geometry = None
        
        # Remove default title bar
        self.parent.overrideredirect(True)
        
        # Create custom title bar
        self.create_title_bar()
        
        # Enable window effects
        self.effects = WindowEffects(parent)
        
        # Bind events for window dragging
        self.bind_drag_events()
    
    def create_title_bar(self):
        """Create custom glassmorphism title bar."""
        self.title_bar = tk.Frame(
            self.parent,
            bg='#1A1A1A',
            height=40,
            relief='flat'
        )
        self.title_bar.pack(fill=tk.X)
        self.title_bar.pack_propagate(False)
        
        # Title bar content frame
        title_content = tk.Frame(self.title_bar, bg='#1A1A1A')
        title_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        
        # App icon and title
        self.title_label = tk.Label(
            title_content,
            text=self.title,
            bg='#1A1A1A',
            fg='#FFFFFF',
            font=('Inter', 12, 'bold'),
            anchor='w'
        )
        self.title_label.pack(side=tk.LEFT, fill=tk.Y)
        
        # Window controls frame
        controls_frame = tk.Frame(title_content, bg='#1A1A1A')
        controls_frame.pack(side=tk.RIGHT)
        
        # Minimize button
        self.minimize_btn = self.create_control_button(
            controls_frame, "−", self.minimize_window
        )
        self.minimize_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Maximize/restore button
        self.maximize_btn = self.create_control_button(
            controls_frame, "□", self.toggle_maximize
        )
        self.maximize_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Close button
        self.close_btn = self.create_control_button(
            controls_frame, "×", self.close_window, hover_color='#FF4444'
        )
        self.close_btn.pack(side=tk.LEFT)
    
    def create_control_button(self, parent, text: str, command, hover_color: str = '#3A3A3A'):
        """Create a modern window control button."""
        btn = tk.Button(
            parent,
            text=text,
            bg='#1A1A1A',
            fg='#FFFFFF',
            font=('Inter', 12, 'bold'),
            relief='flat',
            bd=0,
            width=3,
            height=1,
            command=command,
            cursor='hand2'
        )
        
        # Add hover effects
        def on_enter(event):
            btn.configure(bg=hover_color)
        
        def on_leave(event):
            btn.configure(bg='#1A1A1A')
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def bind_drag_events(self):
        """Bind events for dragging the window."""
        self.start_x = 0
        self.start_y = 0
        
        def start_drag(event):
            self.start_x = event.x_root - self.parent.winfo_rootx()
            self.start_y = event.y_root - self.parent.winfo_rooty()
        
        def drag_window(event):
            if not self.is_maximized:
                x = event.x_root - self.start_x
                y = event.y_root - self.start_y
                self.parent.geometry(f"+{x}+{y}")
        
        def double_click_title(event):
            self.toggle_maximize()
        
        # Bind to title bar elements
        for widget in [self.title_bar, self.title_label]:
            widget.bind("<Button-1>", start_drag)
            widget.bind("<B1-Motion>", drag_window)
            widget.bind("<Double-Button-1>", double_click_title)
    
    def minimize_window(self):
        """Minimize the window."""
        self.parent.iconify()
    
    def toggle_maximize(self):
        """Toggle between maximized and normal window state."""
        if self.is_maximized:
            # Restore to normal size
            if self.normal_geometry:
                self.parent.geometry(self.normal_geometry)
            self.is_maximized = False
            self.maximize_btn.configure(text="□")
        else:
            # Save current geometry and maximize
            self.normal_geometry = self.parent.geometry()
            
            # Get screen dimensions
            screen_width = self.parent.winfo_screenwidth()
            screen_height = self.parent.winfo_screenheight()
            
            # Maximize window
            self.parent.geometry(f"{screen_width}x{screen_height}+0+0")
            self.is_maximized = True
            self.maximize_btn.configure(text="❐")
    
    def close_window(self):
        """Close the window."""
        self.parent.quit()
        self.parent.destroy()
    
    def enable_modern_effects(self):
        """Enable all modern window effects."""
        # Enable blur
        self.effects.enable_blur_effect("acrylic")
        
        # Set transparency
        self.effects.set_window_transparency(0.95)
        
        # Add drop shadow
        self.effects.add_drop_shadow()


class GlassmorphismNotification:
    """Modern notification system with glassmorphism styling."""
    
    def __init__(self, parent):
        self.parent = parent
        self.notifications = []
        self.notification_height = 80
        self.margin = 20
    
    def show_notification(self, title: str, message: str, type: str = "info", 
                         duration: int = 5000):
        """Show a glassmorphism notification."""
        # Create notification window
        notification = tk.Toplevel(self.parent)
        notification.overrideredirect(True)
        notification.configure(bg='#1A1A1A')
        notification.wm_attributes('-topmost', True)
        
        # Position notification
        self.position_notification(notification)
        
        # Create notification content
        self.create_notification_content(notification, title, message, type)
        
        # Store notification
        self.notifications.append(notification)
        
        # Auto-hide after duration
        notification.after(duration, lambda: self.hide_notification(notification))
        
        # Animate in
        self.animate_notification_in(notification)
    
    def position_notification(self, notification):
        """Position notification in the screen."""
        # Get screen dimensions
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        
        # Calculate position
        width = 350
        height = self.notification_height
        x = screen_width - width - self.margin
        y = self.margin + (len(self.notifications) * (height + 10))
        
        notification.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_notification_content(self, notification, title: str, message: str, type: str):
        """Create the notification content with glassmorphism styling."""
        # Main container with glass effect
        container = tk.Frame(
            notification,
            bg='#2A2A2A',
            relief='flat',
            bd=1,
            highlightbackground='#444444',
            highlightthickness=1
        )
        container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Content frame
        content = tk.Frame(container, bg='#2A2A2A')
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        
        # Type indicator
        type_colors = {
            'info': '#FFFFFF',
            'success': '#00FF88',
            'warning': '#FFAA00',
            'error': '#FF4444'
        }
        
        indicator = tk.Label(
            content,
            text="●",
            bg='#2A2A2A',
            fg=type_colors.get(type, '#FFFFFF'),
            font=('Inter', 16)
        )
        indicator.pack(side=tk.LEFT, padx=(0, 12))
        
        # Text content
        text_frame = tk.Frame(content, bg='#2A2A2A')
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            text_frame,
            text=title,
            bg='#2A2A2A',
            fg='#FFFFFF',
            font=('Inter', 11, 'bold'),
            anchor='w'
        )
        title_label.pack(fill=tk.X)
        
        # Message
        message_label = tk.Label(
            text_frame,
            text=message,
            bg='#2A2A2A',
            fg='#CCCCCC',
            font=('Inter', 9),
            anchor='w',
            wraplength=250
        )
        message_label.pack(fill=tk.X, pady=(2, 0))
        
        # Close button
        close_btn = tk.Button(
            content,
            text="×",
            bg='#2A2A2A',
            fg='#FFFFFF',
            font=('Inter', 12, 'bold'),
            relief='flat',
            bd=0,
            width=2,
            command=lambda: self.hide_notification(notification),
            cursor='hand2'
        )
        close_btn.pack(side=tk.RIGHT, padx=(12, 0))
        
        # Add hover effect to close button
        def on_enter(event):
            close_btn.configure(bg='#444444')
        
        def on_leave(event):
            close_btn.configure(bg='#2A2A2A')
        
        close_btn.bind("<Enter>", on_enter)
        close_btn.bind("<Leave>", on_leave)
    
    def animate_notification_in(self, notification):
        """Animate notification sliding in."""
        # Start from right edge
        original_x = notification.winfo_x()
        start_x = original_x + 350
        
        notification.geometry(f"350x{self.notification_height}+{start_x}+{notification.winfo_y()}")
        
        # Animate to final position
        steps = 20
        step_size = (start_x - original_x) // steps
        
        def animate_step(step):
            if step < steps:
                current_x = start_x - (step * step_size)
                notification.geometry(f"350x{self.notification_height}+{current_x}+{notification.winfo_y()}")
                notification.after(10, lambda: animate_step(step + 1))
            else:
                notification.geometry(f"350x{self.notification_height}+{original_x}+{notification.winfo_y()}")
        
        animate_step(0)
    
    def hide_notification(self, notification):
        """Hide and destroy notification."""
        if notification in self.notifications:
            self.notifications.remove(notification)
        
        # Animate out
        def animate_out():
            try:
                current_x = notification.winfo_x()
                target_x = current_x + 350
                
                def slide_out(step):
                    if step < 20:
                        new_x = current_x + (step * 17)
                        notification.geometry(f"350x{self.notification_height}+{new_x}+{notification.winfo_y()}")
                        notification.after(5, lambda: slide_out(step + 1))
                    else:
                        notification.destroy()
                
                slide_out(0)
            except tk.TclError:
                # Window already destroyed
                pass
        
        animate_out()


# Example usage
def create_modern_window_demo():
    """Create a demonstration of modern window effects."""
    root = tk.Tk()
    root.geometry("800x600")
    root.configure(bg='#0A0A0A')
    
    # Create modern frame
    modern_frame = ModernWindowFrame(root, "Modern Glassmorphism App")
    
    # Enable effects
    modern_frame.enable_modern_effects()
    
    # Create content
    content_frame = tk.Frame(root, bg='#0A0A0A')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Add some demo content
    demo_label = tk.Label(
        content_frame,
        text="Modern Glassmorphism Window",
        bg='#0A0A0A',
        fg='#FFFFFF',
        font=('Inter', 24, 'bold')
    )
    demo_label.pack(pady=50)
    
    # Notification system
    notifications = GlassmorphismNotification(root)
    
    # Demo buttons
    def show_info():
        notifications.show_notification("Info", "This is an info notification", "info")
    
    def show_success():
        notifications.show_notification("Success", "Operation completed successfully!", "success")
    
    def show_warning():
        notifications.show_notification("Warning", "Please check your settings", "warning")
    
    def show_error():
        notifications.show_notification("Error", "Something went wrong", "error")
    
    button_frame = tk.Frame(content_frame, bg='#0A0A0A')
    button_frame.pack(pady=30)
    
    buttons = [
        ("Info Notification", show_info),
        ("Success Notification", show_success),
        ("Warning Notification", show_warning),
        ("Error Notification", show_error)
    ]
    
    for text, command in buttons:
        btn = tk.Button(
            button_frame,
            text=text,
            bg='#2A2A2A',
            fg='#FFFFFF',
            font=('Inter', 10),
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            command=command,
            cursor='hand2'
        )
        btn.pack(side=tk.LEFT, padx=5)
        
        # Add hover effects
        def on_enter(event, b=btn):
            b.configure(bg='#3A3A3A')
        
        def on_leave(event, b=btn):
            b.configure(bg='#2A2A2A')
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    return root


if __name__ == "__main__":
    demo = create_modern_window_demo()
    demo.mainloop()