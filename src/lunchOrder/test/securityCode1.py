#encoding=utf-8
from wheezy.captcha.image import captcha, background, text, warp, rotate, offset, curve, noise, smooth
from os import path
import random


_fontsDir='E:\selfwork\lunchOrder\src\lunchOrder\\test\\'
_letter_cases = "abcdefghjkmnpqrstuvwxy" # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper() # 大写字母
_numbers = ''.join(map(str, range(3, 10))) # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))

captcha_image_t = captcha(drawings=[
    background(),
    text(fonts=[
#         path.join(_fontsDir,'ae_AlArabiya.ttf'),
        path.join(_fontsDir,'FreeSans.ttf')],
        drawings=[
            warp(),
            rotate(),
            offset()
        ]),
    curve(),
    noise(),
    smooth()
])
chars_t = random.sample(init_chars, 4)
print chars_t

image_t = captcha_image_t(chars_t)
image_t.save('test.jpeg','jpeg',quality=75)