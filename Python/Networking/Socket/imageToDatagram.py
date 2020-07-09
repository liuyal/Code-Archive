import os, sys, time, io, zlib
import socket as socket
from PIL import Image


def udp_send(msg, UDP_IP="127.0.0.1", UDP_PORT=9996):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg, (UDP_IP, UDP_PORT))
    sock.close()


def udp_listener(UDP_IP="0.0.0.0", UDP_PORT=9996, time_out=5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(time_out)
    sock.bind((UDP_IP, UDP_PORT))
    try:
        while True:
            data, address = sock.recvfrom(1024)
            print("Packet: " + str(address) + "\t" + str(data))
    except socket.timeout:
        print("Listening done, Closing socket.")
        sock.close()


def tcp_send(msg, TCP_IP="127.0.0.1", TCP_PORT=9996):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    sock.send(msg)
    sock.close()


def tcp_listener(TCP_IP="0.0.0.0", TCP_PORT=9996, time_out=5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(time_out)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(1)
    connect, address = sock.accept()
    print(str(connect) + "\t" + str(address))
    try:
        while True:
            data = connect.recv(1024)
            print("Packet: " + str(address) + "\t" + str(data))
            connect.send(data)
    except socket.timeout:
        print("Listening done, Closing socket.")
        sock.close()


if __name__ == "__main__":

    file_name = "lenna.png"
    picture = Image.open(os.getcwd() + os.sep + "im" + os.sep + file_name)
    pictureBytes = picture.tobytes()
    bytesIOArray = io.BytesIO()
    picture.save(bytesIOArray,file_name.split(".")[-1])
    byteArray = bytesIOArray.getvalue()

    IP = "192.168.1.103"
    PORT = 9996
    MSG = str(time.time()) + "\n\r"
    TIME_OUT = 15

    # udp_send(msg=byteArray, UDP_IP=IP, UDP_PORT=PORT)
    # udp_listener(UDP_IP="0.0.0.0", UDP_PORT=PORT, time_out=TIME_OUT)
    #
    # tcp_send(msg=bytes(MSG, "utf-8"), TCP_IP=IP, TCP_PORT=PORT)
    # tcp_listener(TCP_IP="0.0.0.0", TCP_PORT=PORT, time_out=TIME_OUT)
