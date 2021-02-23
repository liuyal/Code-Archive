import os
import sys
import time
import socket
import threading
import datetime


def tcp_listener(thread_id, TCP_IP="", TCP_PORT=9996, time_out=60):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen()
    connection, address = sock.accept()
    with connection:
        while True:
            data = connection.recv(1024)
            if not data: break
            time_stamp = str(datetime.datetime.now().strftime("%H:%M:%S"))
            sys.stdout.write("[" + str(thread_id) + "] " + time_stamp + str(address) + " : " + str(data.decode('utf-8')) + "\n")


def tcp_sender(thread_id, TCP_IP="127.0.0.1", TCP_PORT=9996, time_out=60):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    version = sys.version_info
    for i in range(0, 500):
        MESSAGE = str(i)
        if version.major == 3:
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
            sock.sendall(MESSAGE.encode())
        else:
            sock.sendall(MESSAGE)
        time.sleep(1)


def udp_listener(thread_id, UDP_IP="0.0.0.0", UDP_PORT=9996, time_out=60):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(time_out)
    sock.bind((UDP_IP, UDP_PORT))
    try:
        while True:
            data, address = sock.recvfrom(1024)
            time_stamp = str(datetime.datetime.now().strftime("%H:%M:%S"))
            sys.stdout.write("[" + str(thread_id) + "] " + time_stamp + str(address) + " : " + str(data.decode('utf-8')) + "\n")
    except socket.timeout:
        sock.close()


def udp_sender(thread_id, UDP_IP="0.0.0.0", UDP_PORT=9996, time_out=60):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    version = sys.version_info
    for i in range(0, 500):
        MESSAGE = str(i)
        if version.major ==3:
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
        else:
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

        time.sleep(1)

if __name__ == "__main__":

    try:
        sys.argv[1]
    except:
        print("Arg: -l, -s")

    N = 100
    thread_list = []

    for i in range(0, N):

        if sys.argv[1] == '-l':
            dummy_thread = threading.Thread(target=udp_listener, args=(i, "", 9000 + i, 5))
        else:
            dummy_thread = threading.Thread(target=udp_sender, args=(i, "192.168.1.120", 9000 + i, 5))
        thread_list.append(dummy_thread)

    try:
        for item in thread_list: item.start()
    except KeyboardInterrupt:
        for item in thread_list: item.join()
        print("KeyboardInterrupt. Stopping script.")
