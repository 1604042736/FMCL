import os
from PIL import Image


def main():
    path = '../Resources/Image/icon.png'
    try:
        os.makedirs(os.path.dirname(path))
    except:
        pass
    img = Image.new("RGB", (16, 16))
    # 画背景
    for i in range(16):
        for j in range(16):
            r = 255-i*16
            g = 255-j*16
            b = 255
            img.putpixel((i, j), (r, g, b))
    # 画 "F"
    color = (0, 0, 0)
    for i in range(4, 12):
        img.putpixel((i, 2), color)
    for i in range(3, 14):
        img.putpixel((4, i), color)
    for i in range(5, 12):
        img.putpixel((i, 7), color)
    img.save(path)


if __name__ == '__main__':
    main()
