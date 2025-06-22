import pygame
from settings import WIDTH, HEIGHT, PLAYER_VEL, FPS, SCROLL_AREA_WIDTH  # Настройки проекта
from utils import get_background  # Функция для загрузки фонового изображения
from level import LEVEL_MAP, parse_level  # Уровень и функция парсинга уровня
from player import Player  # Класс игрока
from objects import Block, Fire  # Объекты уровня: блоки и огонь


def handle_vertical_collision(player, objects, dy):
    """
    Обработка вертикальных коллизий (столкновений) игрока с объектами.
    dy - изменение по оси Y (скорость падения или прыжка).
    """
    collided = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):  # Точное столкновение через маску
            if dy > 0:  # Падение вниз — игрок приземляется
                player.rect.bottom = obj.rect.top
                player.landed()  # Метод для завершения падения
            elif dy < 0:  # Столкновение сверху — удар головой
                player.rect.top = obj.rect.bottom
                player.hit_head()  # Метод "удара головой"
            collided.append(obj)
    return collided


def collide(player, objects, dx):
    """
    Проверяет столкновения по горизонтали.
    dx - временный сдвиг на dx, чтобы проверить коллизию.
    """
    player.move(dx, 0)
    player.update()
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            player.move(-dx, 0)  # Отменяем движение, если столкнулись
            player.update()
            return obj  # Возвращаем объект столкновения
    player.move(-dx, 0)  # Если не столкнулись — откатываем движение
    player.update()
    return None


def handle_move(player, objects):
    """
    Обработка движения игрока: влево/вправо, прыжки.
    Также проверяет столкновения с огнём.
    """
    keys = pygame.key.get_pressed()
    player.x_vel = 0  # Сбрасываем горизонтальную скорость
    left = collide(player, objects, -PLAYER_VEL * 2)  # Проверяем слева
    right = collide(player, objects, PLAYER_VEL * 2)  # Проверяем справа

    # Движение по клавишам, если нет препятствий
    if keys[pygame.K_LEFT] and not left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not right:
        player.move_right(PLAYER_VEL)

    # Проверка вертикального столкновения
    vertical = handle_vertical_collision(player, objects, player.y_vel)

    # Проверка столкновения с огнём
    for obj in [left, right, *vertical]:
        if obj and obj.name == "fire":
            player.make_hit()  # Игрок получает урон


def draw(window, background, bg_image, player, objects, offset_x):
    """
    Отрисовывает фон, объекты и игрока с учётом смещения камеры (offset_x).
    """
    for tile in background:
        window.blit(bg_image, tile)  # Рисуем фоновые тайлы
    for obj in objects:
        obj.draw(window, offset_x)  # Рисуем объекты
    player.draw(window, offset_x)  # Рисуем игрока
    pygame.display.update()  # Обновляем экран


def run_game(window):
    """
    Основной игровой цикл.
    """
    clock = pygame.time.Clock()
    background, bg_image = get_background("Purple.png", WIDTH, HEIGHT)  # Загружаем фон
    player = Player(100, 100, 50, 50)  # Создаём игрока
    objects = parse_level(LEVEL_MAP, Block, Fire, 96)  # Парсим уровень

    offset_x = 0  # Горизонтальное смещение камеры
    run = True

    while run:
        clock.tick(FPS)  # Ограничиваем частоту кадров

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()  # Прыжок, если ещё можно

        player.loop(FPS)  # Обновление состояния игрока
        for obj in objects:
            if hasattr(obj, "loop"):  # Например, анимация огня
                obj.loop()
        handle_move(player, objects)  # Обработка движения

        draw(window, background, bg_image, player, objects, offset_x)  # Отрисовка

        # Логика скроллинга (движения камеры)
        if ((player.rect.right - offset_x >= WIDTH - SCROLL_AREA_WIDTH and player.x_vel > 0)
                or (player.rect.left - offset_x <= SCROLL_AREA_WIDTH and player.x_vel < 0)):
            offset_x += player.x_vel  # Изменяем смещение камеры

    pygame.quit()  # Выход из Pygame