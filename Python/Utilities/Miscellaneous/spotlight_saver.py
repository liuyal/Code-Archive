import os, time, sys, shutil, datetime


def get_size(start_path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp) and ".png" in fp:
                total_size += os.path.getsize(fp)

    return total_size


if __name__ == "__main__":
    src = r"C:\Users\Jerry\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"
    dst = r"E:\Picture\SpotLightSaver"

    time_stamp = datetime.datetime.now().strftime("%Y%m%d")
    if not os.path.exists(dst + os.sep + time_stamp): os.makedirs(dst + os.sep + time_stamp)
    for item in os.listdir(src): shutil.copy(src + os.sep + item, dst + os.sep + time_stamp + os.sep + item + ".png")

    images = []
    remove_list = {}
    for item in os.listdir(dst):
        if os.path.isdir(dst + os.sep + item):
            for file in os.listdir(dst + os.sep + item):
                try:
                    remove_list[file]
                except:
                    remove_list[file] = []
                remove_list[file].append(dst + os.sep + item + os.sep + file)
                images.append(dst + os.sep + item + os.sep + file)
                print(dst + os.sep + item + os.sep + file)

    for key in list(remove_list):
        if len(remove_list[key]) == 1: del remove_list[key]
    for key in list(remove_list):
        for i in range(0, len(remove_list[key]) - 1): remove_list[key].pop(i)
    for key in list(remove_list): os.remove(remove_list[key][0])
    for item in os.listdir(dst):
        if os.path.isdir(dst + os.sep + item) and len(os.listdir(dst + os.sep + item)) < 1: shutil.rmtree(dst + os.sep + item)

    size_gb = str(round(get_size(start_path=dst) / 1024 / 1024 / 1024, 3)) + " GB"
    print("Size:", size_gb)

    file = open(dst + os.sep + "README.md", "r+")
    text = file.readlines()
    file.close()

    for line in text:
        if "size" in line.lower():
            text[text.index(line)] = "Size: " + size_gb + "\n"

    file = open(dst + os.sep + "README.md", "w+")
    file.truncate(0)
    file.write("".join(text))
    file.flush()
    file.close()

    os.system(r"cd " + dst + " && python " + dst + r"\git_commit.py")
    time.sleep(5)
