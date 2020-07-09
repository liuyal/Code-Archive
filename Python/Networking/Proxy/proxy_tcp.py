import os
import sys
import socket
from threading import Thread

test_area = "Security"
test_sub_area = ""

inmotionautomation_home_dirname = os.environ['INMOTIONAUTOMATION_HOME']
sys.path.append(inmotionautomation_home_dirname+"/lib/common")

import basic_inmotion as bm
import proxy_airlink


def TCP_LAN_listener_singlePort(remote_lan_proxy_connect,bindIP, portNum):
    bm.cslog("Create TCP listener socket", "BLUE")
    remote_LAN_sock_ins = remote_lan_proxy_connect.modules.socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_LAN_sock_ins.bind((bindIP, portNum))
    remote_LAN_sock_ins.listen(5)
    remote_LAN_sock_ins.settimeout(20)
    connect, addr = remote_LAN_sock_ins.accept()
    connect.setblocking(1)
    bm.cslog("Listener accepted connection from sender", "BLUE")
    data = connect.recv(1024)
    if data == "Hello":
        bm.cslog("Listener received data from sender: " + data, "BLUE")
    connect.send(data)
    bm.cslog("Listener sent data back", "BLUE")
    connect.close()
    remote_LAN_sock_ins.close()
    bm.cslog("Terminate the connection and close listener socket", "BLUE")

def TCP_WAN_sender_singlePort(remote_wan_proxy_connect,connectIP, portNum):
    bm.cslog("Create TCP sender socket", "YELLOW")
    remote_WAN_sock_ins = remote_wan_proxy_connect.modules.socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    remote_WAN_sock_ins.connect((connectIP, portNum))
    bm.cslog("Sender connected to the listener", "YELLOW")
    remote_WAN_sock_ins.send("Hello")
    bm.cslog("Sender sent message to listener", "YELLOW")
    data = remote_WAN_sock_ins.recv(1024)
    if (data == "Hello"):
        bm.cslog("Sender received message from listener: " + data, "YELLOW")
    remote_WAN_sock_ins.close()
    bm.cslog("Close sender socket", "YELLOW")

def Establish_WAN_TO_LAN_TCP_connection_singlePort(remote_wan_proxy_connect, remote_lan_proxy_connect, bindIP, connectIP, portNum):
    try:
        listener = Thread(target=TCP_LAN_listener_singlePort, args=[remote_lan_proxy_connect, bindIP, portNum])
        listener.start()
        sender = Thread(target=TCP_WAN_sender_singlePort, args=[remote_wan_proxy_connect, connectIP, portNum])
        sender.start()
        listener.join()
        sender.join()
    except:
        remote_lan_proxy_connect.close()
        remote_wan_proxy_connect.close()
        print("\nFail")

bindIP = "172.22.0.101"
connectIP = "68.182.37.72"
public_ip = "208.81.123.36"
proxy_lan_ip = "192.168.100.1"
proxy_wan_ip = "192.168.100.3"
portNum = 15424

proxy_hostWan = proxy_airlink.ProxyAirlink(proxy_wan_ip)
proxy_hostLan = proxy_airlink.ProxyAirlink(proxy_lan_ip)
remote_wan_proxy_connect = proxy_hostWan.connect()
remote_lan_proxy_connect = proxy_hostLan.connect()

try:
    Establish_WAN_TO_LAN_TCP_connection_singlePort(remote_wan_proxy_connect, remote_lan_proxy_connect, bindIP, connectIP, portNum)
except:
    remote_lan_proxy_connect.close()
    remote_wan_proxy_connect.close()
    print("\nFail")

