from PIL import ImageDraw, ImageFont
import json
import argparse as prs
import seaborn as sns

color_text = (0, 0, 0)
"""Цвет стандартного текста"""

font_size = 160
# TODO: Переделать под размеры экрана и пропорции
myFont = ImageFont.truetype(r"C:\Users\artem\AppData\Local\Microsoft\Windows\Fonts\Rubik-Regular.ttf", font_size)

border = 10
"""Отступ от левой стенки"""
start_pos_x = myFont.getlength('Спокойной ночи, ') + border
"""Стартовая позиция для написания имени"""

max_len_name = myFont.getlength('Даниил')
"""Длина самого длинного имени"""


class Person:
    """

    :var name: Имя человека
    :type name: str
    :var color: Цвет текста для человека
    :type color: str | tuple[int, int, int]
    :var coords: Координаты текста. Считаются от левого верхнего угла картинки
    :type coords: list[float, float]

    """

    def __init__(self, name: str, color: str | tuple[int, int, int] | tuple[int, int, int, float] | tuple[int, int, int, int] = color_text) -> None:
        """

        :param name: Имя
        :param color: Цвет имени

        """
        self.name = name
        self.coords = [start_pos_x + (max_len_name - myFont.getlength(name)) / 2, 0]
        self.color = color
        # TODO: Сделать проверку на корректность введённого цвета. ColorName, HEX или же RGB(A). Alpha может быть представлена как float (0-1), так и int(0-255), что тоже надо учесть

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
    for human_name in data['people']:
        color = data['people'][human_name]
        if color == "" or color == []:
            count_colorless += 1
        person_list.append(Person(human_name.encode("windows-1251").decode("utf-8"), color))

    rgb_values = [tuple(int(layer * 255) for layer in color) for color in sns.color_palette("magma", n_colors=count_colorless)]
    """Список RGB-значений для людей без указанного цвета"""
    print(rgb_values)
