from .GameObject import GameObject
import random


class Fruit(GameObject):
    name = "FRUIT"

    def __init__(self, x, y, width=40, height=40):
        color = (
            random.randint(150, 255),
            random.randint(0, 100),
            random.randint(0, 100),
        )
        super().__init__(x, y, width, height, color)

        # Можно добавить изображение вместо прямоугольника
        # self.image = pygame.image.load("apple.png")


class Bomb(GameObject):
    name = "BOMB"

    def __init__(self, x, y, width=40, height=40):
        color = (20, 20, 20)
        super().__init__(x, y, width, height, color)
