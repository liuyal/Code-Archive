import os
import time
import sys
import shutil
import datetime
import cv2


def get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp) and ".png" in fp:
                total_size += os.path.getsize(fp)

    return total_size


if __name__ == "__main__":

    src = r"C:\Users\USER\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
    src = src.replace("USER", os.getlogin())
    dst = r"E:\Picture\SpotLightSaver"

    time_stamp = datetime.datetime.now().strftime("%Y%m%d")
    if not os.path.exists(dst + os.sep + time_stamp):
        os.makedirs(dst + os.sep + time_stamp)
    for item in os.listdir(src):
        shutil.copy(src + os.sep + item, dst + os.sep + time_stamp + os.sep + item + ".png")

    # Check for duplicate images in different date folders
    images = []
    remove_list = {}
    for item in os.listdir(dst):
        if os.path.isdir(dst + os.sep + item) and ".git" not in item:
            for file in os.listdir(dst + os.sep + item):
                try:
                    remove_list[file]
                except:
                    remove_list[file] = []
                remove_list[file].append(dst + os.sep + item + os.sep + file)
                images.append(dst + os.sep + item + os.sep + file)
                print(dst + os.sep + item + os.sep + file)

    # Remove non duplicate images from list
    for key in list(remove_list):
        if len(remove_list[key]) == 1:
            del remove_list[key]

    # Reset count of each duplicate image to 1
    for key in list(remove_list):
        for i in range(0, len(remove_list[key]) - 1):
            remove_list[key].pop(i)

    # Remove Duplicate images from most recent date
    for key in list(remove_list):
        os.remove(remove_list[key][0])

    # Clean up empty folders
    for item in os.listdir(dst):
        if os.path.isdir(dst + os.sep + item) and len(os.listdir(dst + os.sep + item)) < 1:
            shutil.rmtree(dst + os.sep + item)

    # Remove non spotlight images
    for image in os.listdir(dst + os.sep + time_stamp):
        if ".png" in image:
            im = cv2.imread(dst + os.sep + time_stamp + os.sep + image)
            if im.shape[0] < 900:
                os.remove(dst + os.sep + time_stamp + os.sep + image)

    # Read count and size of images and write to readme
    size_gb = str(round(get_size(start_path=dst) / 1000 / 1000 / 1000, 3)) + " GB"
    print("\nImage Count: " + str(len(images)))
    print("Size: " + str(size_gb) + "\n")

    file = open(dst + os.sep + "README.md", "r+")
    text = file.readlines()
    file.close()

    for line in text:
        if "count:" in line.lower():
            text[text.index(line)] = "Image Count: " + str(len(images)) + "\n"
        if "size" in line.lower():
            text[text.index(line)] = "Size: " + size_gb + "\n"

    file = open(dst + os.sep + "README.md", "w+")
    file.truncate(0)
    file.write("".join(text))
    file.flush()
    file.close()

    # Commit images to github
    os.system(r"cd " + dst + " && python " + dst + r"\git_commit.py")
    time.sleep(5)
