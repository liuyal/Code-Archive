import os
import sys
import time
import threading
import subprocess
import socket


def tcp_listen(thread_id, TCP_IP, TCP_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(1)
    connect, address = sock.accept()
    while True:
        data = connect.recv(1024)
        sys.stdout.write("[" + str(thread_id) + "] Packet: " + str(address) + "\t" + str(data) + '\n')


def tcp_send(thread_id, TCP_IP, TCP_PORT):
    sys.stdout.write("[" + str(thread_id) + "] Start SEND \n")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    while True:
        sock.send(b"<HELLO>\n")

    # sock.close()


if __name__ == "__main__":

    thread_list = []

    for i in range(5000, 5150):

        if sys.argv[1] == "-s":
            thread = threading.Thread(target=tcp_send, args=(i, "13.1.1.10", i))
        else:
            thread = threading.Thread(target=tcp_listen, args=(i, "0.0.0.0", i))

        thread_list.append(thread)

    for thread in thread_list: thread.start()
    for thread in thread_list: thread.join()
