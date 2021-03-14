import os
import sys
import time
import colour
import colorsys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

if __name__ == "__main__":

    image_file = "rna.png"
    image = Image.open(os.getcwd() + os.sep + "input" + os.sep + image_file)
    data = np.asarray(image)

    pix_values = list(image.getdata())
    pix_values.sort()

    im = Image.new('RGB', (image.width, image.height))
    im.putdata(pix_values)
    im.save(os.getcwd() + os.sep + "output" + os.sep + image_file.split('.')[0] + "_pixel_sorted.png")
