import time, os, sys
import shutil
import moviepy.editor as mp


path = os.getcwd() + os.sep + "videos"

files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.mp4' in file or '.webm' in file:
            files.append(os.path.join(r, file))

number = 1

for item in files:

    type = item.split('.')[-1]
    name = item.split('_')[1].split('-')[0]
    file_name = str(number) + '_' + name[1:]
    src = item
    dst = os.getcwd() + os.sep + "Done" + os.sep + file_name + "." + type
    os.rename(src, dst)
    print(item)
    print(dst)

    number += 1