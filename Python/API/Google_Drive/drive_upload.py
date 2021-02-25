import os
import sys
import time
import json
import requests
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

if __name__ == "__main__":

    file = os.getcwd() + os.sep + 'ip.txt'
    folder_id = '18Jmqqe6PU0RWjeUiXcFbRgfErqcEE7Ad'
    time_stamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    ip = requests.get('https://api.ipify.org').text
    data = time_stamp + "\n\nPublic IP: " + ip + '\n'

    auth = GoogleAuth()
    auth.LoadCredentialsFile("Credentials.token")
    if auth.credentials == None:
        auth.LocalWebserverAuth()
    elif auth.access_token_expired:
        auth.Refresh()
    else:
        auth.Authorize()
    auth.SaveCredentialsFile("Credentials.token")

    drive = GoogleDrive(auth)

    file_list = drive.ListFile({'q': "'" + folder_id + "' in parents and trashed=false"}).GetList()

    if len(file_list) != 0:
        print("Updating IP File...")
        file = file_list[0]
        file.SetContentString(data)
        file.Upload()
        print('Title: %s\nID: %s' % (file['title'], file['id']))
    else:
        print("Creating IP File...")
        file = drive.CreateFile({'title': 'ip.txt', 'parents': [{'id': folder_id}]})
        file.SetContentString(data)
        file.Upload()
        print('Title: %s\nID: %s' % (file['title'], file['id']))

    print('\n' + data)