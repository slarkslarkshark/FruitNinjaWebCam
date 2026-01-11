import pygame
import math


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font,
        color=(100, 200, 100),
        hover_color=(150, 255, 150),
        text_color=(255, 255, 255),
        border_radius=15,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.on_click_callback = None
        self.animation_time = 0

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Update animation for hover effect
        if is_hovered:
            self.animation_time += 0.1
        else:
            self.animation_time = 0
        
        # Choose base color
        base_color = self.hover_color if is_hovered else self.color
        
        # Add subtle glow effect when hovered
        if is_hovered:
            glow_radius = int(5 + 2 * math.sin(self.animation_time))
            glow_surface = pygame.Surface((self.rect.width + glow_radius * 2, 
                                          self.rect.height + glow_radius * 2), 
                                         pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*base_color, 100),
                           (0, 0, glow_surface.get_width(), glow_surface.get_height()),
                           border_radius=self.border_radius)
            screen.blit(glow_surface, (self.rect.x - glow_radius, self.rect.y - glow_radius))
        
        # Draw button with rounded corners
        pygame.draw.rect(screen, base_color, self.rect, border_radius=self.border_radius)
        
        # Add gradient effect (lighter top, darker bottom)
        gradient_surface = pygame.Surface((self.rect.width, self.rect.height // 2), pygame.SRCALPHA)
        for i in range(self.rect.height // 2):
            alpha = int(30 * (1 - i / (self.rect.height // 2)))
            pygame.draw.line(gradient_surface, (*base_color, alpha), 
                           (0, i), (self.rect.width, i))
        screen.blit(gradient_surface, (self.rect.x, self.rect.y))
        
        # Draw border
        border_color = tuple(min(255, c + 30) for c in base_color)
        pygame.draw.rect(screen, border_color, self.rect, width=2, border_radius=self.border_radius)
        
        # Draw text with shadow for better visibility
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Text shadow
        shadow_surface = self.font.render(self.text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
        screen.blit(shadow_surface, shadow_rect)
        
        # Text
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.on_click_callback:
                self.on_click_callback()

    def on_click(self, callback):
        self.on_click_callback = callback
