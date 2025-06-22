import pygame
# Импортируем настройки окна (WIDTH, HEIGHT)
from settings import WIDTH, HEIGHT
# Импортируем функцию-цикл меню
from menu import menu_loop


def main():
    """
    Основная функция запуска игры.
    Инициализирует Pygame, создаёт окно и запускает главное меню.
    """

    # Инициализация всех модулей Pygame
    pygame.init()

    # Устанавливаем заголовок окна
    pygame.display.set_caption("Platformer")

    # Создаём окно игры с заданными размерами
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    # Запускаем цикл главного меню. После выхода из меню — начинается игра или выход из программы
    menu_loop(window)

    # Выход из Pygame после завершения работы
    pygame.quit()


# Проверяем, запускается ли файл напрямую, а не импортируется как модуль
if __name__ == "__main__":
    main()