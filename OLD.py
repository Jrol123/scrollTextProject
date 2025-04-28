from PIL import Image, ImageDraw, ImageFont, ImageOps

save_image = False
"""Сохранить кадры"""

color_text = (0, 0, 0)
"""Цвет текста"""

color_background = (250, 250, 250)
"""Цвет фона"""

height = 1200
width = (height * 16) // 9

font_size = 160

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

name_list = [Person('Артём', (255, 166, 48)), Person('Влад', (130, 232, 186)),
             Person('Сашак', (77, 161, 169)), Person('Алиса', (46, 80, 119)),
             Person('Серёжа', (97, 28, 53)), Person('Аля', (255, 111, 89)),
             Person("Даниил", (37, 68, 65)), Person("Денис", (67, 170, 139)),
             Person("Саша", (178, 176, 255)), Person("Дина", (239, 48, 84))]
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

# txt = Image.new('L', (width, height))
# d = ImageDraw.Draw(txt)
# d.text((0, 0), "Someplace Near Boulder", font=myFont, fill=255)
# w = txt.rotate(17.5, expand=1)

im_base = Image.new('RGB', (width, height), color_background)
d_base = ImageDraw.Draw(im_base)
d_base.text((border, y_mid), "Спокойной ночи, ", fill=color_text, font=myFont)
d_base.text((start_pos_x + max_len_name, y_mid), " !", fill=color_text, font=myFont)

# im_base.paste(ImageOps.colorize(w, (0, 0, 0), (255, 255, 84)), mask=w)

im_base.save('img.png')

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

    if save_image:
        im.save(f'img/r{i}.png')

    # TODO: https://stackoverflow.com/questions/245447/how-do-i-draw-text-at-an-angle-using-pythons-pil

frames[0].save(
    'gif.gif',
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=30,
    loop=0
)
