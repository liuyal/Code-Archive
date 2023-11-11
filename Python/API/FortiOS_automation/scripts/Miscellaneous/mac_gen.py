import os
import sys
import time
import socket
import struct


def ip_gen(start, end):
    start = struct.unpack('>I', socket.inet_aton(start))[0]
    end = struct.unpack('>I', socket.inet_aton(end))[0]
    return [socket.inet_ntoa(struct.pack('>I', i)) for i in range(start, end)]


if __name__ == "__main__":
    f = open("mac-ip.txt", "r+")
    txt_list = f.readlines()
    f.close()

    ips = ip_gen("192.168.1.1", "192.169.255.255")

    mac_ip_list = []

    for i in range(0, len(txt_list)):
        mac_ip_list.append(txt_list[i].split()[0] + ' ' + ips[i])

    f = open("mac-ip-output.txt", "w+")
    f.truncate(0)
    f.write('\n'.join(mac_ip_list))
    f.flush()
    f.close()