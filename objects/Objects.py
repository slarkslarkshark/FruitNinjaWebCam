from .GameObject import GameObject
import random
import pygame
import os
import math


def create_apple_icon():
    """Create a beautiful apple icon"""
    size = 64
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    # Draw apple body with gradient effect
    pygame.draw.circle(surface, (220, 50, 50), (center, center), 28)
    pygame.draw.circle(surface, (255, 100, 100), (center, center), 24)
    pygame.draw.circle(surface, (255, 180, 180), (center - 4, center - 4), 18)
    pygame.draw.ellipse(surface, (180, 30, 30), (center - 20, center + 8, 40, 20))
    
    # Draw green leaf at top
    leaf_points = [
        (center - 8, center - 20),
        (center - 2, center - 28),
        (center + 2, center - 28),
        (center + 8, center - 20),
        (center, center - 18)
    ]
    pygame.draw.polygon(surface, (100, 200, 100), leaf_points)
    pygame.draw.polygon(surface, (80, 180, 80), leaf_points, 2)
    
    # Draw stem
    pygame.draw.line(surface, (139, 90, 43), (center, center - 20), (center, center - 28), 3)
    
    # Add shine/highlight
    pygame.draw.ellipse(surface, (255, 220, 220), (center - 10, center - 12, 12, 8))
    
    return surface


def create_orange_icon():
    """Create a beautiful orange icon"""
    size = 64
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    # Draw orange body
    pygame.draw.circle(surface, (255, 165, 0), (center, center), 28)
    pygame.draw.circle(surface, (255, 200, 100), (center, center), 24)
    pygame.draw.circle(surface, (255, 220, 150), (center - 3, center - 3), 20)
    
    # Draw orange segments (lines)
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x1 = center + int(15 * math.cos(rad))
        y1 = center + int(15 * math.sin(rad))
        x2 = center + int(22 * math.cos(rad))
        y2 = center + int(22 * math.sin(rad))
        pygame.draw.line(surface, (255, 140, 0), (x1, y1), (x2, y2), 1)
    
    # Draw stem and leaf
    pygame.draw.line(surface, (139, 90, 43), (center, center - 20), (center, center - 28), 3)
    leaf_points = [
        (center - 6, center - 24),
        (center, center - 30),
        (center + 6, center - 24),
    ]
    pygame.draw.polygon(surface, (50, 150, 50), leaf_points)
    
    # Add shine
    pygame.draw.ellipse(surface, (255, 240, 200), (center - 8, center - 10, 14, 10))
    
    return surface


def create_banana_icon():
    """Create a beautiful banana icon"""
    size = 64
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    # Draw banana shape (curved)
    banana_points = [
        (center - 20, center + 10),
        (center - 15, center + 15),
        (center - 8, center + 18),
        (center, center + 20),
        (center + 8, center + 18),
        (center + 15, center + 15),
        (center + 20, center + 10),
        (center + 18, center - 5),
        (center + 12, center - 15),
        (center + 5, center - 20),
        (center - 5, center - 20),
        (center - 12, center - 15),
        (center - 18, center - 5),
    ]
    pygame.draw.polygon(surface, (255, 255, 0), banana_points)
    pygame.draw.polygon(surface, (255, 240, 100), banana_points, 2)
    
    # Add banana details (brown spots)
    for spot in [(center - 10, center + 5), (center, center), (center + 10, center - 5)]:
        pygame.draw.circle(surface, (200, 150, 50), spot, 2)
    
    # Draw stem
    pygame.draw.line(surface, (100, 150, 50), (center - 5, center - 20), (center - 8, center - 25), 2)
    
    # Add shine
    pygame.draw.ellipse(surface, (255, 255, 200), (center - 8, center - 5, 12, 8))
    
    return surface


def create_strawberry_icon():
    """Create a beautiful strawberry icon"""
    size = 64
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    # Draw strawberry body (heart-like shape)
    strawberry_points = [
        (center, center + 25),
        (center - 20, center + 10),
        (center - 18, center - 5),
        (center - 12, center - 15),
        (center - 5, center - 20),
        (center, center - 22),
        (center + 5, center - 20),
        (center + 12, center - 15),
        (center + 18, center - 5),
        (center + 20, center + 10),
    ]
    pygame.draw.polygon(surface, (255, 50, 50), strawberry_points)
    pygame.draw.polygon(surface, (255, 100, 100), strawberry_points, 2)
    
    # Draw seeds (yellow dots)
    seed_positions = [
        (center - 12, center - 8), (center, center - 10), (center + 12, center - 8),
        (center - 10, center), (center + 10, center),
        (center - 8, center + 8), (center + 8, center + 8),
    ]
    for pos in seed_positions:
        pygame.draw.circle(surface, (255, 255, 150), pos, 2)
    
    # Draw leaves at top
    leaf_points1 = [
        (center - 8, center - 22),
        (center - 12, center - 28),
        (center - 6, center - 30),
        (center, center - 28),
    ]
    leaf_points2 = [
        (center, center - 28),
        (center + 6, center - 30),
        (center + 12, center - 28),
        (center + 8, center - 22),
    ]
    pygame.draw.polygon(surface, (50, 200, 50), leaf_points1)
    pygame.draw.polygon(surface, (50, 200, 50), leaf_points2)
    
    # Add shine
    pygame.draw.ellipse(surface, (255, 150, 150), (center - 8, center - 12, 12, 8))
    
    return surface


def create_watermelon_icon():
    """Create a beautiful watermelon slice icon"""
    size = 64
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    # Draw watermelon slice (triangle-like)
    slice_points = [
        (center, center + 25),
        (center - 22, center - 5),
        (center + 22, center - 5),
    ]
    pygame.draw.polygon(surface, (50, 200, 50), slice_points)  # Green rind
    pygame.draw.polygon(surface, (255, 50, 50), [
        (center, center + 20),
        (center - 18, center - 3),
        (center + 18, center - 3),
    ])  # Red flesh
    
    # Draw seeds
    seed_positions = [
        (center - 8, center + 5), (center + 8, center + 5),
        (center - 5, center + 10), (center + 5, center + 10),
        (center, center + 15),
    ]
    for pos in seed_positions:
        pygame.draw.ellipse(surface, (50, 30, 20), (pos[0] - 2, pos[1] - 1, 4, 2))
    
    # Add shine on rind
    pygame.draw.line(surface, (100, 255, 100), (center - 15, center - 2), (center + 15, center - 2), 2)
    
    return surface


def create_grape_icon():
    """Create a beautiful grape cluster icon"""
    size = 64
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    # Draw grape cluster (multiple circles)
    grape_positions = [
        (center - 8, center - 15), (center, center - 18), (center + 8, center - 15),
        (center - 10, center - 5), (center - 2, center - 8), (center + 6, center - 5),
        (center - 8, center + 5), (center + 2, center + 2), (center + 10, center + 5),
        (center - 4, center + 10), (center + 6, center + 12),
    ]
    
    for pos in grape_positions:
        pygame.draw.circle(surface, (150, 50, 200), pos, 8)
        pygame.draw.circle(surface, (180, 100, 220), pos, 6)
        pygame.draw.circle(surface, (200, 150, 240), pos, 4)
        # Add shine to each grape
        pygame.draw.circle(surface, (220, 180, 255), (pos[0] - 2, pos[1] - 2), 2)
    
    # Draw stem
    pygame.draw.line(surface, (100, 150, 50), (center - 2, center - 18), (center - 4, center - 25), 3)
    pygame.draw.line(surface, (100, 150, 50), (center + 2, center - 18), (center + 4, center - 25), 3)
    
    return surface


def create_pineapple_icon():
    """Create a beautiful pineapple icon"""
    size = 64
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    # Draw pineapple body (oval)
    pygame.draw.ellipse(surface, (255, 255, 0), (center - 20, center - 15, 40, 50))
    pygame.draw.ellipse(surface, (255, 240, 100), (center - 18, center - 13, 36, 46))
    
    # Draw diamond pattern (pineapple texture)
    from itertools import product
    for i, j in product(range(-2, 3), range(-2, 3)):
        x = center + i * 8
        y = center + j * 10
        if abs(i) + abs(j) < 3:
            diamond_points = [
                (x, y - 4), (x + 4, y), (x, y + 4), (x - 4, y)
            ]
            pygame.draw.polygon(surface, (200, 200, 0), diamond_points, 1)
    
    # Draw leaves at top
    for i in range(-2, 3):
        x = center + i * 6
        leaf_points = [
            (x, center - 15),
            (x - 2, center - 22),
            (x + 2, center - 22),
        ]
        pygame.draw.polygon(surface, (50, 200, 50), leaf_points)
    
    # Add shine
    pygame.draw.ellipse(surface, (255, 255, 200), (center - 10, center - 8, 16, 12))
    
    return surface


def load_or_create_fruit_image(fruit_type):
    """Load fruit image from file, or create it programmatically if not found"""
    image_path = f"assets/images/fruit_{fruit_type}.png"
    if os.path.exists(image_path):
        try:
            image = pygame.image.load(image_path).convert_alpha()
            return image
        except:
            pass  # Fall through to programmatic creation
    
    # Create programmatically based on fruit type
    fruit_creators = {
        'apple': create_apple_icon,
        'orange': create_orange_icon,
        'banana': create_banana_icon,
        'strawberry': create_strawberry_icon,
        'watermelon': create_watermelon_icon,
        'grape': create_grape_icon,
        'pineapple': create_pineapple_icon,
    }
    
    creator = fruit_creators.get(fruit_type, create_apple_icon)
    return creator()


def load_or_create_bomb_image():
    """Load bomb image from file, or create it programmatically if not found"""
    image_path = "assets/images/bomb.png"
    if os.path.exists(image_path):
        try:
            image = pygame.image.load(image_path).convert_alpha()
            return image
        except:
            pass  # Fall through to programmatic creation
    
    # Create programmatically if file doesn't exist
    size = 64
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    # Draw bomb body with 3D effect
    pygame.draw.circle(surface, (20, 20, 20), (center, center), 28)
    pygame.draw.circle(surface, (40, 40, 40), (center, center), 24)
    pygame.draw.circle(surface, (60, 60, 60), (center - 3, center - 3), 20)
    pygame.draw.ellipse(surface, (80, 80, 80), (center - 12, center - 18, 20, 12))
    
    # Draw fuse (brown rope-like)
    fuse_start = (center, center - 28)
    fuse_end = (center, 4)
    pygame.draw.line(surface, (101, 67, 33), fuse_start, fuse_end, 4)
    for i in range(3):
        y_pos = center - 28 + i * 8
        pygame.draw.line(surface, (80, 50, 25), (center - 2, y_pos), (center + 2, y_pos), 1)
    
    # Draw spark/flame at top
    flame_points = [
        (center, 2),
        (center - 4, 8),
        (center - 2, 10),
        (center, 12),
        (center + 2, 10),
        (center + 4, 8),
    ]
    pygame.draw.polygon(surface, (255, 150, 0), flame_points)
    pygame.draw.polygon(surface, (255, 200, 100), [
        (center, 2),
        (center - 2, 6),
        (center, 8),
        (center + 2, 6),
    ])
    
    # Add some shine to bomb
    pygame.draw.ellipse(surface, (100, 100, 100), (center - 8, center - 14, 12, 8))
    
    return surface


class Fruit(GameObject):
    name = "FRUIT"
    
    # Available fruit types
    FRUIT_TYPES = ['apple', 'orange', 'banana', 'strawberry', 'watermelon', 'grape', 'pineapple']

    def __init__(self, x, y, width=40, height=40):
        # Randomly select fruit type
        self.fruit_type = random.choice(self.FRUIT_TYPES)
        
        color = (
            random.randint(150, 255),
            random.randint(0, 100),
            random.randint(0, 100),
        )
        fruit_image = load_or_create_fruit_image(self.fruit_type)
        super().__init__(x, y, width, height, color, image=fruit_image)


class Bomb(GameObject):
    name = "BOMB"

    def __init__(self, x, y, width=40, height=40):
        color = (20, 20, 20)
        bomb_image = load_or_create_bomb_image()
        super().__init__(x, y, width, height, color, image=bomb_image)
