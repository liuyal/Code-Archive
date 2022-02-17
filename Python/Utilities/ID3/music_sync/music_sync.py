import os
import eyed3
import shutil
from tinytag import TinyTag
from ytmusicapi import YTMusic


def copy_files(desktop_folder):
    if os.path.exists(desktop_folder):
        shutil.rmtree(desktop_folder)
    os.mkdir(desktop_folder)

    diff = set(local_album.keys()) - set(yt_albums.keys())
    for item in diff:
        album = local_album[item]
        for song in album:
            path = song[1].split(os.sep)
            path[0] = 'C:'
            path[1] = 'Users' + os.sep + 'Jerry' + os.sep + 'Desktop'
            path.insert(2, 'music')
            if len(path) == 5:
                if not os.path.exists(os.sep.join(path[:-1])):
                    os.mkdir(os.sep.join(path[:-1]))
            else:
                if not os.path.exists(os.sep.join(path[:-2])):
                    os.mkdir(os.sep.join(path[:-2]))
                if not os.path.exists(os.sep.join(path[:-1])):
                    os.mkdir(os.sep.join(path[:-1]))

            shutil.copy(song[1], os.sep.join(path))

            print(song[0], song[1])
            print(path)

if __name__ == "__main__":

    f = open('headers_auth_raw.txt', 'r+')
    f_raw = f.read()
    f.close()

    YTMusic.setup(filepath='headers_auth.json', headers_raw=f_raw)
    ytmusic = YTMusic('headers_auth.json')

    yt_songs = ytmusic.get_library_upload_songs(limit=9999, order='a_to_z')
    yt_albums = {}
    for song in yt_songs:
        title = song['title']
        album = song['album']['name']
        id = song['entityId']
        if album not in yt_albums.keys(): yt_albums[album] = []
        yt_albums[album].append((title, id))

    local_album = {}
    eyed3.log.setLevel("ERROR")
    for dirpath, dirnames, filenames in os.walk(r"E:\Music"):
        for filename in filenames:
            if '.mp3' in filename[-4:]:
                audiofile = eyed3.load(dirpath + os.sep + filename)
                title = audiofile.tag.title
                album = audiofile.tag.album
                if album not in local_album.keys(): local_album[album] = []
                local_album[album].append((title, dirpath + os.sep + filename))
            if '.flac' in filename[-5:]:
                audiofile = TinyTag.get(dirpath + os.sep + filename)
                title = audiofile.title
                album = audiofile.album
                if album not in local_album.keys(): local_album[album] = []
                local_album[album].append((title, dirpath + os.sep + filename))

    for item in yt_albums.keys():
        if len(yt_albums[item]) != len(local_album[item]):
            print('youtube\t', item, len(yt_albums[item]))
            print('local\t', item, len(local_album[item]))

    print('\nyoutube\t', len(yt_albums))
    print('local\t', len(local_album), '\n')

