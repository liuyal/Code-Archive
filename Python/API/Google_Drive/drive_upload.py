import os
import sys
import time
import json
import requests
import datetime
import socket
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

if __name__ == "__main__":

    path =  r'/home/wolf/Documents/Google_Drive'
    file = path + os.sep + 'ip.txt'
    time_stamp = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")
    ip = requests.get('https://api.ipify.org').text

    try: socket.inet_aton(ip)
    except socket.error: ip = "0.0.0.0"

    data = "[" + time_stamp + "] Public IP: " + ip

    auth = GoogleAuth()
    auth.LoadCredentialsFile(path + os.sep + "Credentials.token")
    if auth.credentials == None: auth.LocalWebserverAuth()
    elif auth.access_token_expired: auth.Refresh()
    else: auth.Authorize()
    auth.SaveCredentialsFile(path + os.sep + "Credentials.token")

    drive = GoogleDrive(auth)
    folder_id = '18Jmqqe6PU0RWjeUiXcFbRgfErqcEE7Ad'
    file_list = drive.ListFile({'q': "'" + folder_id + "' in parents and trashed=false"}).GetList()

    if len(file_list) != 0:
        print("Updating IP File...")
        file = file_list[0]
        text = file.GetContentString()
        file.SetContentString(text + "\n" + data)
        file.Upload()
        print(("Title",file['title']) + ("ID", file['id']))
    else:
        print("Creating IP File...")
        file = drive.CreateFile({'title': 'ip.txt', 'parents': [{'id': folder_id}]})
        file.SetContentString(data)
        file.Upload()
        print(("Title",file['title']) + ("ID", file['id']))

    print(data)