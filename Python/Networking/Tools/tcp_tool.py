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
    version = sys.version_info[0]
    for i in range(0, 500):
        time_stamp = str(datetime.datetime.now().strftime("%H:%M:%S"))
        sys.stdout.write("[" + str(thread_id) + "] " + time_stamp + " : " + str(i) + "\n")
        if version == 3:
            sock.sendall(str(i).encode())
        else:
            sock.sendall(str(i))
        time.sleep(1)


if __name__ == "__main__":

    try:
        sys.argv[1]
    except:
        print("Listen [-l], Send [-s]")

    N = 100
    thread_list = []

    for i in range(0, N):
        if sys.argv[1] == '-l':
            dummy_thread = threading.Thread(target=tcp_listener, args=(i, "", 9000 + i, 5))
        else:
            dummy_thread = threading.Thread(target=tcp_sender, args=(i, "192.168.1.72", 9000 + i, 5))
        thread_list.append(dummy_thread)

    try:
        for item in thread_list: item.start()
    except KeyboardInterrupt:
        for item in thread_list: item.join()
        print("KeyboardInterrupt. Stopping script.")
