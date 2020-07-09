import socket


def tcp_gps_lisener(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    file_id = open("tcp_gps_output.txt", "a+")
    file_id.truncate(0)
    while (1):
        response = client.recv(4096).replace('\r', '')
        file_id.write(response)
        file_id.flush()
        print(response)


def udp_gps_lisener(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    file_id = open("udp_gps_output.txt", "a+")
    file_id.truncate(0)
    while True:
        data, addr = sock.recvfrom(1024)
        file_id.write(data.replace('\r', ''))
        file_id.flush()
        print(data.replace('\r', ''))


if __name__ == "__main__":
    try:
        udp_gps_lisener("0.0.0.0", 5067)
        # tcp_gps_lisener("20.1.100.1", 9345)
    except KeyboardInterrupt:
        print("KeyboardInterrupt. Stopping script.")
