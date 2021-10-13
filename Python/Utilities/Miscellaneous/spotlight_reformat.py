import os
import sys
import time
import cv2
import shutil
import datetime

src = r"C:\Users\Jerry\Desktop\old_images"
dst = r"C:\Users\Jerry\Desktop\new_images"

for folder in os.listdir(src):
    for image in os.listdir(src + os.sep + folder):

        time_stamp_year = folder[0:4]
        time_stamp_month = folder[4:6]
        time_stamp_day = folder[6:9]

        if not os.path.exists(dst + os.sep + time_stamp_year):
            os.makedirs(dst + os.sep + time_stamp_year)
        if not os.path.exists(dst + os.sep + time_stamp_year + os.sep + time_stamp_month):
            os.makedirs(dst + os.sep + time_stamp_year + os.sep + time_stamp_month)
        if not os.path.exists(dst + os.sep + time_stamp_year + os.sep + time_stamp_month + os.sep + time_stamp_day):
            os.makedirs(dst + os.sep + time_stamp_year + os.sep + time_stamp_month + os.sep + time_stamp_day)

        src_image = src + os.sep + folder + os.sep + image

        if "_pi" in image:
            dst_image = dst + os.sep + time_stamp_year + os.sep + time_stamp_month + os.sep + time_stamp_day + os.sep + image.replace("_pi", "_p")
        else:
            dst_image = dst + os.sep + time_stamp_year + os.sep + time_stamp_month + os.sep + time_stamp_day + os.sep + image

        shutil.copy(src_image, dst_image)



