import pygame
import cv2
import pywindows as pw
from finger import FingerCatcher
WIDTH, HEIGHT = 800, 600
CAMWIDTH, CAMHEIGHT = WIDTH + 400, HEIGHT + 300

if __name__ == "__main__":
    catcher = FingerCatcher(CAMWIDTH, CAMHEIGHT, WIDTH, HEIGHT)
    cap = cv2.VideoCapture(0)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Случайные прямоугольники")

    start_window = pw.StartWindow()
    settings_window = pw.SettingsWindow()
    game_window = pw.GameWindow(WIDTH, HEIGHT, CAMWIDTH, CAMHEIGHT)
    clock = pygame.time.Clock()
    cap.read()
    game_mode = "menu"
    running = True
    while running:
        if game_mode == "menu":
            game_mode, running = start_window.plot(screen, game_mode)
        elif game_mode == "settings":
            game_mode, running = settings_window.plot(screen, game_mode, cap)
        elif game_mode == "game":
            game_mode, running = game_window.play(screen, cap, catcher)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    cap.release()
