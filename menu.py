import pygame
# Импортируем функцию запуска игры и настройки окна
from game import run_game
from settings import WIDTH, HEIGHT, FPS


def load_image(path, size=None):
    """
    Загружает изображение по указанному пути и при необходимости масштабирует.

    :param path: путь к файлу изображения
    :param size: новый размер (ширина, высота), если нужно изменить
    :return: загруженное и обработанное изображение
    """
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image


def menu_loop(window):
    """
    Основной цикл главного меню.
    Отображает фон и кнопки, обрабатывает нажатия мыши.

    :param window: окно Pygame для отрисовки
    """

    clock = pygame.time.Clock()

    # Загружаем и масштабируем фоновое изображение меню
    splash = pygame.image.load("assets/Background/bg001.png").convert()
    splash = pygame.transform.scale(splash, (WIDTH, HEIGHT))

    # Загружаем изображения кнопок с масштабированием
    start_button = load_image("assets/Menu/Buttons/play_normal.png", (160, 90))
    exit_button = load_image("assets/Menu/Buttons/Back.png", (100, 80))

    # Вычисляем позиции кнопок по центру экрана
    start_rect = start_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    exit_rect = exit_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем клик по кнопкам
                if start_rect.collidepoint(event.pos):
                    run_game(window)  # Запуск игры
                elif exit_rect.collidepoint(event.pos):
                    run = False  # Выход из меню и завершение программы

        # Отрисовываем фон и кнопки
        window.blit(splash, (0, 0))  # Фон
        window.blit(start_button, start_rect.topleft)  # Кнопка "Start"
        window.blit(exit_button, exit_rect.topleft)  # Кнопка "Exit"

        # Обновляем экран
        pygame.display.update()