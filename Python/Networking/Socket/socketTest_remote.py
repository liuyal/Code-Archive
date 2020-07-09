import datetime
import socket
import sys, os
import time

inmotionautomation_home_dirname = os.environ['INMOTIONAUTOMATION_HOME']
sys.path.append(inmotionautomation_home_dirname + "/lib/common")
sys.path.append(inmotionautomation_home_dirname + "/lib/site-packages")
sys.path.append(inmotionautomation_home_dirname + "/testsuite/inmotion/Feature/GPS")
sys.path.append(inmotionautomation_home_dirname + "/testsuite/inmotion/Feature/GPS/gps_lib")

import proxy_airlink

listener = "192.168.100.3"
address = "208.81.123.36"
port = 15415
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


proxy_host = proxy_airlink.ProxyAirlink(listener)
remote_proxy_connect = proxy_host.connect()
if not remote_proxy_connect:
    sys.exit("Could not connect Listener via Proxy!")
else:
    print("Listener Is Online.")


sock = remote_proxy_connect.modules.socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((address, port))

print(datetime.datetime.now())

t = time.time()
while ((time.time() - t) < 200):

    buf = recvall(sock)

    print(datetime.datetime.now())

    if buf:
        print(buf)
        t = time.time()
    # time.sleep(1)

sock.close()

print("END")
