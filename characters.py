from collections import deque
import pygame
from shapely import box, LineString, Point
import random

class Enemy:
    def __init__(self, color, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        enemy_width = random.randint(20, 100)
        enemy_height = random.randint(20, 100)
        x = random.randint(0, WIDTH - enemy_width)
        y = 0
        self.rect = pygame.Rect(x, y, enemy_width, enemy_height)

        self.speed = random.randint(3, 8)
        self.color = color

    def move(self):
        self.rect.top += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.rect.left, self.rect.top,
                                                self.rect.width, self.rect.height))
    
    def colliderect(self, rect):
        return self.rect.colliderect(rect)
    
class Player:
    def __init__(self, WIDTH, HEIGHT):
        self.hand_track = deque()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

    def __iter__(self):
        return iter(self.hand_track)

    def pop(self):
        if len(self.hand_track) >= 4:
            self.hand_track.pop()

    def update(self, x, y):
        new_x = int(x * self.HEIGHT)
        new_y = int(y * self.WIDTH)
        self.hand_track.appendleft((new_x, new_y))

    def collide(self, enemy):
        if not len(self.hand_track):
            return False
        
        rect = box(
            enemy.rect.left, enemy.rect.bottom,
            enemy.rect.right, enemy.rect.top
            )
       
        if len(self.hand_track) == 1:
            finger_point = Point(self.hand_track[0])
            return rect.contains(finger_point)
        
        track = LineString(self.hand_track)
        return rect.intersects(track)
    
    def clear(self):
        self.hand_track.clear()
        
    def draw(self, screen):
        for i in range(len(self.hand_track) - 1):
            pygame.draw.line(screen, (255, 255, 255), self.hand_track[i], self.hand_track[i + 1], 4)
            pygame.draw.circle(screen, (255, 255, 255), self.hand_track[0], 4)