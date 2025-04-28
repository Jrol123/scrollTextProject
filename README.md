# ScrollText project

Этот репозиторий посвящён генерации гифок с прокручивающимся списком имён.

## Пример использования

```json:example/example.json
{
  "people": {
    "Name1": [0, 0, 0],
    "Name2": "black",
    "Name3": [255, 0, 0, 255],
    "Name4": [245, 40, 145, 0.4],
    "Name5": "#00FF00",
    "Name6": ""
  },
  "height": 800,
  "width": 1920,
  "font_size": 150,
  "default_name_color": "",
  "color_main_text": "",
  "color_background": "",
  "first_part": "Спокойной ночи, ",
  "second_part": " !",
  "border": 10,
  "color_palette": "magma",
  "font": "Rubik-Regular.ttf",
  "save_frames": false
}


```

Результат:
![Example GIF](example/output.gif)

## Todo

Планируется реализовать версию с прокруткой списка по-кругу.

Также смотрите TODO в коде.
