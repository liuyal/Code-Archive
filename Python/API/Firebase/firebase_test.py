import datetime, time, os, sys
from firebase import firebase

# https://ozgur.github.io/python-firebase/
# https://stackoverflow.com/questions/52133031/receiving-async-error-when-trying-to-import-the-firebase-package
# https://firebase.google.com/docs/database/admin/save-data#python

def Firebase_wipe_database(url, firebase_handler):
    firebase = firebase_handler.FirebaseApplication(url, None)
    firebase.put('','/', None)

def Firebase_put(url, firebase_handler, username, password, uuid):
    firebase = firebase_handler.FirebaseApplication(url, None)
    firebase.put('', '/users/'+ uuid +'/username', username)
    firebase.put('', '/users/'+ uuid +'/password', password)

if __name__ == "__main__":

    url = ''

    username = 'jerry'
    password = 'newwdfasdfdsfgaorld'
    uuid = 'A7ZE71AH5'

    Firebase_wipe_database(url, firebase)
    Firebase_put(url, firebase, '', '', uuid)
    Firebase_put(url, firebase, username, password, uuid)

    print("EOT")
