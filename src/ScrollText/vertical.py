from PIL import Image, ImageDraw, ImageFont
import seaborn as sns

save_frame = False
# ! DEBUG



print(start_pos_y, y_mid + 3 * diff_pos_y)

N = 10
RGB_tuples = sns.color_palette(None, N, as_cmap=True)
# TODO: Будет переработано при переходе к файловой системе

name_list = [Person('Артём', (245, 40, 140, 255)), Person('Влад', RGB_tuples[1]),
             Person('Сашак', RGB_tuples[2]), Person('Алиса', RGB_tuples[3]),
             Person('Серёжа', RGB_tuples[4]), Person('Аля', RGB_tuples[5]),
             Person("Даниил", RGB_tuples[6]), Person("Денис", RGB_tuples[7]),
             Person("Саша", RGB_tuples[8]), Person("Дина", RGB_tuples[9])]
"""Список людей"""



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
