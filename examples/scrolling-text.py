# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

import ILI9163


MESSAGE = "AE-ATM0177B3Aは秋月電子通商で買えるSPI接続の128x160ディスプレイモジュールです。ドライバはILI9163でST7735とほぼ同じです。"

# Create ILI9163 LCD display class.
disp = ILI9163.ILI9163(
    port=0,
    cs=0,
    dc=12,
    rst=25,
    rotation=90,
    width=128,
    height=160,
    spi_speed_hz=40000000
)

# Initialize display.
disp.begin()

WIDTH = disp.width
HEIGHT = disp.height


img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))

draw = ImageDraw.Draw(img)

font = ImageFont.truetype("/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf", 24)

size_x, size_y = draw.textsize(MESSAGE, font)

text_x = 160
text_y = (120 - size_y) // 2

t_start = time.time()

while True:
    x = (time.time() - t_start) * 100
    x %= (size_x + 160)
    draw.rectangle((0, 0, 160, 80), (0, 0, 0))
    draw.text((int(text_x - x), text_y), MESSAGE, font=font, fill=(255, 255, 0))
    disp.display(img)
