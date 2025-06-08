import pygame


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font,
        color=(100, 100, 100),
        hover_color=(150, 150, 150),
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.on_click_callback = None

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        pygame.draw.rect(
            screen, self.hover_color if is_hovered else self.color, self.rect
        )

        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.on_click_callback:
                self.on_click_callback()

    def on_click(self, callback):
        self.on_click_callback = callback
