from PIL import Image, ImageDraw, ImageFont

color_text = (0, 0, 0)
"""Цвет текста"""

color_background = (255, 255, 255)
"""Цвет фона"""

height = 1200
width = (height * 16) // 9

font_size = 160

myFont = ImageFont.truetype(r"C:\Users\artem\AppData\Local\Microsoft\Windows\Fonts\Rubik-Regular.ttf", font_size)


class Person:
    """

    :var name: Имя человека
    :var color: Цвет текста для человека
    :var coords: Координаты текста. Считаются от левого верхнего угла картинки

    """

    def __init__(self, name: str, x_coord: float, color: str | tuple[int, int, int] = color_text) -> None:
        """

        :param name: Имя
        :param x_coord: Координата по OX
        :param color: Цвет имени

        """
        self.name = name
        self.coords = [x_coord, 0]
        self.color = color

    def draw(self, d: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont = myFont) -> None:
        """
        Рисование имени человека на нужном холсте

        :param d: Рисовальщик
        :param font: Шрифт текста

        :returns: Отрисовывает имя человека

        """
        d.text(self.coords, self.name, fill=self.color, font=font)


koef = 85  # TODO: Сделать авто-скалирующийся коэффициент
"""Коэффициент ширины. Подобран вручную.

Можно сделать массив с буквами и отношением высоты к ширине, и затем всё отмерять, но...

+ на всё это влияет шрифт...

Переделать ширину под выделяемое пространство на наиболее длинное имя через getlength"""

print(myFont.getlength('Даниил') + 20 * 2)

name_list = [Person('Артём', koef * (16 + 0.25)), Person('Влад', koef * (16 + 0.25)),
             Person('Сашак', koef * (16 + 0.25)), Person('Алиса', koef * (16 + 0.25)),
             Person('Серёжа', koef * (16 + 0.25)), Person('Аля', koef * (16 + 0.25)),
             Person("Даниил", koef * (16 + 0.25)), Person("Денис", koef * (16 + 0.25)),
             Person("Саша", koef * (16 + 0.25)), Person("Дина", koef * (16 + 0.25))]
"""Список имён с положением на экране формата (x, y).

Коэффициент 0.25 стоит изменить, если нужно центрирование"""

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

start_pos = height - font_size - font_size // 16
"""Нижняя позиция."""

print(start_pos, y_mid + 3 * diff_pos_y)

end_pos = start_pos - diff_pos_y * (len(name_list) - 1)
"""Верхняя позиция.

В неё переносится текст после выхода за нижнюю часть экрана."""

for i, item in enumerate(name_list):
    item.coords[1] = start_pos - diff_pos_y * i

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
d_base.text((10, y_mid), "Спокойной ночи, ", fill=color_text, font=myFont)
d_base.text((koef * (16 + 7.5), y_mid), "!", fill=color_text, font=myFont)

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

    im.save(f'img/r{i}.png')
    # TODO: https://stackoverflow.com/questions/245447/how-do-i-draw-text-at-an-angle-using-pythons-pil

frames[0].save(
    'gif.gif',
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=25,
    loop=0
)
