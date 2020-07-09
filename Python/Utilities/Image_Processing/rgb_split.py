import binascii, sys, os, time
from PIL import Image
import numpy as np

output_path = os.getcwd() + os.sep + "output"
if not os.path.exists(output_path): os.makedirs(output_path)

image_file = "lenna.png"
image = Image.open(os.getcwd() + os.sep + "input" + os.sep + image_file)
data = np.asarray(image)

red = np.zeros((image.size[1], image.size[0], 3), dtype=np.uint8)
red[:, :, 0] = data[:, :, 0]
green = np.zeros((image.size[1], image.size[0], 3), dtype=np.uint8)
green[:, :, 1] = data[:, :, 1]
blue = np.zeros((image.size[1], image.size[0], 3), dtype=np.uint8)
blue[:, :, 2] = data[:, :, 2]

Image.fromarray(red).save(output_path + os.sep + image_file.split(".")[0] + "_" + "red.png")
Image.fromarray(green).save(output_path + os.sep + image_file.split(".")[0] + "_" + "green.png")
Image.fromarray(blue).save(output_path + os.sep + image_file.split(".")[0] + "_" + "blue.png")

