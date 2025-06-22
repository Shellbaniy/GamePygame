import pygame
# Импортируем вспомогательные функции для загрузки текстур
from utils import get_block, load_sprite_sheets
# Импортируем настройки анимации
from settings import ANIMATION_DELAY


class Object(pygame.sprite.Sprite):
    """
    Базовый класс для всех объектов игры.
    Наследуется от pygame.sprite.Sprite — стандартного класса спрайтов Pygame.
    """

    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        # Прямоугольник для позиции и коллизий
        self.rect = pygame.Rect(x, y, width, height)
        # Поверхность изображения (с поддержкой прозрачности)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name  # Дополнительное имя объекта (например "fire")

    def draw(self, win, offset_x):
        """
        Рисует объект на экране с учётом смещения камеры (offset_x).
        :param win: окно рендеринга (surface)
        :param offset_x: горизонтальное смещение камеры
        """
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    """
    Класс статичного блока (платформы, земли и т.п.).
    Наследуется от Object.
    """

    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        # Загружаем текстуру блока и рисуем её на изображении спрайта
        block_img = get_block(size)
        self.image.blit(block_img, (0, 0))
        # Создаём маску для точных коллизий
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    """
    Класс огня — опасный объект с анимацией.
    Может быть в состоянии on (включён) или off (выключен).
    """

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, name="fire")
        # Загружаем анимационные спрайты ("on" и "off")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        # Стартовое изображение — выключенное
        self.image = self.fire["off"][0]
        # Маска для коллизии
        self.mask = pygame.mask.from_surface(self.image)
        # Счётчик для анимации
        self.animation_count = 0
        # Текущее состояние анимации
        self.animation_name = "off"

    def on(self):
        """Включает анимацию огня."""
        self.animation_name = "on"

    def off(self):
        """Выключает анимацию огня."""
        self.animation_name = "off"

    def loop(self):
        """
        Обновляет анимацию огня каждый кадр.
        Переключает кадры в зависимости от animation_count.
        """
        sprites = self.fire[self.animation_name]  # Получаем нужную последовательность
        index = (self.animation_count // ANIMATION_DELAY) % len(sprites)  # Вычисляем индекс кадра
        self.image = sprites[index]  # Устанавливаем текущий кадр
        self.animation_count += 1  # Увеличиваем счётчик

        # Обновляем rect и mask после изменения изображения
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        # Сбрасываем счётчик, если анимация закончилась
        if self.animation_count // ANIMATION_DELAY > len(sprites):
            self.animation_count = 0