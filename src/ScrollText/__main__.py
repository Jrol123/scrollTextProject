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

border = 10
"""Отступ от левой стенки"""
# TODO: Сделать задаваемый отступ
start_pos_x = myFont.getlength('Спокойной ночи, ') + border
"""Стартовая позиция для написания имени"""

max_len_name = myFont.getlength('Даниил')
"""Длина самого длинного имени"""


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
    name_list: list[tuple[str, str | list[int, int, int] | list[int, int, int, float] | list[int, int, int, int]]] = []

    for human_name in data['people']:
        color = data['people'][human_name]
        if color == "" or color == []:
            count_colorless += 1
            color = None
        color = is_valid_color(color)
        name_list.append((human_name.encode("windows-1251").decode("utf-8"), color))

    rgb_values = [tuple(int(layer * 255) for layer in color) for color in
                  sns.color_palette("magma", n_colors=count_colorless)]
    """Генерация RGB-значений для людей без указанного цвета"""

    people_list: list[Person] = []
    """Список людей"""

    iter = 0
    for human in name_list:
        if human[1] == "":
            human[1] = rgb_values[iter]
            iter += 1
        people_list.append(Person(human[0], human[1]))
    for person in people_list: print(person)


