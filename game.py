import pygame
import random
import cv2
import numpy as np
from finger import FingerCatcher

class Rectangle:
    def __init__(self, color):
        self.width = random.randint(20, 100)
        self.height = random.randint(20, 100)
        self.x = random.randint(0, WIDTH - self.width)
        self.y = 0
        self.speed = random.randint(1, 5)
        self.color = color

    def move(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

class SettingsWindow:
    def __init__(self):
        self.b_camera = pygame.Rect(80, 80, 250, 50)
        self.b_back = pygame.Rect(80, 160, 250, 50)

        font = pygame.font.SysFont("comic sans ms", 40)
        self.camera_text = font.render("Camera Testing", True, WHITE)
        self.back_text = font.render("Back", True, WHITE)
    
    def plot(self, screen, game_mode):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = event.pos[0]
                    y = event.pos[1]

                    if x > self.b_camera.left  and x < self.b_camera.right \
                    and self.b_camera.top and y < self.b_camera.bottom:
                        pass
                    
                    if x > self.b_back.left and x < self.b_back.right \
                    and y > self.b_back.top and y < self.b_back.bottom:
                        game_mode = "menu"

        screen.fill(BLACK)

        pygame.draw.rect(screen, GREEN, self.b_camera)
        screen.blit(self.camera_text, (165, 80))

        pygame.draw.rect(screen, GREEN, self.b_back)
        screen.blit(self.back_text, (118, 160))
        return game_mode


class StartWindow:
    def __init__(self):
        self.b_play = pygame.Rect(80, 80, 250, 50)
        self.b_settings = pygame.Rect(80, 160, 250, 50)
        self.b_exit = pygame.Rect(80, 240, 250, 50)

        font1 = pygame.font.SysFont("comic sans ms", 50)
        font2 = pygame.font.SysFont("comic sans ms", 40)
        
        self.game_name = font1.render("Fruit Ninja", True, WHITE)
        self.play_text = font2.render("Play", True, WHITE)
        self.settings_text = font2.render("Settings", True, WHITE)
        self.exit_text = font2.render("Exit", True, WHITE)
        

    def plot(self, screen, game_mode):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return self.game_mode, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = event.pos[0]
                    y = event.pos[1]
                    
                    if x > self.b_exit.left and x < self.b_exit.right \
                    and y > self.b_exit.top and y < self.b_exit.bottom:
                        return game_mode, False

                    if x > self.b_play.left and x < self.b_play.right \
                    and y > self.b_play.top and y < self.b_play.bottom:
                        game_mode = "game"
                    
                    if x > self.b_settings.left and x < self.b_settings.right \
                    and y > self.b_settings.top and y < self.b_settings.bottom:
                        game_mode = "settings"

        screen.fill(BLACK)
        screen.blit(self.game_name, (120, 0)) 

        pygame.draw.rect(screen, GREEN, self.b_play)
        screen.blit(self.play_text, (165, 80))

        pygame.draw.rect(screen, GREEN, self.b_settings)
        screen.blit(self.settings_text, (118, 160))

        pygame.draw.rect(screen, GREEN, self.b_exit)
        screen.blit(self.exit_text, (165, 240))

        return game_mode, True


WIDTH, HEIGHT = 480, 640

catcher = FingerCatcher()
cap = cv2.VideoCapture(0)
pygame.init()

screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("Случайные прямоугольники")

#Настройка цвета
BLACK = (0,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0, 255, 255)

# Меню
game_mode = "menu"

font1 = pygame.font.SysFont("comic sans ms", 50)
text = font1.render("Fruit Ninja", True, WHITE)
font2 = pygame.font.SysFont("comic sans ms", 40)
text2 = font2.render("Play", True, WHITE)
text3 = font2.render("Settings", True, WHITE)
text4 = font2.render("Exit", True, WHITE)
text5 = font2.render("Back", True, WHITE)


rectangles = []
running = True
start_window = StartWindow()
settings_window = SettingsWindow()
clock = pygame.time.Clock()
while running:
    if game_mode == "menu":
        game_mode, running = start_window.plot(screen, game_mode)
    elif game_mode == "settings":
        game_mode = settings_window.plot(screen, game_mode)
    elif game_mode == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if random.random() < 0.02: 
            rectangles.append(Rectangle(RED))

        for rectangle in rectangles:
            rectangle.move()

        rectangles = [r for r in rectangles if r.y < HEIGHT]

        screen.fill(BLACK)
        for rectangle in rectangles:
            rectangle.draw(screen)

        _, img = cap.read()
        img = cv2.flip(img, 1)
        track = catcher.find_finger(img)
        if len(track) != 0:
            for i in range(len(track) - 1):
                pygame.draw.line(screen, WHITE, track[i], track[i + 1], 4)
                pygame.draw.circle(screen, WHITE, track[0], 4)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
cap.release()
