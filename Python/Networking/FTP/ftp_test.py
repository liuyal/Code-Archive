import sys, os, time, shutil, ftplib, threading, random
from ftplib import FTP


# default to /home
def FTP_upload(ip, port, usr, pwd, file):
    ftp = FTP(timeout=60)
    ftp.set_debuglevel(2)

    print("Connecting to: " + str(ip) + ':' + str(port))
    ftp.connect(ip, port)
    print("Login to: " + str(usr) + ':' + str(pwd))
    ftp.login(usr, pwd)

    localPath = file
    remotePath = 'STOR ' + ftp.pwd() + file.split(os.sep)[-1]
    ftp.storbinary(remotePath, open(localPath, 'rb'))
    ftp.voidcmd('NOOP')


if __name__ == "__main__":
    ip = "3.224.104.150"
    port = 14550
    usr = "bread"
    pwd = "123456"
    file = os.getcwd() + os.sep + "test.png"

    upload_results = FTP_upload(ip, port, usr, pwd, file)

    print("<EOT>")
    time.sleep(5)