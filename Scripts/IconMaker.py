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
    b = 0
    for i in range(16):
        for j in range(16):
            r = 255-i*16
            g = 255-j*16
            img.putpixel((i, j), (r, g, b))
            b += 1
    # 画 "F"
    color = (0, 0, 0)
    for i in range(4, 12):
        img.putpixel((i, 2), color)
        img.putpixel((i, 3), color)
    for i in range(3, 14):
        img.putpixel((4, i), color)
        img.putpixel((5, i), color)
    for i in range(5, 12):
        img.putpixel((i, 7), color)
        img.putpixel((i, 8), color)
    img.save(path)
    path = "../Resources/Icon/FMCL.ico"
    try:
        os.makedirs(os.path.dirname(path))
    except:
        pass
    img.save(path)


if __name__ == '__main__':
    main()
