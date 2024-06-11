from PIL import Image, ImageDraw, ImageFont

color = (0, 0, 0)

height = 1200
width = (height * 16) // 9

font_size = 160

myFont = ImageFont.truetype(r"C:\Users\artem\AppData\Local\Microsoft\Windows\Fonts\Rubik-Regular.ttf", font_size)

koef = 85  # TODO: Сделать скалирующийся коэффициент

name_list = [['Артём', [koef * (16 + 0.25), 0]], ['Аля', [koef * (16 + 0.25), 0]],
             ["Алиса", [koef * (16 + 0.25), 0]], ["Сашак", [koef * (16 + 0.25), 0]],
             ["Серёжа", [koef * (16 + 0.25), 0]], ["Влад", [koef * (16 + 0.25), 0]],
             ["Даниил", [koef * (16 + 0.25), 0]], ["Денис", [koef * (16 + 0.25), 0]],
             ["Саша", [koef * (16 + 0.25), 0]], ["Дина", [koef * (16 + 0.25), 0]]]

diff_pos_y = font_size + font_size // 16

y_mid = height // 2 - font_size // 2

step = 5

# print((y_mid + font_size) / step)
half_rot = (y_mid + font_size) / step
frames = []

start_pos = y_mid + 3 * diff_pos_y

d_name = list(name_list)
# d_name += list(name_list)

for i, item in enumerate(d_name):
    item[1][1] = start_pos - diff_pos_y * i
    # print(item)

# print(d_name, len(d_name))

# + 3 из-за длинных букв
# (y_mid + font_size) // step + 3
for i in range(30):
    print(i)
    im = Image.new('RGB', (width, height), 'white')
    d1 = ImageDraw.Draw(im)
    d1.text((10, y_mid), "Спокойной ночи, ", fill=color, font=myFont)
    d1.text((koef * (16 + 7.5), y_mid), "!", fill=color, font=myFont)
    d1.text((0, 0), f"{i}", fill=color, font=myFont)

    for name in d_name:
        # print(name)
        d1.text(name[1], name[0], fill=color, font=myFont)

    # d1.text((koef * (16 + d_name[0][1]), y_mid + 3 * diff_pos_y), d_name[7][0], fill=(0, 0, 0), font=myFont)

    frames.append(im)

    for name in d_name:
        name[1][1] += step

    im.save(f'img/r{i}.png')
    # https://stackoverflow.com/questions/245447/how-do-i-draw-text-at-an-angle-using-pythons-pil

frames[0].save(
    'gif.gif',
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=40,
    loop=0
)

# d1.text((koef * (16 + [koef * (16 + 0.25), 0]), y_mid), name_list[0], fill=(0, 0, 0), font=myFont)
# d1.text((koef * (16 + [koef * (16 + 0.25), 0]), y_mid - 1 * diff_pos_y), name_list[1], fill=(0, 0, 0), font=myFont)
# d1.text((koef * (16 + [koef * (16 + 0.25), 0]), y_mid - 2 * diff_pos_y), name_list[2], fill=(0, 0, 0), font=myFont)
# d1.text((koef * (16 + [koef * (16 + 0.25), 0]), y_mid - 3 * diff_pos_y), name_list[3], fill=(0, 0, 0), font=myFont)
# d1.text((koef * (16 + [koef * (16 + 0.25), 0]), y_mid - 4 * diff_pos_y), name_list[4], fill=(0, 0, 0), font=myFont)
# d1.text((koef * (16 + [koef * (16 + 0.25), 0]), y_mid + 1 * diff_pos_y), name_list[5], fill=(0, 0, 0), font=myFont)
# d1.text((koef * (16 + [koef * (16 + 0.25), 0]), y_mid + 2 * diff_pos_y), name_list[6], fill=(0, 0, 0), font=myFont)
# d1.text((koef * (16 + [koef * (16 + 0.25), 0]), y_mid + 3 * diff_pos_y), name_list[7], fill=(0, 0, 0), font=myFont)
# # d1.text((koef * (16 + [koef * (16 + 0.25), 0]), y_mid + 4 * diff_pos_y), name_list[8], fill=(0, 0, 0), font=myFont)

# Отображает одновременно 8 имён (верхушка тоже считается

# print(len(name_list))
# d1.text((koef * 16, y_mid + diff_pos_y), "", fill=(0, 0, 0), font=myFont)
