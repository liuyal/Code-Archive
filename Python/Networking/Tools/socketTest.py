from socket import *
import os, time, datetime

address = "0.0.0.0"
port = 5067

def recvall(sock):
    sock.settimeout(0.1)
    data = ""
    buf = ""
    t = time.time()

    while ((time.time() - t) < 1):
        try:
            buf, addr = sock.recvfrom(1024)
            t = time.time()
            data += buf
        except:
            pass
    return data

sock = socket(AF_INET, SOCK_DGRAM)
binder = sock.bind((address,port))

print(datetime.datetime.now())

t = time.time()
while ((time.time() - t) < 200):

    buf = recvall(sock)

    print(datetime.datetime.now())

    if buf:
       print(buf)
       t = time.time()
    # time.sleep(1)


print("END")