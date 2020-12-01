import time, os, sys
import shutil
import moviepy.editor as mp


path = os.getcwd() + os.sep + "0_Video"

files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.mp4' in file or '.webm' in file:
            files.append(os.path.join(r, file))

for item in files:

    try:
        name = item.split("\\")[-1].split('.')[0]
        clip = mp.VideoFileClip(item)
        clip.audio.write_audiofile(os.getcwd() + os.sep + "Output" + os.sep + name + ".mp3")
    except:
        time.sleep(1)
        print("Failed on " + name)
