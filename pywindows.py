import pygame
import cv2
import random
import characters as pers

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 255, 255)

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
                return game_mode, False
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

class SettingsWindow:
    def __init__(self):
        self.b_camera = pygame.Rect(80, 80, 250, 50)
        self.b_back = pygame.Rect(80, 160, 250, 50)

        font = pygame.font.SysFont("comic sans ms", 40)
        self.camera_text = font.render("Camera Testing", True, WHITE)
        self.back_text = font.render("Back", True, WHITE)
        self.camera_on = False
    
    def plot(self, screen, game_mode, cap):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return game_mode, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.camera_on = False
            if event.type == pygame.MOUSEBUTTONDOWN and not self.camera_on:
                if event.button == 1:
                    x = event.pos[0]
                    y = event.pos[1]

                    if x > self.b_camera.left and x < self.b_camera.right \
                    and self.b_camera.top and y < self.b_camera.bottom:
                        self.camera_on = True
                        
                    if x > self.b_back.left and x < self.b_back.right \
                    and y > self.b_back.top and y < self.b_back.bottom:
                        game_mode = "menu"

        if self.camera_on:
            _, img = cap.read()
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            screen.blit(pygame.surfarray.make_surface(img), (0, 0))
        else:
            screen.fill(BLACK)
            pygame.draw.rect(screen, GREEN, self.b_camera)
            screen.blit(self.camera_text, (165, 80))
            pygame.draw.rect(screen, GREEN, self.b_back)
            screen.blit(self.back_text, (118, 160))
        return game_mode, True

class GameWindow:
    def __init__(self, WIDTH, HEIGHT):
        self.enemies = []
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

    def play(self, screen, cap, catcher):
        running = True
        game_mode = "game"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.enemies = []
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_mode = "menu"
                    
        if random.random() < 0.02: 
            self.enemies.append(pers.Enemy(RED, self.WIDTH, self.HEIGHT))

        for enemy in self.enemies:
            enemy.move()

        self.enemies = [r for r in self.enemies if r.rect.top < self.HEIGHT]
        screen.fill(BLACK)

        _, img = cap.read()
        track = catcher.find_finger(img)
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        screen.blit(pygame.surfarray.make_surface(img), (0, 0))

        for enemy in self.enemies:
            enemy.draw(screen)
            
        track.draw(screen)
        for enemy in self.enemies:
            if track.collide(enemy):
                self.enemies.remove(enemy)
        return game_mode, running
