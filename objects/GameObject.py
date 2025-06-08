import pygame
import random
import math


class GameObject:
    def __init__(self, x, y, width, height, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.vel_x = random.uniform(-3, 3)
        self.vel_y = random.uniform(-10, -8)
        self.acc_y = 0.1
        self.mass = 1.0

        self.bbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        """Обновление физики объекта"""
        self.vel_y += self.acc_y
        self.x += self.vel_x
        self.y += self.vel_y

        # Обновляем bbox
        self.bbox.x = int(self.x)
        self.bbox.y = int(self.y)

    def draw(self, screen):
        """Отрисовка объекта"""
        pygame.draw.rect(screen, self.color, self.bbox)

    def is_out_of_bounds(self, screen_width, screen_height):
        """Проверяет, вышел ли объект за пределы экрана"""
        return (
            self.y > screen_height + self.height
            or self.x < -self.width
            or self.x > screen_width + self.width
        )

    def check_collision(self, other):
        """Проверяет пересечение с другим объектом"""
        return self.bbox.colliderect(other.bbox)

    def resolve_collision(self, other):
        """Реакция на столкновение: упругий удар с физически корректным поведением"""
        # Центры объектов
        x1 = self.x + self.width / 2
        y1 = self.y + self.height / 2
        x2 = other.x + other.width / 2
        y2 = other.y + other.height / 2

        dx = x2 - x1
        dy = y2 - y1
        distance = math.hypot(dx, dy)
        min_dist = (self.width + other.width) / 2

        # Если нет пересечения — выходим
        if distance >= min_dist:
            return

        # Нормализуем вектор между центрами
        nx = dx / distance if distance != 0 else 0
        ny = dy / distance if distance != 0 else 0

        # Глубина проникновения
        overlap = min_dist - distance
        # Раздвигаем объекты, чтобы избежать липкости
        self.x -= overlap * nx * 0.5
        self.y -= overlap * ny * 0.5
        other.x += overlap * nx * 0.5
        other.y += overlap * ny * 0.5

        # Вычисляем относительную скорость по нормали
        v_self = (self.vel_x, self.vel_y)
        v_other = (other.vel_x, other.vel_y)

        # Проекции скоростей на нормаль
        v_self_n = v_self[0] * nx + v_self[1] * ny
        v_other_n = v_other[0] * nx + v_other[1] * ny

        # Относительная скорость по нормали
        dv_n = v_other_n - v_self_n

        # Если объекты уже двигаются друг от друга — ничего не делаем
        if dv_n > 0:
            return

        # Массы (можно сделать разные)
        m1 = self.mass
        m2 = other.mass
        restitution = 0.8  # Коэффициент восстановления (упругость), можно менять

        # Импульс (impulse scalar)
        j = -(1 + restitution) * dv_n
        j /= 1 / m1 + 1 / m2

        # Вектор импульса
        impulse_x = j * nx
        impulse_y = j * ny

        # Обновляем скорости
        self.vel_x -= impulse_x / m1
        self.vel_y -= impulse_y / m1
        other.vel_x += impulse_x / m2
        other.vel_y += impulse_y / m2

