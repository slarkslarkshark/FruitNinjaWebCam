import pygame
from .PygameWindow import PygameWindow
from .Button import Button
from objects.Player import Player
from objects.Objects import Fruit, Bomb
from objects.Explosion import Explosion
from objects.FingerTrail import FingerTrail, FingerIcon
import cv2
import random
import threading
import time
import math
from config import Config as cfg
from shapely.geometry import Polygon, LineString, Point


class GameWindow(PygameWindow):
    def __init__(
        self,
        player,
    ):
        super().__init__()

        self.back_button = Button(20, 20, 100, 40, "Quit", self.font)
        self.back_button.on_click(lambda: self.switch_window(MainMenuWindow()))
        self.buttons = [self.back_button]

        self.player = player
        self.trail = FingerTrail()
        self.finger_icon = FingerIcon()
        self.SPAWN_INTERVAL = cfg.SPAWN_INTERVAL
        self.score = 0
        self.BOMB_PROB = cfg.get("bomb_prob")
        self.SCORE_TO_WIN = cfg.get("score_to_win")
        self.health = cfg.get("health")

        self.objects = []
        self.explosions = []  # Store active explosion animations

        self.last_spawn_time = pygame.time.get_ticks()

    def update_trail(self):
        """Update finger trail and icon"""
        finger_pos = self.player.get_finger_position()
        if finger_pos:
            self.trail.add_point(finger_pos[1], finger_pos[0])
        
        self.trail.update()
        self.finger_icon.update()

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(
            f"Fruits left: {self.SCORE_TO_WIN - self.score}", True, (255, 255, 255)
        )
        text_rect = score_text.get_rect(topright=(self.window_width - 20, 20))
        self.screen.blit(score_text, text_rect)

    def spawn_object(self):
        x = random.randint(0, self.window_width - 50)
        y = self.window_height
        if random.random() <= self.BOMB_PROB:
            obj = Bomb(x, y)
        else:
            obj = Fruit(x, y)
        self.objects.append(obj)

    def update_objects(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.SPAWN_INTERVAL:
            self.spawn_object()
            self.last_spawn_time = current_time

        for obj in self.objects:
            obj.update()

        self.objects = [
            obj
            for obj in self.objects
            if not obj.is_out_of_bounds(self.window_width, self.window_height)
        ]
        for i, obj_a in enumerate(self.objects):
            for j, obj_b in enumerate(self.objects):
                if i >= j:
                    continue  # Избегаем повторных проверок
                if obj_a.check_collision(obj_b):
                    obj_a.resolve_collision(obj_b)

        # Convert trail points for collision detection
        trail_points_list = [(point.x, point.y) for point in self.trail.trail_points if point.age < 300]
        if len(trail_points_list) >= 2:
            trail = LineString(trail_points_list)
        elif len(trail_points_list) == 1:
            trail = Point(trail_points_list[0])
        else:
            return
        new_objects = []
        for obj in self.objects:
            x = obj.x
            y = obj.y
            w = obj.width
            h = obj.height
            polygon = Polygon([(x, y), (x, y + h), (x + w, y + h), (x + w, y), (x, y)])

            if (isinstance(trail, LineString) and not polygon.intersects(trail)) or (
                isinstance(trail, Point) and not polygon.contains(trail)
            ):
                new_objects.append(obj)
            else:
                if obj.name == "FRUIT":
                    self.score += 1
                elif obj.name == "BOMB":
                    self.health -= 1
                    # Create explosion animation at bomb position
                    bomb_center_x = obj.x + obj.width / 2
                    bomb_center_y = obj.y + obj.height / 2
                    explosion = Explosion(bomb_center_x, bomb_center_y)
                    self.explosions.append(explosion)

        self.objects = new_objects

    def draw_objects(self):
        for obj in self.objects:
            obj.draw(self.screen)

    def draw_health(self):
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {self.health}", True, (255, 255, 255))

        padding = 20
        text_rect = health_text.get_rect(
            bottomright=(self.window_width - padding, self.window_height - padding)
        )

        self.screen.blit(health_text, text_rect)

    def check_victory(self):
        if self.score >= self.SCORE_TO_WIN:
            self.is_running = False
            self.switch_window(VictoryWindow())

    def check_game_over(self):
        if self.health <= 0:
            self.is_running = False
            self.switch_window(GameOverWindow())

    def update_explosions(self):
        """Update all active explosion animations"""
        self.explosions = [exp for exp in self.explosions if exp.update()]

    def update(self):
        self.update_objects()
        self.update_explosions()
        self.update_trail()
        self.check_victory()
        self.check_game_over()

    def draw_explosions(self):
        """Draw all active explosion animations"""
        for explosion in self.explosions:
            explosion.draw(self.screen)

    def draw(self):
        frame = self.player.get_frame()
        if frame is not None:
            # Convert frame to pygame surface (without drawing trail on cv2 frame)
            frame_surface = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame_surface, (0, 0))

        # Draw trail using pygame (better animations)
        self.trail.draw(self.screen)
        
        # Draw animated finger icon
        finger_pos = self.player.get_finger_position()
        if finger_pos:
            self.finger_icon.draw(self.screen, finger_pos[1], finger_pos[0])

        self.draw_objects()
        self.draw_explosions()  # Draw explosions on top of objects
        self.draw_health()
        self.draw_score()

    def switch_window(self, next_window):
        self.next_window = next_window
        self.is_running = False
        self.objects = []
        self.explosions = []  # Clear explosions when switching windows
        self.trail.clear()  # Clear trail when switching windows
        self.score = 0
        self.health = 1
        self.on_exit()

    def on_exit(self):
        self.player.release()


class GameOverWindow(PygameWindow):
    def __init__(self):
        super().__init__(background=(150, 50, 50))  # Dark red background

        self.back_button = Button(
            20, 20, 200, 50, "Main Menu", self.font,
            color=(100, 150, 200),
            hover_color=(150, 200, 255),
            text_color=(255, 255, 255),
        )
        self.back_button.on_click(lambda: self.switch_window(MainMenuWindow()))
        self.buttons = [self.back_button]
        self.animation_time = 0

    def update(self):
        self.animation_time += 0.05

    def draw(self):
        # Draw gradient background
        for y in range(self.window_height):
            r = int(150 + (100 - 150) * y / self.window_height)
            g = int(50 + (30 - 50) * y / self.window_height)
            b = int(50 + (30 - 50) * y / self.window_height)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.window_width, y))

        title_font = pygame.font.Font(None, 90)
        game_over_text = "Game Over"
        
        # Pulsing effect
        pulse = int(30 * math.sin(self.animation_time * 2))
        color = (
            max(0, min(255, 200 + pulse)),
            max(0, min(255, 20 + pulse)),
            max(0, min(255, 20 + pulse))
        )
        
        # Shadow
        shadow_surface = title_font.render(game_over_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(
            center=(self.window_width // 2 + 3, self.window_height // 3 + 3)
        )
        self.screen.blit(shadow_surface, shadow_rect)
        
        title_surface = title_font.render(game_over_text, True, color)
        title_rect = title_surface.get_rect(
            center=(self.window_width // 2, self.window_height // 3)
        )
        self.screen.blit(title_surface, title_rect)

        subtitle_font = pygame.font.Font(None, 40)
        subtitle_text = subtitle_font.render("Try again!", True, (255, 255, 200))
        subtitle_rect = subtitle_text.get_rect(
            center=(self.window_width // 2, self.window_height // 2)
        )
        self.screen.blit(subtitle_text, subtitle_rect)


class VictoryWindow(PygameWindow):
    def __init__(self):
        super().__init__(background=(255, 240, 150))  # Light golden background

        self.back_button = Button(
            20, 20, 200, 50, "Main Menu", self.font,
            color=(100, 200, 100),
            hover_color=(150, 255, 150),
            text_color=(255, 255, 255),
        )
        self.back_button.on_click(lambda: self.switch_window(MainMenuWindow()))
        self.buttons = [self.back_button]
        self.animation_time = 0

    def update(self):
        self.animation_time += 0.03

    def draw(self):
        # Draw gradient background
        for y in range(self.window_height):
            r = int(255 + (200 - 255) * y / self.window_height)
            g = int(240 + (180 - 240) * y / self.window_height)
            b = int(150 + (100 - 150) * y / self.window_height)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.window_width, y))

        # Draw animated confetti/fruit particles
        for i in range(20):
            x = (i * 30 + self.animation_time * 20) % (self.window_width + 40) - 20
            y = (i * 25 + self.animation_time * 15) % (self.window_height + 40) - 20
            size = 5 + int(3 * math.sin(self.animation_time + i))
            color = random.choice([(255, 100, 100), (255, 200, 100), (100, 255, 100), (255, 150, 200)])
            pygame.draw.circle(self.screen, color, (int(x), int(y)), size)

        title_font = pygame.font.Font(None, 90)
        title_text = "Victory!"
        
        # Pulsing effect
        pulse = int(20 * math.sin(self.animation_time * 2))
        color = (
            max(0, min(255, 255 + pulse)),
            max(0, min(255, 50 + pulse)),
            max(0, min(255, 50 + pulse))
        )
        
        # Shadow
        shadow_surface = title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(
            center=(self.window_width // 2 + 3, self.window_height // 2 + 3)
        )
        self.screen.blit(shadow_surface, shadow_rect)
        
        title_surface = title_font.render(title_text, True, color)
        title_rect = title_surface.get_rect(
            center=(self.window_width // 2, self.window_height // 2)
        )
        self.screen.blit(title_surface, title_rect)
        
        subtitle_font = pygame.font.Font(None, 35)
        subtitle_text = subtitle_font.render("You sliced all the fruits!", True, (100, 100, 100))
        subtitle_rect = subtitle_text.get_rect(
            center=(self.window_width // 2, self.window_height // 2 + 60)
        )
        self.screen.blit(subtitle_text, subtitle_rect)


class LoadingWindow(PygameWindow):
    def __init__(self):
        super().__init__()
        self.loading_dots = 10
        self.player = None
        self.initialized = False

        self.loading_thread = threading.Thread(target=self._init_player, daemon=True)
        self.loading_thread.start()

    def _init_player(self):
        try:
            self.player = Player()
            self.initialized = True
        except Exception as e:
            print("Ошибка при инициализации камеры:", e)

    def draw(self):
        # Draw colorful gradient background
        for y in range(self.window_height):
            r = int(100 + (150 - 100) * y / self.window_height)
            g = int(150 + (200 - 150) * y / self.window_height)
            b = int(255 + (255 - 255) * y / self.window_height)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.window_width, y))
        
        self.loading_dots = (self.loading_dots + 1) % 4
        dots = "." * self.loading_dots
        
        # Draw animated loading text
        title_font = pygame.font.Font(None, 60)
        loading_text = f"Loading{dots}"
        
        # Shadow
        shadow_surface = title_font.render(loading_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(
            center=(self.window_width // 2 + 2, self.window_height // 2 + 2)
        )
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Main text
        text_surface = title_font.render(loading_text, True, (255, 100, 100))
        text_rect = text_surface.get_rect(
            center=(self.window_width // 2, self.window_height // 2)
        )
        self.screen.blit(text_surface, text_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, 30)
        subtitle = subtitle_font.render("Initializing camera...", True, (100, 100, 100))
        subtitle_rect = subtitle.get_rect(
            center=(self.window_width // 2, self.window_height // 2 + 50)
        )
        self.screen.blit(subtitle, subtitle_rect)
        
        time.sleep(0.2)

    def update(self):
        if self.initialized and self.player.get_frame() is not None:
            self.switch_window(GameWindow(player=self.player))


class MainMenuWindow(PygameWindow):
    def __init__(self):
        super().__init__(background=(135, 206, 250))  # Light sky blue background
        
        # Animated fruit decorations
        self.fruit_decorations = []
        self.animation_time = 0
        
        # Create floating fruit decorations using the fruit creation functions
        from objects.Objects import create_apple_icon, create_orange_icon, create_strawberry_icon
        fruit_types = [create_apple_icon, create_orange_icon, create_strawberry_icon]
        
        for i in range(8):
            fruit_type = random.choice(fruit_types)
            self.fruit_decorations.append({
                'image': fruit_type(),
                'x': random.randint(50, self.window_width - 50),
                'y': random.randint(50, self.window_height - 200),
                'speed': random.uniform(0.5, 1.5),
                'angle': random.uniform(0, 2 * math.pi),
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-2, 2),
            })

        button_width, button_height = 250, 60
        padding = 25
        start_y = (self.window_height - (3 * button_height + 2 * padding)) // 2

        # Colorful buttons matching fruit theme
        self.play_button = Button(
            (self.window_width - button_width) // 2,
            start_y,
            button_width,
            button_height,
            "Play",
            self.font,
            color=(255, 100, 100),  # Apple red
            hover_color=(255, 150, 150),
            text_color=(255, 255, 255),
        )
        self.settings_button = Button(
            (self.window_width - button_width) // 2,
            start_y + button_height + padding,
            button_width,
            button_height,
            "Settings",
            self.font,
            color=(255, 165, 0),  # Orange
            hover_color=(255, 200, 100),
            text_color=(255, 255, 255),
        )
        self.exit_button = Button(
            (self.window_width - button_width) // 2,
            start_y + 2 * (button_height + padding),
            button_width,
            button_height,
            "Exit",
            self.font,
            color=(200, 50, 50),  # Dark red
            hover_color=(255, 100, 100),
            text_color=(255, 255, 255),
        )

        self.play_button.on_click(lambda: self.switch_window(LoadingWindow()))
        self.settings_button.on_click(lambda: self.switch_window(SettingsWindow()))
        self.exit_button.on_click(lambda: self.close_game())

        self.buttons = [self.play_button, self.settings_button, self.exit_button]

    def close_game(self):
        self.is_running = False
        pygame.quit()
        exit()

    def update(self):
        """Update floating fruit animations"""
        self.animation_time += 0.02
        for fruit in self.fruit_decorations:
            fruit['rotation'] += fruit['rotation_speed']
            # Gentle floating motion
            fruit['y'] += math.sin(self.animation_time + fruit['x'] * 0.01) * 0.5
            fruit['x'] += math.cos(self.animation_time * 0.5 + fruit['y'] * 0.01) * 0.3
            
            # Wrap around screen edges
            if fruit['x'] < -50:
                fruit['x'] = self.window_width + 50
            elif fruit['x'] > self.window_width + 50:
                fruit['x'] = -50
            if fruit['y'] < -50:
                fruit['y'] = self.window_height + 50
            elif fruit['y'] > self.window_height + 50:
                fruit['y'] = -50

    def draw(self):
        # Draw gradient background
        for y in range(self.window_height):
            # Gradient from light blue to light green
            r = int(135 + (50 - 135) * y / self.window_height)
            g = int(206 + (200 - 206) * y / self.window_height)
            b = int(250 + (100 - 250) * y / self.window_height)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.window_width, y))
        
        # Draw floating fruit decorations
        for fruit in self.fruit_decorations:
            rotated_image = pygame.transform.rotate(fruit['image'], fruit['rotation'])
            img_rect = rotated_image.get_rect(center=(int(fruit['x']), int(fruit['y'])))
            # Add transparency for background effect
            fruit_surface = pygame.Surface(rotated_image.get_size(), pygame.SRCALPHA)
            fruit_surface.blit(rotated_image, (0, 0))
            fruit_surface.set_alpha(150)  # Semi-transparent
            self.screen.blit(fruit_surface, img_rect)
        
        # Draw title with colorful gradient effect
        title_font = pygame.font.Font(None, 90)
        title_text = "Fruit Ninja WebCam"
        
        # Draw title with shadow and gradient effect
        shadow_surface = title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.window_width // 2 + 3, 103))
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Draw title with gradient colors
        title_surface = title_font.render(title_text, True, (255, 50, 50))
        title_rect = title_surface.get_rect(center=(self.window_width // 2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_font = pygame.font.Font(None, 30)
        subtitle_text = subtitle_font.render("Slice fruits with your finger!", True, (50, 50, 50))
        subtitle_rect = subtitle_text.get_rect(center=(self.window_width // 2, 150))
        self.screen.blit(subtitle_text, subtitle_rect)


class SettingsWindow(PygameWindow):
    def __init__(self):
        super().__init__(background=(180, 220, 255))  # Light blue background

        self.back_button = Button(
            20, 20, 120, 45, "Back", self.font,
            color=(100, 150, 200),
            hover_color=(150, 200, 255),
            text_color=(255, 255, 255),
        )
        self.back_button.on_click(lambda: self.switch_window(MainMenuWindow()))

        self.level_buttons = {}
        self.animation_time = 0

        self.buttons = [self.back_button]

        self.create_level_buttons()

    def create_level_buttons(self):
        button_width = 250
        button_height = 60
        padding = 30
        start_x = (self.window_width - button_width) // 2

        levels = ["easy", "medium", "hard"]
        level_colors = {
            "easy": ((100, 255, 100), (150, 255, 150)),  # Green
            "medium": ((255, 200, 100), (255, 230, 150)),  # Yellow
            "hard": ((255, 100, 100), (255, 150, 150)),  # Red
        }

        for i, level in enumerate(levels):
            start_y = (
                self.window_height
                - (len(levels) * button_height + (len(levels) - 1) * padding)
            ) // 2 + i * (button_height + padding)

            color, hover_color = level_colors[level]
            btn = Button(
                start_x,
                start_y,
                button_width,
                button_height,
                f"{level.capitalize()}",
                self.font,
                color=color,
                hover_color=hover_color,
                text_color=(255, 255, 255),
            )
            btn.on_click(lambda l=level: self.set_level(l))
            self.level_buttons[level] = btn
            self.buttons.append(btn)

    def set_level(self, level):
        cfg.LEVEL = level

        self.buttons = [self.back_button]
        self.create_level_buttons()

    def update(self):
        self.animation_time += 0.02

    def draw(self):
        # Draw gradient background
        for y in range(self.window_height):
            r = int(180 + (200 - 180) * y / self.window_height)
            g = int(220 + (230 - 220) * y / self.window_height)
            b = int(255 + (255 - 255) * y / self.window_height)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.window_width, y))

        title_font = pygame.font.Font(None, 70)
        title_text = "Select Difficulty"
        
        # Draw title with shadow
        shadow_surface = title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.window_width // 2 + 3, 103))
        self.screen.blit(shadow_surface, shadow_rect)
        
        title_surface = title_font.render(title_text, True, (50, 50, 150))
        title_rect = title_surface.get_rect(center=(self.window_width // 2, 100))
        self.screen.blit(title_surface, title_rect)

        current_level = cfg.LEVEL

        # Define level colors
        level_colors = {
            "easy": ((100, 255, 100), (150, 255, 150)),  # Green
            "medium": ((255, 200, 100), (255, 230, 150)),  # Yellow
            "hard": ((255, 100, 100), (255, 150, 150)),  # Red
        }

        # Highlight selected level with pulsing effect
        pulse = int(20 * math.sin(self.animation_time * 3))
        for level, button in self.level_buttons.items():
            original_color, original_hover = level_colors[level]
            if level == current_level:
                # Apply pulse with proper clamping for selected button
                button.color = tuple(max(0, min(255, c + pulse)) for c in original_color)
                button.hover_color = tuple(max(0, min(255, c + pulse)) for c in original_hover)
            else:
                # Reset to original colors for non-selected buttons
                button.color = original_color
                button.hover_color = original_hover

    def switch_window(self, next_window):
        self.next_window = next_window
        self.is_running = False
