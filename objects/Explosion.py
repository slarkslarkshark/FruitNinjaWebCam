import pygame
import math
import random


class Explosion:
    """Brief explosion animation for bomb hits"""
    DURATION = 400  # milliseconds - short and non-intrusive
    
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.start_time = pygame.time.get_ticks()
        self.particles = []
        
        # Create particles for explosion effect
        num_particles = 12
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            self.particles.append({
                'angle': angle,
                'speed': speed,
                'distance': 0,
                'max_distance': random.uniform(15, 25),
                'size': random.randint(3, 6),
                'color': random.choice([
                    (255, 100, 0),  # Orange
                    (255, 200, 0),  # Yellow
                    (255, 50, 0),   # Red
                    (255, 150, 50), # Light orange
                ])
            })
    
    def update(self):
        """Update explosion animation"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        
        if elapsed >= self.DURATION:
            return False  # Animation finished
        
        # Update particle positions
        progress = elapsed / self.DURATION
        for particle in self.particles:
            # Ease out function for smooth animation
            eased_progress = 1 - (1 - progress) ** 2
            particle['distance'] = particle['max_distance'] * eased_progress
        
        return True  # Animation still active
    
    def draw(self, screen):
        """Draw explosion effect"""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        progress = elapsed / self.DURATION
        
        if progress >= 1.0:
            return
        
        # Draw expanding circle flash
        alpha = int(255 * (1 - progress))
        max_radius = int(30 + (progress * 20))
        
        # Create temporary surface for alpha blending
        flash_size = max_radius * 2
        flash_surface = pygame.Surface((flash_size, flash_size), pygame.SRCALPHA)
        flash_color = (255, 200, 0)
        pygame.draw.circle(
            flash_surface,
            flash_color,
            (max_radius, max_radius),
            max_radius
        )
        flash_surface.set_alpha(alpha // 2)
        screen.blit(flash_surface, (int(self.start_x - max_radius), int(self.start_y - max_radius)))
        
        # Draw particles
        for particle in self.particles:
            x = self.start_x + math.cos(particle['angle']) * particle['distance']
            y = self.start_y + math.sin(particle['angle']) * particle['distance']
            
            # Fade out particles
            particle_alpha = int(255 * (1 - progress))
            color = particle['color']
            particle_size = particle['size']
            
            # Draw particle with alpha
            particle_surface = pygame.Surface((particle_size * 2, particle_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                particle_surface,
                color,
                (particle_size, particle_size),
                particle_size
            )
            particle_surface.set_alpha(particle_alpha)
            screen.blit(particle_surface, (int(x - particle_size), int(y - particle_size)))
