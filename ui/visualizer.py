import pygame
import math
import random
import colorsys

class CircularSpectrum:
    """
    This is the visualizer thingy.
    Basically tries to copy that swooshy Siri/Alexa look.
    """
    
    def __init__(self, screen, center_x, center_y):
        self.screen = screen
        self.cx = center_x
        self.cy = center_y
        
        # how big the circle is
        self.radius = 150
        self.num_bars = 90  # how many bars we want around it
        
        # pretending we have audio levels since we can't actually read system audio easily
        self.levels = [0.0] * self.num_bars
        self.target_levels = [0.0] * self.num_bars
        self.velocities = [0.0] * self.num_bars
        
        # animation state
        self.time = 0
        self.mode = "idle"
        self.rotation = 0
        
        # colors for different states
        self.color_schemes = {
            'idle': self._create_tech_gradient(),      # The signature tech look
            'listening': self._create_gradient(0.3, 0.4), # Greenish for listening
            'speaking': self._create_tech_gradient(),     # Use same fancy gradient for speaking
            'thinking': self._create_gradient(0.7, 0.8),  # Purple for thinking
        }
        self.colors = self.color_schemes['idle']
        self.target_colors = self.colors
        
    def _create_tech_gradient(self):
        """
        Manually builds that sweet Cyan -> Blue -> Purple -> Magenta gradient
        Matches the reference image style.
        """
        colors = []
        # Key colors extracted from the image
        # i=0 is Top. i=22 Right. i=45 Bottom. i=67 Left.
        key_colors = [
            (0, 100, 255),    # Top (Deep Blue)
            (150, 0, 255),    # Right (Purple)
            (255, 50, 200),   # Bottom Right (Pink)
            (100, 50, 255),   # Bottom (Bluish Purple)
            (50, 150, 255),   # Bottom Left (Blue)
            (50, 200, 255),   # Left (Cyan - The main focus)
            (0, 255, 200),    # Top Left (Teal)
        ]
        
        steps_per_section = self.num_bars // (len(key_colors) - 1)
        
        for i in range(len(key_colors) - 1):
            c1 = key_colors[i]
            c2 = key_colors[i+1]
            
            for j in range(steps_per_section):
                t = j / steps_per_section
                r = int(c1[0] + (c2[0] - c1[0]) * t)
                g = int(c1[1] + (c2[1] - c1[1]) * t)
                b = int(c1[2] + (c2[2] - c1[2]) * t)
                colors.append((r, g, b))
        
        # fill any remaining
        while len(colors) < self.num_bars:
            colors.append(key_colors[-1])
            
        return colors

    def _create_gradient(self, hue_start, hue_end):
        """Generates a smooth color gradient so it looks fancy"""
        colors = []
        for i in range(self.num_bars):
            progress = i / self.num_bars
            # interpolate the hue
            hue = hue_start + (hue_end - hue_start) * progress
            hue = hue % 1.0
            
            # make it pop with high sat/val
            r, g, b = colorsys.hsv_to_rgb(hue, 0.9, 1.0)
            colors.append((int(r * 255), int(g * 255), int(b * 255)))
        
        return colors
    
    def set_mode(self, mode):
        """Swaps the mode so we know what color to use"""
        self.mode = mode
        if mode in self.color_schemes:
            self.target_colors = self.color_schemes[mode]
        
    def _generate_audio_levels(self):
        """Fakes the audio visualization because hooking into Wasapi is a pain"""
        # Center of the "Left" side is roughly 3/4 around the circle if 0 is top
        left_center_idx = int(self.num_bars * 0.75) 
        
        if self.mode == "idle":
            for i in range(self.num_bars):
                # Calculate distance from the "Left" center
                dist = abs(i - left_center_idx)
                if dist > self.num_bars / 2:
                    dist = self.num_bars - dist
                
                # Shape factor: Max at left_center
                shape_factor = max(0.1, 1.0 - (dist / (self.num_bars * 0.35)))
                
                # Add some breathing motion
                breath = math.sin(self.time * 2 + i * 0.1) * 0.1
                
                self.target_levels[i] = (shape_factor * 0.5) + breath + random.uniform(0, 0.05)
                
        elif self.mode == "listening":
            for i in range(self.num_bars):
                base = 0.3 + math.sin(self.time * 4 + i * 0.2) * 0.1
                self.target_levels[i] = base
                
        elif self.mode == "speaking":
            # IMPROVED PHYSICS: NCS / Audio Spectrum Style
            # This simulates "beats" and "frequency jitter"
            
            # 1. Global "Kick" or "Bass" beat
            beat = 0
            # every ~0.5 seconds, do a kick
            if (self.time % 0.5) < 0.1: 
                beat = random.uniform(0.3, 0.6)
            
            for i in range(self.num_bars):
                # Calculate distance from the "Left" center for shaping
                dist = abs(i - left_center_idx)
                if dist > self.num_bars / 2:
                    dist = self.num_bars - dist
                    
                # Shape bias (Long on left, short on right)
                shape_bias = max(0.15, 1.0 - (dist / (self.num_bars * 0.45)))
                
                # 2. Simulate frequency bands
                # Some bars vibrate fast (high freq), some slow (bass)
                # We map index 'i' to a "frequency"
                
                # Fast jitter for "highs"
                jitter = random.uniform(0, 0.3)
                
                # Perlin-ish noise for "mids"
                wave = math.sin(self.time * 15 + i * 0.5) * 0.2
                
                # Combine: Shape * (Bass + Mids + Highs)
                energy = beat + wave + jitter
                
                # Scale appropriately
                level = 0.2 + (energy * 0.8)
                
                # Apply the shape mask
                final_level = level * shape_bias
                
                # Allow huge spikes (the "vibrating" look)
                self.target_levels[i] = max(0.05, min(1.3, final_level))
                
        elif self.mode == "thinking":
            for i in range(self.num_bars):
                angle = (i / self.num_bars) * math.pi * 2
                wave = math.sin(angle * 3 + self.time * 8) * 0.4
                self.target_levels[i] = 0.4 + wave
    
    def update(self, dt):
        """Runs the loop updates"""
        self.time += dt
        self.rotation += dt * 0.1  # slow rotation
        
        # interpolate colors so they don't snap instantly
        for i in range(self.num_bars):
            current = self.colors[i]
            target = self.target_colors[i]
            # lerp
            new_r = int(current[0] + (target[0] - current[0]) * 0.1)
            new_g = int(current[1] + (target[1] - current[1]) * 0.1)
            new_b = int(current[2] + (target[2] - current[2]) * 0.1)
            self.colors[i] = (new_r, new_g, new_b)
        
        # pick new target heights - VERY FAST for "vibrating" look
        refresh_rate = 1.0 if self.mode == "speaking" else 0.3
        if random.random() < refresh_rate:
            self._generate_audio_levels()
        
        # Physics tuning
        for i in range(self.num_bars):
            diff = self.target_levels[i] - self.levels[i]
            
            # SUPER SNAPPY physics for NCS style
            # Very high speed, very low damping to let it jitter
            if self.mode == "speaking":
                speed = 40  # Snap to target instantly
                damping = 0.5 # Low damping = lots of vibration/overshoot
            else:
                speed = 10
                damping = 0.85
            
            self.velocities[i] += diff * speed * dt
            self.velocities[i] *= damping
            self.levels[i] += self.velocities[i] * dt
            self.levels[i] = max(0.05, min(1.3, self.levels[i]))
    
    def draw(self):
        """Actually puts the stuff on screen"""
        self._draw_bars()
    
    def _draw_bars(self):
        """Calculates where each bar goes"""
        bar_width = 7  # Even beefier
        min_height = 10
        max_height = 160 # Maximum length
        
        for i in range(self.num_bars):
            # Circular positioning
            angle = (i / self.num_bars) * math.pi * 2 - math.pi / 2 + self.rotation
            
            # Smooth out the height
            height = min_height + self.levels[i] * max_height
            
            # Start point (on the radius)
            inner_x = self.cx + math.cos(angle) * self.radius
            inner_y = self.cy + math.sin(angle) * self.radius
            
            # End point (radiating out)
            outer_x = self.cx + math.cos(angle) * (self.radius + height)
            outer_y = self.cy + math.sin(angle) * (self.radius + height)
            
            color = self.colors[i]
            
            # Draw the main bar line with rounded ends simulation
            pygame.draw.line(self.screen, color, (inner_x, inner_y), (outer_x, outer_y), bar_width)
            
            # Draw rounded tip at the outer end
            tip_x = int(outer_x)
            tip_y = int(outer_y)
            pygame.draw.circle(self.screen, color, (tip_x, tip_y), bar_width // 2)
            
            # Draw rounded tip at inner end
            base_x = int(inner_x)
            base_y = int(inner_y)
            pygame.draw.circle(self.screen, color, (base_x, base_y), bar_width // 2)

    def _draw_inner(self):
        pass
