from PIL import ImageDraw, ImageFont
import json
import argparse as prs
import seaborn as sns

max_color_val = 255

color_text = (0, 0, 0)
"""Цвет стандартного текста"""

font_size = 160
# TODO: Переделать под размеры экрана и пропорции
myFont = ImageFont.truetype(r"C:\Users\artem\AppData\Local\Microsoft\Windows\Fonts\Rubik-Regular.ttf", font_size)

height = 1200
width = (height * 16) // 9
# TODO: Разобраться с пропорциями.
#  Или заставить человека самостоятельно вводить разрешение...
# TODO: Перенести

border = 10
"""Отступ от левой стенки"""
# TODO: Сделать задаваемый отступ
start_pos_x = myFont.getlength('Спокойной ночи, ') + border
"""Стартовая позиция для написания имени"""

max_len_name: float
"""Длина самого длинного имени"""

diff_pos_y = font_size + font_size // 16
"""Разница в позициях между строками текста.

Считается от левого верхнего угла.

Коэффициент подобран вручную."""

y_mid = height // 2 - font_size // 2
"""Позиция по y, такая, что при напечатывании в ней текста,
 его середина будет находиться на настоящей середине картинки."""

step = 5
"""Сдвиг строк"""

frames = []
"""Массив кадров"""

start_pos_y = height - font_size - font_size // 16
"""Нижняя позиция."""

end_pos = start_pos_y - diff_pos_y * (len(name_list) - 1)
"""Верхняя позиция.

В неё переносится текст после выхода за нижнюю часть экрана."""

for i, item in enumerate(name_list):
    item.coords[1] = start_pos_y - diff_pos_y * i

percentile = diff_pos_y // step
"""Вычисление количества шагов, необходимых для того, чтобы текст вышел за нижнюю границу картинки"""
print(percentile, diff_pos_y / step)

count_cycles = len(name_list) - 0
"""Количество прокруток.

По-умолчанию один полный круг (len(person_list) шагов)"""

count_iter = percentile * count_cycles
"""Количество кадров"""
print(count_iter)

im_base = Image.new('RGB', (width, height), color_background)
d_base = ImageDraw.Draw(im_base)
d_base.text((border, y_mid), "Спокойной ночи, ", fill=color_text, font=myFont)
d_base.text((start_pos_x + max_len_name, y_mid), " !", fill=color_text, font=myFont)

"""Заготовка заднего фона"""

# TODO: Это всё надо будет перенести


class Person:
    """

    :var name: Имя человека
    :type name: str
    :var color: Цвет текста для человека
    :type color: str | tuple[int, int, int] | tuple[int, int, int, int] | tuple[int, int, int, float]
    :var coords: Координаты текста. Считаются от левого верхнего угла картинки
    :type coords: list[float, float]

    """

    def __init__(self, name: str, color: str | list[int, int, int] | list[int, int, int, float] | list[
        int, int, int, int] = color_text) -> None:
        """

        :param name: Имя
        :param color: Цвет имени

        """
        self.name = name
        self.coords = [start_pos_x + (max_len_name - myFont.getlength(name)) / 2, 0]
        self.color = color

    def __str__(self) -> str:
        return f"Person(name={self.name}, color={self.color}, coords={self.coords})"

    def __repr__(self) -> str:
        return str(self)

    def draw(self, d: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont = myFont) -> None:
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
                                     list[int, int, int] |
                                     list[int, int, int, int]) |
                                    None):
    """
    Проверка на корректность цвета + его преобразование из float в int.
    :param color:
    :return: Цвет в корректной форме.
    :raises: TypeError

    """
    if isinstance(color, str):
        return color
        # TODO: Сделать проверку на корректность str цвета.
        #  Или же просто не говорить о возможности ввода цвета через str...
    elif isinstance(color, list):
        if isinstance(color[0], int) and isinstance(color[1], int) and isinstance(color[2], int):
            if len(color) == 3:
                return color
            elif len(color) == 4:
                if isinstance(color[3], int):
                    return color
                elif isinstance(color[3], float):
                    color[3] *= max_color_val
                    return color
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

    args = parser.parse_args()

    with open(args.config_path) as f:
        data = json.load(f)

    person_list: list[Person] = []
    """Список людей"""
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
    max_len_name = max([myFont.getlength(human[0]) for human in name_list])

    rgb_values = [tuple(int(layer * 255) for layer in color) for color in
                  sns.color_palette("magma", n_colors=count_colorless)]
    """Генерация RGB-значений для людей без указанного цвета"""

    people_list: list[Person] = []
    """Список людей"""

    iter = 0
    for human in name_list:
        if human[1] is None:
            human[1] = rgb_values[iter]
            iter += 1
        people_list.append(Person(human[0], human[1]))
    for person in people_list: print(person)

    if args.mode == 'v':
        pass
