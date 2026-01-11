import pygame
import math

class TrailPoint:
    def __init__(self, x, y, timestamp):
        self.x = x
        self.y = y
        self.timestamp = timestamp
        self.age = 0

class FingerTrail:
    """Manages and draws the finger trail with animations"""
    MAX_TRAIL_LENGTH = 30
    FADE_DURATION = 500  # milliseconds
    
    def __init__(self):
        self.trail_points = []
        self.animation_time = 0
        
    def add_point(self, x, y):
        """Add a new point to the trail"""
        if x is not None and y is not None:
            current_time = pygame.time.get_ticks()
            self.trail_points.append(TrailPoint(x, y, current_time))
            
            # Remove old points
            if len(self.trail_points) > self.MAX_TRAIL_LENGTH:
                self.trail_points.pop(0)
    
    def update(self):
        """Update trail point ages"""
        current_time = pygame.time.get_ticks()
        self.animation_time += 0.05
        
        # Remove expired points
        self.trail_points = [
            point for point in self.trail_points
            if current_time - point.timestamp < self.FADE_DURATION
        ]
        
        # Update ages
        for point in self.trail_points:
            point.age = current_time - point.timestamp
    
    def clear(self):
        """Clear all trail points"""
        self.trail_points = []
    
    def _clamp_color(self, value):
        """Ensure color component is in [0, 255]"""
        return max(0, min(255, int(value)))
    
    def draw(self, screen):
        """Draw the trail with gradient colors and fading"""
        if len(self.trail_points) < 2:
            return
        
        # Draw trail segments with gradient
        for i in range(len(self.trail_points) - 1):
            point1 = self.trail_points[i]
            point2 = self.trail_points[i + 1]
            
            # Calculate fade based on age
            fade1 = 1.0 - (point1.age / self.FADE_DURATION)
            fade2 = 1.0 - (point2.age / self.FADE_DURATION)
            
            # Skip if both points are fully faded
            if fade1 <= 0 and fade2 <= 0:
                continue
            
            # Clamp fade to [0, 1]
            fade1 = max(0.0, min(1.0, fade1))
            fade2 = max(0.0, min(1.0, fade2))
            
            # Calculate position in trail (0 = oldest, 1 = newest)
            pos_in_trail = i / max(1, len(self.trail_points) - 1)
            
            # Color gradient: blue -> cyan -> green -> yellow -> red
            if pos_in_trail < 0.25:
                t = pos_in_trail / 0.25
                r = 0
                g = 100 + t * 155  # 100 → 255
                b = 255
            elif pos_in_trail < 0.5:
                t = (pos_in_trail - 0.25) / 0.25
                r = 0
                g = 255
                b = 255 * (1 - t)  # 255 → 0
            elif pos_in_trail < 0.75:
                t = (pos_in_trail - 0.5) / 0.25
                r = 255 * t        # 0 → 255
                g = 255
                b = 0
            else:
                t = (pos_in_trail - 0.75) / 0.25
                r = 255
                g = 255 - 155 * t  # 255 → 100
                b = 0
            
            # Clamp RGB values
            r = self._clamp_color(r)
            g = self._clamp_color(g)
            b = self._clamp_color(b)
            
            # Apply fade to alpha
            alpha1 = self._clamp_color(255 * fade1)
            alpha2 = self._clamp_color(255 * fade2)
            
            # Draw line with gradient
            self._draw_gradient_line(
                screen,
                (int(point1.x), int(point1.y)),
                (int(point2.x), int(point2.y)),
                (r, g, b, alpha1),
                (r, g, b, alpha2),
                width=int(3 + 2 * fade1)
            )
        
        # Draw particles/sparks along trail
        for i, point in enumerate(self.trail_points):
            if i % 3 == 0:  # Draw every 3rd point as a particle
                fade = 1.0 - (point.age / self.FADE_DURATION)
                if fade > 0:
                    fade = max(0.0, min(1.0, fade))
                    size = int(3 + 2 * math.sin(self.animation_time + i))
                    size = max(1, size)  # Ensure at least size 1
                    alpha = self._clamp_color(200 * fade)
                    self._draw_particle(screen, int(point.x), int(point.y), size, alpha)
    
    def _draw_gradient_line(self, screen, start, end, color1, color2, width=3):
        """Draw a line with gradient color"""
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = math.hypot(dx, dy)
        
        if distance == 0 or width <= 0:
            return
        
        steps = max(2, int(distance / 2))
        for i in range(steps):
            t = i / steps
            x = int(start[0] + dx * t)
            y = int(start[1] + dy * t)
            
            # Interpolate color and alpha
            r = color1[0] * (1 - t) + color2[0] * t
            g = color1[1] * (1 - t) + color2[1] * t
            b = color1[2] * (1 - t) + color2[2] * t
            alpha = color1[3] * (1 - t) + color2[3] * t
            
            # Clamp all values
            r = self._clamp_color(r)
            g = self._clamp_color(g)
            b = self._clamp_color(b)
            alpha = self._clamp_color(alpha)
            
            # Create surface and draw circle
            particle_surface = pygame.Surface((width * 2, width * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (r, g, b, alpha), (width, width), width)
            screen.blit(particle_surface, (x - width, y - width))
    
    def _draw_particle(self, screen, x, y, size, alpha):
        """Draw a glowing particle"""
        if size <= 0 or alpha <= 0:
            return
        particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        # Outer glow
        pygame.draw.circle(particle_surface, (255, 255, 255, alpha), (size, size), size)
        # Inner bright core
        inner_alpha = min(255, alpha + 55)  # Slightly brighter
        pygame.draw.circle(particle_surface, (255, 255, 200, inner_alpha), (size, size), max(1, size // 2))
        screen.blit(particle_surface, (x - size, y - size))


class FingerIcon:
    """Animated finger icon/visualization"""
    def __init__(self):
        self.animation_time = 0
        self.pulse_phase = 0
        
    def update(self):
        """Update animation"""
        self.animation_time += 0.1
        self.pulse_phase += 0.15
        
    def draw(self, screen, x, y):
        """Draw animated finger icon"""
        if x is None or y is None:
            return
        
        x, y = int(x), int(y)
        
        # Pulsing outer glow
        pulse_radius = 15 + int(5 * math.sin(self.pulse_phase))
        glow_surface = pygame.Surface((pulse_radius * 2, pulse_radius * 2), pygame.SRCALPHA)
        glow_alpha = int(100 + 50 * math.sin(self.pulse_phase))
        pygame.draw.circle(glow_surface, (255, 255, 255, glow_alpha), 
                          (pulse_radius, pulse_radius), pulse_radius)
        glow_surface.set_alpha(glow_alpha)
        screen.blit(glow_surface, (x - pulse_radius, y - pulse_radius))
        
        # Main circle with rotation effect
        main_radius = 12
        main_surface = pygame.Surface((main_radius * 2, main_radius * 2), pygame.SRCALPHA)
        
        # Draw rotating segments
        num_segments = 8
        for i in range(num_segments):
            angle = (self.animation_time * 50 + i * 360 / num_segments) % 360
            rad = math.radians(angle)
            x1 = main_radius + int((main_radius - 2) * math.cos(rad))
            y1 = main_radius + int((main_radius - 2) * math.sin(rad))
            x2 = main_radius + int(main_radius * math.cos(rad))
            y2 = main_radius + int(main_radius * math.sin(rad))
            
            # Color based on segment
            segment_color = (
                max(0, min(255, int(100 + 155 * math.sin(self.animation_time + i)))),
                max(0, min(255, int(200 + 55 * math.cos(self.animation_time + i)))),
                255
            )
            pygame.draw.line(main_surface, segment_color, (x1, y1), (x2, y2), 2)
        
        # Bright center core
        pygame.draw.circle(main_surface, (255, 255, 255), (main_radius, main_radius), main_radius - 4)
        pygame.draw.circle(main_surface, (100, 200, 255), (main_radius, main_radius), main_radius - 6)
        
        screen.blit(main_surface, (x - main_radius, y - main_radius))
        
        # Draw slash effect when moving (optional enhancement)
        # This could be added later if needed
