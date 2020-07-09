import os, sys, time
import colour
import colorsys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def generate_hue():
    colors = []
    for hue in range(360):
        for sat in range(100):
            # Convert color from HSV to RGB
            rgb = colorsys.hsv_to_rgb(hue / 360, sat / 100, 1)
            rgb = [int(0.5 + 255 * u) for u in rgb]
            colors.extend(rgb)

    colors = bytes(colors)
    img = Image.frombytes('RGB', (100, 360), colors)
    img.save('hues.png')
    img.show()


def generate_gradient():
    colors = list(colour.Color("red").range_to(colour.Color("white"), 100))
    colors.pop(0)
    colors.pop(-1)

    palette = []
    for item in colors:
        r = int(item.get_red() * 255.0)
        g = int(item.get_green() * 255.0)
        b = int(item.get_blue() * 255.0)
        palette.append((r, g, b))


    palette = np.array(palette)[np.newaxis, :, :]
    plt.imshow(palette)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    generate_hue()
    generate_gradient()
