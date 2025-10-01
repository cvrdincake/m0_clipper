#!/usr/bin/env python3
"""
Advanced cyber UI elements and effects for glassmorphism M0 Clipper.
Includes holographic effects, scanning lines, particle systems, and glitch transitions.
"""

import tkinter as tk
from tkinter import Canvas
import math
import random
import threading
import time
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Particle:
    """Data class for particle effects."""
    x: float
    y: float
    vx: float
    vy: float
    size: float
    color: str
    alpha: float
    life: float


class HolographicScanline:
    """Holographic scanning line effect for glassmorphism panels."""
    
    def __init__(self, canvas: Canvas, width: int, height: int, colors: List[str]):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.colors = colors
        self.position = 0
        self.direction = 1
        self.speed = 2
        self.is_running = False
        self.line_id = None
        
    def start(self):
        """Start the scanning animation."""
        self.is_running = True
        self.animate()
    
    def stop(self):
        """Stop the scanning animation."""
        self.is_running = False
        if self.line_id:
            self.canvas.delete(self.line_id)
    
    def animate(self):
        """Animate the scanning line."""
        if not self.is_running:
            return
            
        # Clear previous line
        if self.line_id:
            self.canvas.delete(self.line_id)
        
        # Create gradient effect
        color = random.choice(self.colors)
        
        # Draw scanning line with opacity effect
        self.line_id = self.canvas.create_line(
            0, self.position,
            self.width, self.position,
            fill=color,
            width=3,
            smooth=True
        )
        
        # Update position
        self.position += self.speed * self.direction
        
        # Bounce at edges
        if self.position >= self.height or self.position <= 0:
            self.direction *= -1
        
        # Schedule next frame
        self.canvas.after(50, self.animate)


class ParticleSystem:
    """Particle system for cyberpunk effects."""
    
    def __init__(self, canvas: Canvas, width: int, height: int):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.particles: List[Particle] = []
        self.is_running = False
        self.particle_ids = []
        
    def add_particle(self, x: float, y: float, color: str = "#FFFFFF"):
        """Add a new particle to the system."""
        particle = Particle(
            x=x,
            y=y,
            vx=random.uniform(-2, 2),
            vy=random.uniform(-3, -1),
            size=random.uniform(1, 3),
            color=color,
            alpha=1.0,
            life=1.0
        )
        self.particles.append(particle)
    
    def start(self):
        """Start the particle system."""
        self.is_running = True
        self.update()
    
    def stop(self):
        """Stop the particle system."""
        self.is_running = False
        for particle_id in self.particle_ids:
            self.canvas.delete(particle_id)
        self.particle_ids.clear()
        self.particles.clear()
    
    def update(self):
        """Update all particles."""
        if not self.is_running:
            return
            
        # Clear previous particles
        for particle_id in self.particle_ids:
            self.canvas.delete(particle_id)
        self.particle_ids.clear()
        
        # Update and draw particles
        alive_particles = []
        
        for particle in self.particles:
            # Update position
            particle.x += particle.vx
            particle.y += particle.vy
            
            # Update life and alpha
            particle.life -= 0.02
            particle.alpha = max(0, particle.life)
            
            # Apply gravity
            particle.vy += 0.1
            
            # Keep alive particles
            if particle.life > 0 and 0 <= particle.x <= self.width and 0 <= particle.y <= self.height:
                alive_particles.append(particle)
                
                # Draw particle
                particle_id = self.canvas.create_oval(
                    particle.x - particle.size,
                    particle.y - particle.size,
                    particle.x + particle.size,
                    particle.y + particle.size,
                    fill=particle.color,
                    outline="",
                    stipple="gray50" if particle.alpha < 0.5 else ""
                )
                self.particle_ids.append(particle_id)
        
        self.particles = alive_particles
        
        # Add new particles occasionally
        if random.random() < 0.1:
            self.add_particle(
                random.uniform(0, self.width),
                self.height + 10,
                random.choice(["#FFFFFF", "#E0E0E0", "#CCCCCC"])
            )
        
        # Schedule next frame
        self.canvas.after(33, self.update)  # ~30 FPS


class GlitchEffect:
    """Digital glitch effect for cyberpunk aesthetics."""
    
    def __init__(self, widget: tk.Widget):
        self.widget = widget
        self.original_colors = {}
        self.is_glitching = False
        
    def start_glitch(self, duration: float = 1.0):
        """Start glitch effect."""
        if self.is_glitching:
            return
            
        self.is_glitching = True
        
        # Store original colors
        try:
            self.original_colors = {
                'bg': self.widget.cget('bg'),
                'fg': self.widget.cget('fg') if hasattr(self.widget, 'fg') else None
            }
        except:
            pass
        
        # Start glitch animation
        self.glitch_frame(0, int(duration * 30))  # 30 FPS
    
    def glitch_frame(self, current_frame: int, total_frames: int):
        """Animate a single glitch frame."""
        if not self.is_glitching or current_frame >= total_frames:
            self.stop_glitch()
            return
        
        # Random glitch colors
        glitch_colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFFFF", "#000000"]
        
        if random.random() < 0.3:  # 30% chance of glitch
            try:
                glitch_bg = random.choice(glitch_colors)
                self.widget.configure(bg=glitch_bg)
                
                if self.original_colors.get('fg'):
                    glitch_fg = random.choice(glitch_colors)
                    self.widget.configure(fg=glitch_fg)
            except:
                pass
        else:
            # Restore original colors occasionally
            try:
                self.widget.configure(bg=self.original_colors['bg'])
                if self.original_colors.get('fg'):
                    self.widget.configure(fg=self.original_colors['fg'])
            except:
                pass
        
        # Schedule next frame
        self.widget.after(33, lambda: self.glitch_frame(current_frame + 1, total_frames))
    
    def stop_glitch(self):
        """Stop glitch effect and restore original appearance."""
        self.is_glitching = False
        
        try:
            self.widget.configure(bg=self.original_colors['bg'])
            if self.original_colors.get('fg'):
                self.widget.configure(fg=self.original_colors['fg'])
        except:
            pass


class CyberProgressRing:
    """Cyberpunk-style circular progress indicator."""
    
    def __init__(self, parent: tk.Widget, size: int = 100, thickness: int = 8):
        self.parent = parent
        self.size = size
        self.thickness = thickness
        self.progress = 0.0
        self.is_indeterminate = False
        self.rotation = 0
        
        # Create canvas
        self.canvas = Canvas(
            parent,
            width=size,
            height=size,
            bg="#1A1A1A",
            highlightthickness=0
        )
        
        # Colors
        self.bg_color = "#333333"
        self.progress_color = "#FFFFFF"
        self.glow_color = "#E0E0E0"
        
        self.draw()
    
    def pack(self, **kwargs):
        """Pack the canvas."""
        self.canvas.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid the canvas."""
        self.canvas.grid(**kwargs)
    
    def place(self, **kwargs):
        """Place the canvas."""
        self.canvas.place(**kwargs)
    
    def set_progress(self, value: float):
        """Set progress value (0.0 to 1.0)."""
        self.progress = max(0.0, min(1.0, value))
        self.is_indeterminate = False
        self.draw()
    
    def set_indeterminate(self, enabled: bool = True):
        """Enable/disable indeterminate mode."""
        self.is_indeterminate = enabled
        if enabled:
            self.animate_indeterminate()
        else:
            self.draw()
    
    def draw(self):
        """Draw the progress ring."""
        self.canvas.delete("all")
        
        center = self.size // 2
        radius = (self.size - self.thickness) // 2
        
        # Draw background ring
        self.canvas.create_oval(
            center - radius,
            center - radius,
            center + radius,
            center + radius,
            outline=self.bg_color,
            width=self.thickness,
            fill=""
        )
        
        if self.is_indeterminate:
            # Draw animated arc for indeterminate mode
            start_angle = self.rotation
            extent = 90
        else:
            # Draw progress arc
            start_angle = -90  # Start at top
            extent = 360 * self.progress
        
        if extent > 0:
            # Main progress arc
            self.canvas.create_arc(
                center - radius,
                center - radius,
                center + radius,
                center + radius,
                start=start_angle,
                extent=extent,
                outline=self.progress_color,
                width=self.thickness,
                style="arc"
            )
            
            # Glow effect
            if self.thickness > 4:
                self.canvas.create_arc(
                    center - radius,
                    center - radius,
                    center + radius,
                    center + radius,
                    start=start_angle,
                    extent=extent,
                    outline=self.glow_color,
                    width=max(1, self.thickness // 4),
                    style="arc"
                )
    
    def animate_indeterminate(self):
        """Animate indeterminate progress."""
        if not self.is_indeterminate:
            return
            
        self.rotation = (self.rotation + 10) % 360
        self.draw()
        
        # Schedule next frame
        self.canvas.after(50, self.animate_indeterminate)


class MatrixRain:
    """Matrix-style digital rain effect."""
    
    def __init__(self, canvas: Canvas, width: int, height: int):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.columns = width // 20
        self.drops = [0] * self.columns
        self.is_running = False
        
        # Matrix characters
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def start(self):
        """Start the matrix rain effect."""
        self.is_running = True
        self.animate()
    
    def stop(self):
        """Stop the matrix rain effect."""
        self.is_running = False
        self.canvas.delete("matrix")
    
    def animate(self):
        """Animate the matrix rain."""
        if not self.is_running:
            return
            
        # Clear previous frame
        self.canvas.delete("matrix")
        
        # Draw falling characters
        for i in range(self.columns):
            # Random character
            char = random.choice(self.chars)
            
            # Position
            x = i * 20
            y = self.drops[i] * 20
            
            # Color based on position (fade effect)
            if y < self.height:
                alpha = max(0.1, 1.0 - (y / self.height))
                
                if alpha > 0.7:
                    color = "#FFFFFF"
                elif alpha > 0.4:
                    color = "#CCCCCC"
                else:
                    color = "#666666"
                
                # Draw character
                self.canvas.create_text(
                    x, y,
                    text=char,
                    fill=color,
                    font=("Courier", 12, "bold"),
                    tags="matrix"
                )
            
            # Update drop position
            if y > self.height and random.random() > 0.975:
                self.drops[i] = 0
            else:
                self.drops[i] += 1
        
        # Schedule next frame
        self.canvas.after(100, self.animate)


class CyberEnhancedWidget:
    """Wrapper class to add cyber effects to any widget."""
    
    def __init__(self, widget: tk.Widget):
        self.widget = widget
        self.scanline = None
        self.particles = None
        self.glitch = None
        self.canvas_overlay = None
        
    def add_scanline_effect(self, colors: List[str] = None):
        """Add holographic scanline effect."""
        if colors is None:
            colors = ["#FFFFFF", "#E0E0E0", "#CCCCCC"]
        
        # Create overlay canvas
        if not self.canvas_overlay:
            self.canvas_overlay = Canvas(
                self.widget,
                highlightthickness=0,
                bg=""
            )
            self.canvas_overlay.place(relwidth=1, relheight=1)
        
        # Get widget dimensions
        self.widget.update_idletasks()
        width = self.widget.winfo_width()
        height = self.widget.winfo_height()
        
        self.scanline = HolographicScanline(self.canvas_overlay, width, height, colors)
        self.scanline.start()
    
    def add_particle_effect(self):
        """Add particle system effect."""
        if not self.canvas_overlay:
            self.canvas_overlay = Canvas(
                self.widget,
                highlightthickness=0,
                bg=""
            )
            self.canvas_overlay.place(relwidth=1, relheight=1)
        
        # Get widget dimensions
        self.widget.update_idletasks()
        width = self.widget.winfo_width()
        height = self.widget.winfo_height()
        
        self.particles = ParticleSystem(self.canvas_overlay, width, height)
        self.particles.start()
    
    def add_glitch_effect(self, duration: float = 1.0):
        """Add glitch effect."""
        if not self.glitch:
            self.glitch = GlitchEffect(self.widget)
        
        self.glitch.start_glitch(duration)
    
    def stop_all_effects(self):
        """Stop all cyber effects."""
        if self.scanline:
            self.scanline.stop()
        
        if self.particles:
            self.particles.stop()
        
        if self.glitch:
            self.glitch.stop_glitch()
        
        if self.canvas_overlay:
            self.canvas_overlay.destroy()
            self.canvas_overlay = None


class CyberBackground:
    """Animated cyber background for the main window."""
    
    def __init__(self, parent: tk.Widget, width: int, height: int):
        self.parent = parent
        self.width = width
        self.height = height
        
        # Create background canvas
        self.canvas = Canvas(
            parent,
            width=width,
            height=height,
            bg="#0A0A0A",
            highlightthickness=0
        )
        
        # Effects
        self.matrix = MatrixRain(self.canvas, width, height)
        self.particles = ParticleSystem(self.canvas, width, height)
        
        self.is_active = False
    
    def place(self, **kwargs):
        """Place the background canvas."""
        self.canvas.place(**kwargs)
    
    def start_effects(self):
        """Start all background effects."""
        self.is_active = True
        
        # Start matrix rain with low opacity
        threading.Thread(
            target=lambda: time.sleep(1) or self.matrix.start(),
            daemon=True
        ).start()
        
        # Start subtle particle effects
        threading.Thread(
            target=lambda: time.sleep(2) or self.particles.start(),
            daemon=True
        ).start()
    
    def stop_effects(self):
        """Stop all background effects."""
        self.is_active = False
        self.matrix.stop()
        self.particles.stop()


# Example usage and integration functions
def create_cyber_enhanced_button(parent, text: str, command=None, **kwargs):
    """Create a button with cyber enhancement capabilities."""
    button = tk.Button(parent, text=text, command=command, **kwargs)
    cyber_widget = CyberEnhancedWidget(button)
    
    # Add hover effects
    def on_enter(event):
        cyber_widget.add_scanline_effect()
    
    def on_leave(event):
        cyber_widget.stop_all_effects()
    
    def on_click(event):
        cyber_widget.add_glitch_effect(0.3)
    
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.bind("<Button-1>", on_click)
    
    return button, cyber_widget


def create_cyber_progress_indicator(parent, size: int = 100):
    """Create a cyberpunk-style progress indicator."""
    return CyberProgressRing(parent, size)


if __name__ == "__main__":
    # Demo of cyber effects
    root = tk.Tk()
    root.geometry("800x600")
    root.configure(bg="#0A0A0A")
    root.title("Cyber UI Effects Demo")
    
    # Add cyber background
    cyber_bg = CyberBackground(root, 800, 600)
    cyber_bg.place(x=0, y=0)
    cyber_bg.start_effects()
    
    # Demo frame
    demo_frame = tk.Frame(root, bg="#1A1A1A", width=400, height=300)
    demo_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    demo_frame.pack_propagate(False)
    
    # Demo buttons
    cyber_button, _ = create_cyber_enhanced_button(
        demo_frame,
        "Cyber Button",
        bg="#2A2A2A",
        fg="#FFFFFF",
        font=("Inter", 12, "bold"),
        relief="flat",
        bd=0,
        padx=20,
        pady=10
    )
    cyber_button.pack(pady=20)
    
    # Demo progress ring
    progress_ring = create_cyber_progress_indicator(demo_frame, 80)
    progress_ring.pack(pady=20)
    progress_ring.set_indeterminate(True)
    
    # Demo label with effects
    demo_label = tk.Label(
        demo_frame,
        text="CYBER ENHANCED UI",
        bg="#1A1A1A",
        fg="#FFFFFF",
        font=("Inter", 16, "bold")
    )
    demo_label.pack(pady=20)
    
    # Add effects to label
    label_effects = CyberEnhancedWidget(demo_label)
    label_effects.add_scanline_effect()
    
    root.mainloop()