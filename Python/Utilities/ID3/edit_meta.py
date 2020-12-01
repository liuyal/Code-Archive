import eyed3, time, sys, os


files = os.listdir(os.getcwd() + os.sep + "ost")


for item in files:

    number = int(item.split("_")[0])
    name = item.split("_")[-1].split(".")[0]

    audiofile = eyed3.load(os.getcwd() + os.sep + "ost" + os.sep + item)
    audiofile.tag.title  = name
    audiofile.tag.track_num  = number
    audiofile.tag.save()