from PIL import Image, ImageDraw, ImageFont

color = (0, 0, 0)
"""Цвет текста"""

height = 1200
width = (height * 16) // 9

font_size = 160

myFont = ImageFont.truetype(r"C:\Users\artem\AppData\Local\Microsoft\Windows\Fonts\Rubik-Regular.ttf", font_size)

koef = 85  # TODO: Сделать авто-скалирующийся коэффициент
"""Коэффициент ширины. Подобран вручную.

Можно сделать массив с буквами и отношением высоты к ширине, и затем всё отмерять, но...

+ на всё это влияет шрифт...

Переделать ширину под выделяемое пространство на наиболее длинное имя через getlength"""

print(myFont.getlength('Даниил') + 20 * 2)

name_list = [['Артём', [koef * (16 + 0.25), 0]], ['Аля', [koef * (16 + 0.25), 0]],
             ["Алиса", [koef * (16 + 0.25), 0]], ["Сашак", [koef * (16 + 0.25), 0]],
             ["Серёжа", [koef * (16 + 0.25), 0]], ["Влад", [koef * (16 + 0.25), 0]],
             ["Даниил", [koef * (16 + 0.25), 0]], ["Денис", [koef * (16 + 0.25), 0]],
             ["Саша", [koef * (16 + 0.25), 0]], ["Дина", [koef * (16 + 0.25), 0]]]
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
    item[1][1] = start_pos - diff_pos_y * i

percentile = diff_pos_y // step
"""Вычисление количества шагов, необходимых для того, чтобы текст вышел за нижнюю границу картинки"""
print(percentile, diff_pos_y / step)

count_cycles = len(name_list) - 0
"""Количество прокруток.

По-умолчанию один полный круг (len(name_list) шагов)"""

count_iter = percentile * count_cycles
"""Количество кадров"""
print(count_iter)

for i in range(count_iter):
    print(i)
    im = Image.new('RGB', (width, height), 'white')
    d1 = ImageDraw.Draw(im)
    d1.text((10, y_mid), "Спокойной ночи, ", fill=color, font=myFont)
    d1.text((koef * (16 + 7.5), y_mid), "!", fill=color, font=myFont)

    for name in name_list:
        d1.text(name[1], name[0], fill=color, font=myFont)

    if i % percentile == 0:
        name_list[(i // percentile) - 1][1][1] = end_pos

    frames.append(im)

    for name in name_list:
        name[1][1] += step

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
