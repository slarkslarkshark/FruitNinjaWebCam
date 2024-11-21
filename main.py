import pygame
import cv2
import pywindows as pw
from finger import FingerCatcher
from time import time
WIDTH, HEIGHT = 1024, 576
CAMWIDTH, CAMHEIGHT = 1280, 720
FPS = 25

if __name__ == "__main__":
    catcher = FingerCatcher(CAMWIDTH, CAMHEIGHT, WIDTH, HEIGHT)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMWIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMHEIGHT)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fruit Ninja")

    start_window = pw.StartWindow()
    settings_window = pw.SettingsWindow(WIDTH, HEIGHT, CAMWIDTH, CAMHEIGHT)
    game_window = pw.GameWindow(WIDTH, HEIGHT, CAMWIDTH, CAMHEIGHT)

    game_mode = "menu"
    running = True
    prev_time = 0
    while running:
        time_elapsed = time() - prev_time
        _, img = cap.read()
        if time_elapsed > 1./FPS:
            prev_time = time()
            if game_mode == "menu":
                game_mode, running = start_window.plot(screen, game_mode)
            elif game_mode == "settings":
                game_mode, running = settings_window.plot(screen, game_mode, img)
            elif game_mode == "game":
                game_mode, running = game_window.play(screen, img, catcher)

            pygame.display.flip()

    pygame.quit()
    cap.release()
