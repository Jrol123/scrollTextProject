from PIL import Image, ImageDraw, ImageFont

color = (0, 0, 0)

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

y_mid = height // 2 - font_size // 2

step = 5

# print((y_mid + font_size) / step)
half_rot = (y_mid + font_size) / step
frames = []

start_pos = y_mid + 3 * diff_pos_y

end_pos = start_pos - diff_pos_y * (len(name_list) - 1)

for i, item in enumerate(name_list):
    item[1][1] = start_pos - diff_pos_y * i
    # print(item)

percentile = diff_pos_y // step
print(percentile, diff_pos_y / step)

count_iter = percentile * (len(name_list) - 9)  # 340
print(count_iter)

for i in range(count_iter):
    print(i)
    im = Image.new('RGB', (width, height), 'white')
    d1 = ImageDraw.Draw(im)
    d1.text((10, y_mid), "Спокойной ночи, ", fill=color, font=myFont)
    d1.text((koef * (16 + 7.5), y_mid), "!", fill=color, font=myFont)

    # d1.text((0, 0), f"{i}", fill=color, font=myFont)

    for name in name_list:
        # print(name)
        d1.text(name[1], name[0], fill=color, font=myFont)

    if i % percentile == 0:
        name_list[(i // percentile) - 1][1][1] = end_pos

        # d1.text((koef * (16 + d_name[0][1]), y_mid + 3 * diff_pos_y), d_name[7][0], fill=(0, 0, 0), font=myFont)

    frames.append(im)

    for name in name_list:
        name[1][1] += step

    im.save(f'img/r{i}.png')
    # https://stackoverflow.com/questions/245447/how-do-i-draw-text-at-an-angle-using-pythons-pil

frames[0].save(
    'gif.gif',
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=30,
    loop=0
)
