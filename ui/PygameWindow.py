import pygame
from config import Config as cfg


class PygameWindow:
    screen = None

    def __init__(self, background=(0, 0, 0)):
        self.background_color = background
        self.is_running = True
        self.next_window = None
        self.buttons = []
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            for button in self.buttons:
                button.handle_event(event)

    @classmethod
    def init_screen(cls, game_name, width, height):
        print("Создаю экран...")
        if cls.screen is None:
            cls.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption(game_name)

    @property
    def window_width(self):
        return self.screen.get_width()

    @property
    def window_height(self):
        return self.screen.get_height()

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.background_color)

    def switch_window(self, next_window):
        self.next_window = next_window
        self.is_running = False

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            for button in self.buttons:
                button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(cfg.FPS)
        return self.next_window
