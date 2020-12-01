import time
import sys
import os
import eyed3
import pandas as pd


def read_tags(path):
    w_file = open(os.getcwd() + os.sep + "genre.csv", "a+")
    w_file.truncate(0)
    w_file.write("Artist,Album,Genre\n")
    for folder in os.listdir(path):
        if " - " in folder:
            artist = folder.split(" - ")[0].replace(',', '')
            album = folder.split(" - ")[1].replace(',', '')
            genre_list = []
            try:
                for dirpath, dirnames, filenames in os.walk(path + os.sep + folder):
                    for filename in filenames:
                        if "mp3" in filename:
                            audiofile = eyed3.load(dirpath + os.sep + filename)
                            genre_list.append(audiofile.tag.genre.name)
                            print('\t' + filename + '\t' + audiofile.tag.genre.name)
                genre_list = list(dict.fromkeys(genre_list))
                w_file.write(artist + "," + album + "," + ';'.join(genre_list) + "\n")
                w_file.flush()
                print(folder)
                print(genre_list)
            except Exception as E:
                print(E)

    w_file.close()


def set_tags(path, tag_sheet):
    music_data = {}

    df = pd.read_excel(tag_sheet)
    for index, row in df.iterrows():
        if row["Artist"] not in music_data.keys():
            music_data[row["Artist"]] = {}
        music_data[row["Artist"]][row["Album"]] = row["Genre"]

    for folder in os.listdir(path):
        if " - " in folder:
            artist = folder.split(" - ")[0].replace(',', '')
            album = folder.split(" - ")[1].replace(',', '')
            try:
                for dirpath, dirnames, filenames in os.walk(path + os.sep + folder):
                    for filename in filenames:
                        if "mp3" in filename:
                            genre = music_data[artist][album]
                            audiofile = eyed3.load(dirpath + os.sep + filename)
                            audiofile.tag.genre.name = genre
                            audiofile.tag.save(dirpath + os.sep + filename)

            except Exception as E:
                print(E)


if __name__ == "__main__":
    # eyed3.log.setLevel("ERROR")
    music_path = r"E:\Music"

    read_tags(music_path)
    set_tags(music_path, "new_genre.xlsx")
