# Карта уровня — текстовое представление расположения объектов.
#   'X' — блок (земля/платформа)
#   'F' — огонь (враждебный элемент)
LEVEL_MAP = [
    "                        ",
    "                        ",
    "     X                  ",
    "   F     X       X       ",
    "   XX         XX   XX     ",
    "X     XX    XX   X    F ",
    "XXXXXXXXXXXXXXXXXXXXXXXX"
]


def parse_level(level_map, block_cls, fire_cls, block_size):
    """
    Парсит уровень из текстового представления в список объектов.

    :param level_map: список строк, описывающих уровень
    :param block_cls: класс блока (например, Block)
    :param fire_cls: класс огня (например, Fire)
    :param block_size: размер одного тайла (блока)
    :return: список объектов уровня
    """
    objects = []

    for i, row in enumerate(level_map):  # i - номер строки (ось Y)
        for j, tile in enumerate(row):  # j - номер символа в строке (ось X)

            # Вычисляем координаты тайла
            x = j * block_size
            y = i * block_size

            if tile == "X":
                # Создаём блок
                block = block_cls(x, y, block_size)
                objects.append(block)

            elif tile == "F":
                # Создаём огонь (ширина 16, высота 32)
                fire = fire_cls(x, y, 16, 32)
                fire.on()  # Запускаем анимацию огня
                objects.append(fire)

    return objects