import os, sys, threading, time
import socket as socket


def udp_listener(cv, UDP_IP="0.0.0.0", UDP_PORT=9996, time_out=5):
    global data
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(time_out)
    sock.bind((UDP_IP, UDP_PORT))
    try:
        while True:
            data, address = sock.recvfrom(1024)
            cv.acquire()
            cv.notifyAll()
            cv.release()
            print("Packet: " + str(address) + "\t" + str(data))
    except socket.timeout:
        sock.close()

def printer(cv, thread_id):
    global data
    while True:
        cv.acquire()
        cv.wait()
        cv.release()
        print("\n" + str(thread_id) + ":" + str(data))


if __name__ == "__main__":

    data = ""
    condition = threading.Condition()

    t_main = threading.Thread(target=udp_listener, args=(condition, "0.0.0.0", 9996, 600))
    t1 = threading.Thread(target=printer, args=(condition, 1))
    t2 = threading.Thread(target=printer, args=(condition, 2))

    t_main.start()
    t1.start()
    t2.start()
    




