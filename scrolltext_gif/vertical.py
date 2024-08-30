import os
from PIL import ImageDraw

def draw_vertical(im_base, person_list, count_iter, percentile, end_pos, step, font, output_name, save_frame):
    print(f"Будет сгенерировано {count_iter} кадров \n")
    frames = []
    """Массив кадров"""

    if not os.path.exists('frames') and save_frame:
        os.mkdir('frames')

    for i in range(count_iter):
        print(i)

        im = im_base.copy()
        d1 = ImageDraw.Draw(im)

        for name in person_list:
            name.draw(d1, font)

        if i % percentile == 0:
            person_list[(i // percentile) - 1].coords[1] = end_pos

        frames.append(im)

        for name in person_list:
            name.coords[1] += step

        if save_frame:
            im.save(f'frames/f{i}.png')
        # ! DEBUG

    print("\nКадры сгенерированы.\nИдёт сохранение...")

    frames[0].save(
        output_name  + '.gif',
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=30,
        loop=0
    )

    print("\nГотово!")
