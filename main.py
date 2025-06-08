import pygame
from config import Config as cfg
from ui import PygameWindow, MainMenuWindow


if __name__ == "__main__":
    pygame.init()
    PygameWindow.init_screen(cfg.GAMENAME, cfg.HEIGHT, cfg.WIDTH)
    current_window = MainMenuWindow()


    while current_window:
        current_window = current_window.run()
