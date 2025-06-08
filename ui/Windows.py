import pygame
from .PygameWindow import PygameWindow
from .Button import Button
from objects.Player import Player
from objects.Objects import Fruit, Bomb
import cv2
import random
import threading
import time
from config import Config as cfg
from shapely.geometry import Polygon, LineString, Point


class GameWindow(PygameWindow):
    MAX_TRAIL_LENGTH = 10

    def __init__(
        self,
        player,
    ):
        super().__init__()

        self.back_button = Button(20, 20, 100, 40, "Quit", self.font)
        self.back_button.on_click(lambda: self.switch_window(MainMenuWindow()))
        self.buttons = [self.back_button]

        self.player = player
        self.trail_points = []
        self.SPAWN_INTERVAL = cfg.SPAWN_INTERVAL
        self.time_trail_counter = 0
        self.score = 0
        self.BOMB_PROB = cfg.get("bomb_prob")
        self.SCORE_TO_WIN = cfg.get("score_to_win")
        self.health = cfg.get("health")

        self.objects = []

        self.last_spawn_time = pygame.time.get_ticks()

    def update_trail(self):
        finger_pos = self.player.get_finger_position()
        if finger_pos:
            self.time_trail_counter = 0
            self.trail_points.append(finger_pos)
            if len(self.trail_points) > self.MAX_TRAIL_LENGTH:
                self.trail_points.pop(0)
        elif self.trail_points:
            self.time_trail_counter += 1

        if self.time_trail_counter >= 3 and self.trail_points:
            self.trail_points = []
            self.time_trail_counter = 0

    def _draw_trail(self, frame):
        if len(self.trail_points) < 2:
            return frame

        for i in range(len(self.trail_points) - 1):
            start = tuple(map(int, self.trail_points[i]))
            end = tuple(map(int, self.trail_points[i + 1]))

            color = (255, 255, 255)

            cv2.line(frame, start, end, color, thickness=2)
        return frame

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

        trail = [(y, x) for x, y in self.trail_points]
        if len(trail) >= 2:
            trail = LineString(trail)
        elif len(trail) == 1:
            trail = Point(trail)
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

    def update(self):
        self.update_objects()
        self.update_trail()
        self.check_victory()
        self.check_game_over()

    def draw(self):
        frame = self.player.get_frame()
        if frame is not None:
            frame = self._draw_trail(frame)
            frame_surface = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame_surface, (0, 0))

        self.draw_objects()
        self.draw_health()
        self.draw_score()

    def switch_window(self, next_window):
        self.next_window = next_window
        self.is_running = False
        self.objects = []
        self.score = 0
        self.health = 1
        self.on_exit()

    def on_exit(self):
        self.player.release()


class GameOverWindow(PygameWindow):
    def __init__(self):
        super().__init__(background=(50, 50, 50))

        self.back_button = Button(20, 20, 200, 50, "Main Menu", self.font)
        self.back_button.on_click(lambda: self.switch_window(MainMenuWindow()))
        self.buttons = [self.back_button]

    def draw(self):
        super().draw()

        title_font = pygame.font.Font(None, 74)
        game_over_text = title_font.render("Game over...", True, (200, 20, 20))
        game_over_rect = game_over_text.get_rect(
            center=(self.window_width // 2, self.window_height // 3)
        )
        self.screen.blit(game_over_text, game_over_rect)

        subtitle_font = pygame.font.Font(None, 36)
        subtitle_text = subtitle_font.render("Try again!", True, (150, 150, 150))
        subtitle_rect = subtitle_text.get_rect(
            center=(self.window_width // 2, self.window_height // 2)
        )
        self.screen.blit(subtitle_text, subtitle_rect)


class VictoryWindow(PygameWindow):
    def __init__(self):
        super().__init__(background=(255, 223, 0))

        self.back_button = Button(20, 20, 200, 50, "Main Menu", self.font)
        self.back_button.on_click(lambda: self.switch_window(MainMenuWindow()))
        self.buttons = [self.back_button]

    def draw(self):
        super().draw()

        for i in range(0, self.window_width, 60):
            for j in range(0, self.window_height, 60):
                pygame.draw.circle(self.screen, (255, 255, 0), (i, j), 3)

        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("Victory!", True, (255, 0, 0))
        title_rect = title_text.get_rect(
            center=(self.window_width // 2, self.window_height // 2)
        )
        self.screen.blit(title_text, title_rect)


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
        super().draw()
        self.loading_dots = (self.loading_dots + 1) % 4
        dots = "." * self.loading_dots
        title_font = pygame.font.Font(None, 50)
        loading_text = title_font.render(f"Loading{dots}", True, (255, 255, 255))
        loading_rect = loading_text.get_rect(
            center=(self.window_width // 2, self.window_height // 2)
        )
        self.screen.blit(loading_text, loading_rect)
        time.sleep(0.2)

    def update(self):
        if self.initialized and self.player.get_frame() is not None:
            self.switch_window(GameWindow(player=self.player))


class MainMenuWindow(PygameWindow):
    def __init__(self):
        super().__init__(background=(30, 30, 30))

        button_width, button_height = 200, 50
        padding = 20
        start_y = (self.window_height - (3 * button_height + 2 * padding)) // 2

        self.play_button = Button(
            (self.window_width - button_width) // 2,
            start_y,
            button_width,
            button_height,
            "Play",
            self.font,
        )
        self.settings_button = Button(
            (self.window_width - button_width) // 2,
            start_y + button_height + padding,
            button_width,
            button_height,
            "Settings",
            self.font,
        )
        self.exit_button = Button(
            (self.window_width - button_width) // 2,
            start_y + 2 * (button_height + padding),
            button_width,
            button_height,
            "Exit",
            self.font,
        )

        self.play_button.on_click(lambda: self.switch_window(LoadingWindow()))
        self.settings_button.on_click(lambda: self.switch_window(SettingsWindow()))
        self.exit_button.on_click(lambda: self.close_game())

        self.buttons = [self.play_button, self.settings_button, self.exit_button]

    def close_game(self):
        self.is_running = False
        pygame.quit()
        exit()

    def draw(self):
        super().draw()
        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("Main Menu", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.window_width // 2, 100))
        self.screen.blit(title_text, title_rect)


class SettingsWindow(PygameWindow):
    def __init__(self):
        super().__init__(background=(40, 40, 40))

        self.back_button = Button(20, 20, 100, 40, "Back", self.font)
        self.back_button.on_click(lambda: self.switch_window(MainMenuWindow()))

        self.level_buttons = {}

        self.buttons = [self.back_button]

        self.create_level_buttons()

    def create_level_buttons(self):
        button_width = 200
        button_height = 50
        padding = 30
        start_x = (self.window_width - button_width) // 2

        levels = ["easy", "medium", "hard"]

        for i, level in enumerate(levels):
            start_y = (
                self.window_height
                - (len(levels) * button_height + (len(levels) - 1) * padding)
            ) // 2 + i * (button_height + padding)

            btn = Button(
                start_x,
                start_y,
                button_width,
                button_height,
                level.capitalize(),
                self.font,
            )
            btn.on_click(lambda l=level: self.set_level(l))
            self.level_buttons[level] = btn
            self.buttons.append(btn)

    def set_level(self, level):
        cfg.LEVEL = level

        self.buttons = [self.back_button]
        self.create_level_buttons()

    def draw(self):
        super().draw()

        title_font = pygame.font.Font(None, 50)
        title_text = title_font.render("Select Difficulty", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.window_width // 2, 80))
        self.screen.blit(title_text, title_rect)

        current_level = cfg.LEVEL

        for level, button in self.level_buttons.items():
            if level == current_level:
                button.color = (0, 200, 0)
                button.hover_color = (0, 255, 0)
            else:
                button.color = (100, 100, 100)
                button.hover_color = (150, 150, 150)

    def switch_window(self, next_window):
        self.next_window = next_window
        self.is_running = False
