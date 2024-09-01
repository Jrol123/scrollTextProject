import json
import argparse as prs
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont, ImageColor
from PIL.ImageFont import FreeTypeFont

from scrolltext_gif.vertical import draw_vertical

max_color_val = 255

global_font: FreeTypeFont


class Person:
    """

    :var name: Имя человека
    :type name: str
    :var color: Цвет текста для человека
    :type color: str | tuple[int, int, int] | tuple[int, int, int, int] | tuple[int, int, int, float]
    :var coords: Координаты текста. Считаются от левого верхнего угла картинки
    :type coords: list[float, float]

    """

    def __init__(self, name: str, color: str |
                                         tuple[int, int, int] |
                                         tuple[int, int, int, float] |
                                         tuple[int, int, int, int], font: FreeTypeFont, start_pos_x: float,
                 max_len_name: float) -> None:
        """

        :param name: Имя
        :param color: Цвет имени

        """
        self.name = name
        self.coords = [start_pos_x + (max_len_name - font.getlength(name)) / 2, 0]
        self.color = color

    def __str__(self) -> str:
        return f"Person(name={self.name}, color={self.color}, coords={self.coords})"

    def __repr__(self) -> str:
        return str(self)

    def draw(self, d: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont) -> None:
        """
        Рисование имени человека на нужном холсте

        :param d: Рисовальщик
        :param font: Шрифт текста

        :returns: Отрисовывает имя человека

        """
        d.text(self.coords, self.name, fill=self.color, font=font)


def is_valid_color(color: str |
                          list[int, int, int] |
                          list[int, int, int, float] |
                          list[int, int, int, int] |
                          None) -> ((str |
                                     tuple[int, int, int] |
                                     tuple[int, int, int, int]) |
                                    None):
    """
    Проверка на корректность цвета + его преобразование из float в int.
    :param color:
    :return: Цвет в корректной форме.
    :raises: TypeError, ValueError

    """
    if isinstance(color, str):
        if color.startswith("#"):
            if len(color[1:]) == 6 and color[1:].isalnum() and all(
                    char.isdigit() or char.lower() in 'abcdef' for char in color[1:]):
                return color
            raise ValueError("Неверное HEX значение цвета")
        elif color in ImageColor.colormap.keys():
            return color
        raise TypeError("Неверное наименование цвета в кавычках")

    elif isinstance(color, list):
        if all((isinstance(color_element, int) and 0 <= color_element <= 255) for color_element in color[0:3]):
            if len(color) == 3:
                return tuple(color)

            elif len(color) == 4:
                if isinstance(color[3], int) and 0 <= color[3] <= 255:
                    return tuple(color)
                elif isinstance(color[3], float) and 0 <= color[3] <= 1:
                    color[3] = int(color[3] * max_color_val)
                    return tuple(color)
                else:
                    raise ValueError("У вас сломалось 4-е значение в списке")
            raise ValueError("Неверное количество параметров в RGB")

        raise TypeError("Неверно набран RGB")

    elif color is None:
        return None
    else:
        raise TypeError("Неверный тип цвета")


parser = prs.ArgumentParser(prog="ScrollText", description="Описание программы", epilog='Text at the bottom of help')
parser.add_argument('config_path', type=str, help='Путь к конфигурационному файлу')
parser.add_argument("mode", choices=["v", "c"], type=str, default="v", help="Режим работы программы")
# TODO: Прикрутить Enum (?)
parser.add_argument(metavar="name", nargs='?', dest='output_filename', type=str,
                    default="output", help='Название выходного файла')

if __name__ == '__main__':
    # Ввод параметров
    args = parser.parse_args()
    with open(args.config_path) as f:
        data = json.load(f)
    color_background = data['color_background']
    """Цвет фона"""
    color_main_text = data['color_main_text']
    """Цвет текста"""

    # Обработка шрифта
    font_size = data['font_size']
    """Размер шрифта"""
    if data["font"] == "":
        global_font = ImageFont.truetype("arial.ttf",
                                         font_size)
    else:
        global_font = ImageFont.truetype(data["font"], font_size)
    """Шрифт"""

    # Обработка размеров
    height, width = data['height'], data['width']

    # Старая версия с пропорциями
    # height = 1200
    # width = (height * 16) // 9
    ## TODO: Разобраться с пропорциями.
    ##  Или заставить человека самостоятельно вводить разрешение...

    border = data['border']
    """Отступ от левой стенки"""
    start_pos_x = global_font.getlength(data['first_part'].encode("windows-1251").decode("utf-8")) + border
    """Стартовая позиция для написания имени"""

    diff_pos_y = font_size + font_size // 16
    """Разница в позициях между строками текста.
    
    Считается от левого верхнего угла.
    
    Коэффициент подобран вручную."""

    y_mid = height // 2 - font_size // 2
    """Позиция по y, такая, что при напечатывании в ней текста,
     его середина будет находиться на настоящей середине картинки."""
    # ! TODO: Сломалась центровка!
    #   На font_size=150 и 1920x1200 // 4 работает корректно. Ставит в центр Name4.
    #   На других раскладках ломается

    start_pos_y = height - font_size - font_size // 16
    """Нижняя позиция."""

    end_pos = start_pos_y - diff_pos_y * (len(data['people']) - 1)
    """Верхняя позиция.
    В неё переносится текст после выхода за нижнюю часть экрана."""
    # TODO: При малом количестве имён, спавнится внутри картинки.
    #   Реализовать корректный спавн за границами картинки.
    #   Вообще, надо сделать размещение не от низа картинки, а от центра

    # Обработка основных цветов
    if color_background == "" or color_background == []:
        color_background = (250, 250, 250)
    else:
        color_background = is_valid_color(color_background)
    if color_main_text == "" or color_main_text == []:
        color_main_text = (0, 0, 0)
    else:
        color_main_text = is_valid_color(color_main_text)

    # Обработка цветов людей
    count_colorless = 0
    """Количество людей без цвета"""
    name_list: list[
        list[str, str | list[int, int, int] | list[int, int, int, float] | list[int, int, int, int] | None]] = []
    for human_name in data['people']:
        color = data['people'][human_name]
        if color == "" or color == []:
            count_colorless += 1
            color = None
        color = is_valid_color(color)
        name_list.append([human_name.encode("windows-1251").decode("utf-8"), color])
    max_len_name = max([global_font.getlength(human[0]) for human in name_list])
    """Длина самого длинного имени"""

    # Генерация палитры
    color_palette = "magma"
    if data['color_palette'] != "" and data['color_palette'] != []:
        color_palette = data['color_palette']
    rgb_values = [tuple(int(layer * 255) for layer in color) for color in
                  sns.color_palette(color_palette, n_colors=(
                                                                count_colorless // 2 if count_colorless % 2 != 0 else count_colorless // 2 - 1) + 1)]
    """Генерация RGB-значений для людей без указанного цвета"""
    # TODO: Сделать возможность вводить "Стандартный цвет". Такой цвет, который будет использован для людей без цвета.
    #   Если такой параметр включён, не генерировать цвета.

    # Создание людей
    people_list: list[Person] = []
    """Список людей"""

    iter = 0
    middle = len(name_list) // 2 if len(name_list) % 2 != 0 else len(name_list) // 2 - 1
    """Последний индекс левой половины"""
    if len(rgb_values) != 0:
        for human in name_list:
            if human[1] is None:
                if iter > middle:
                    human[1] = rgb_values[middle - (iter - middle)]
                else:
                    human[1] = rgb_values[iter]
                iter += 1
            people_list.append(Person(human[0], human[1], global_font, start_pos_x, max_len_name))
    else:
        for human in name_list:
            people_list.append(Person(human[0], human[1], global_font, start_pos_x, max_len_name))
    # for person in people_list: print(person)
    # ! DEBUG

    for i, item in enumerate(people_list):
        item.coords[1] = start_pos_y - diff_pos_y * i

    step = 5
    """Сдвиг строк"""

    percentile = diff_pos_y // step
    """Вычисление количества шагов, необходимых для того, чтобы текст вышел за нижнюю границу картинки"""
    # print(percentile, diff_pos_y / step)
    # ! Debug
    count_cycles = len(name_list) - 0
    """Количество прокруток.
    
    По-умолчанию один полный круг (len(people_list) шагов)"""

    count_iter = percentile * count_cycles
    """Количество кадров"""

    im_base = Image.new('RGB', (width, height), color_background)
    d_base = ImageDraw.Draw(im_base)
    d_base.text((border, y_mid), data['first_part'].encode("windows-1251").decode("utf-8"), fill=color_main_text,
                font=global_font)
    d_base.text((start_pos_x + max_len_name, y_mid), data['second_part'].encode("windows-1251").decode("utf-8"),
                fill=color_main_text, font=global_font)

    """Заготовка заднего фона"""

    if args.mode == 'v':
        draw_vertical(im_base, people_list, count_iter, percentile, end_pos, step, global_font, args.output_filename,
                      data['save_frames'])
