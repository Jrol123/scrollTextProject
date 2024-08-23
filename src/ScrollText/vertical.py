from PIL import Image, ImageDraw, ImageFont
import seaborn as sns

save_frame = False
# ! DEBUG

color_text = (0, 0, 0)
"""Цвет стандартного текста"""

color_background = (250, 250, 250)
"""Цвет фона"""

height = 1200
width = (height * 16) // 9
# TODO: Разобраться с пропорциями

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

    def __init__(self, name: str, color: str | tuple[int, int, int] = color_text) -> None:
        """

        :param name: Имя
        :param color: Цвет имени

        """
        self.name = name
        self.coords = [start_pos_x + (max_len_name - myFont.getlength(name)) / 2, 0]
        self.color = color

    def draw(self, d: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont = myFont) -> None:
        """
        Рисование имени человека на нужном холсте

        :param d: Рисовальщик
        :param font: Шрифт текста

        :returns: Отрисовывает имя человека

        """
        d.text(self.coords, self.name, fill=self.color, font=font)


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

print(start_pos_y, y_mid + 3 * diff_pos_y)

N = 10
RGB_tuples = sns.color_palette(None, N, as_cmap=True)
# TODO: Будет переработано при переходе к файловой системе

name_list = [Person('Артём', RGB_tuples[0]), Person('Влад', RGB_tuples[1]),
             Person('Сашак', RGB_tuples[2]), Person('Алиса', RGB_tuples[3]),
             Person('Серёжа', RGB_tuples[4]), Person('Аля', RGB_tuples[5]),
             Person("Даниил", RGB_tuples[6]), Person("Денис", RGB_tuples[7]),
             Person("Саша", RGB_tuples[8]), Person("Дина", RGB_tuples[9])]
"""Список людей"""

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

По-умолчанию один полный круг (len(name_list) шагов)"""

count_iter = percentile * count_cycles
"""Количество кадров"""
print(count_iter)

im_base = Image.new('RGB', (width, height), color_background)
d_base = ImageDraw.Draw(im_base)
d_base.text((border, y_mid), "Спокойной ночи, ", fill=color_text, font=myFont)
d_base.text((start_pos_x + max_len_name, y_mid), " !", fill=color_text, font=myFont)

"""Заготовка заднего фона"""

for i in range(count_iter):
    print(i)

    im = im_base.copy()
    d1 = ImageDraw.Draw(im)

    for name in name_list:
        name.draw(d1, myFont)

    if i % percentile == 0:
        name_list[(i // percentile) - 1].coords[1] = end_pos

    frames.append(im)

    for name in name_list:
        name.coords[1] += step

    if save_frame:
        im.save(f'img/f{i}.png')
    # ! DEBUG

frames[0].save(
    'gif.gif',
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=30,
    loop=0
)
