import os
import sys
import time
import traceback
import threading
import paramiko
import socket
import queue


def create_ssh_client(ip, user, pwd='', key=''):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key == '':
            ssh_client.connect(ip, username=user, password=pwd)
        else:
            ssh_client.connect(ip, username=user, key_filename=key)
        return ssh_client
    except Exception as e:
        print(e)
        return None


def create_ssh_client_jump_host(ip, user, pwd, jump_host):
    try:
        jump_host_transport = jump_host.get_transport()
        jump_ip, jump_port = jump_host_transport.getpeername()
        src_addr = (jump_ip, 22)
        dst_addr = (ip, 22)
        jump_host_channel = jump_host_transport.open_channel("direct-tcpip", dst_addr, src_addr)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip, username=user, password=pwd, sock=jump_host_channel)
        return ssh_client
    except Exception as e:
        return None


def netcat_send(thread_id, msg, ip, port=9996):
    try:
        cmd = 'nc -u ' + ip + ' ' + str(port)
        jump_host = create_ssh_client("172.17.216.160", "ljerry", '', key=os.getcwd().replace(os.path.basename(os.getcwd()), '') + "keys" + os.sep + "id_rsa")
        ssh = create_ssh_client_jump_host("10.59.71.201", "ubuntu201", "1234", jump_host)
        ssh_channel = ssh.invoke_shell()
        ssh_channel.send(cmd + '\n')
        ssh_channel.send(msg + '\n\n')
        sys.stdout.write("[" + str(thread_id) + "] Send MSG... " + cmd + "\n")
        ssh.close()
    except Exception as e:
        return None


def netcat_listen(thread_id, queue=None, port=9996, timeout=10, expect_str="", verbose=False):
    data = ""
    cmd = b'nc -ul ' + str(port).encode()
    try:
        jump_host = create_ssh_client("172.17.216.160", "ljerry", '', key=os.getcwd().replace(os.path.basename(os.getcwd()), '') + "keys" + os.sep + "id_rsa")
        ssh = create_ssh_client_jump_host("10.59.71.203", "ubuntu203", "1234", jump_host)
        ssh_channel = ssh.invoke_shell()
        ssh_channel.timeout = timeout
        ssh_channel.send(cmd + b'\n')
        sys.stdout.write("[" + str(thread_id) + "] Start Listening " + cmd.decode('utf-8') + "\n")
        while not ssh_channel.recv_ready(): time.sleep(5)
        while True:
            stdout = ssh_channel.recv(1024)
            data = data + stdout.decode("ascii")
            if verbose: sys.stdout.write(stdout.decode("ascii"))
            if expect_str in data and expect_str != "":
                sys.stdout.write("[" + str(thread_id) + "] Received:" + expect_str + "\n")
                break
        if queue != None: queue.put(data)
        ssh.close()
        return data
    except Exception as e:
        return None


def gen_sessions():
    listen_thread_list = []
    send_thread_list = []
    port_range = range(8000, 8010)

    for port in port_range:
        listen_thread = threading.Thread(target=netcat_listen, args=("L" + str(port), None, port, 30, '<hello>', False))
        send_thread = threading.Thread(target=netcat_send, args=("S" + str(port), "<hello>", "13.1.1.10", port))

        listen_thread_list.append(listen_thread)
        send_thread_list.append(send_thread)

    for thread in listen_thread_list: thread.start()
    time.sleep(5)
    for thread in send_thread_list: thread.start()

    for thread in listen_thread_list: thread.join()
    for thread in send_thread_list: thread.join()


def gen_session_v2():
    jump_host = create_ssh_client("172.17.216.160", "ljerry", '', key=os.getcwd().replace(os.path.basename(os.getcwd()), '') + "keys" + os.sep + "id_rsa")
    ssh = create_ssh_client_jump_host("10.59.71.201", "ubuntu201", "1234", jump_host)

    for _ in range(0, 5):
        for i in range(2, 255):
            cmd = "sudo ip addr add 11.1.1." + str(i) + "/24 dev ens192"
            ping_cmd = "ping 13.1.1.10 -c 1 -s 1500 -I 11.1.1." + str(i)
            stdin, stdout, stderr = ssh.exec_command(ping_cmd + '\n')
            print(ping_cmd)
        time.sleep(3)

if __name__ == "__main__":

    for i in range(2, 255):
        cmd = "sudo ip addr add 11.1.1." + str(i) + "/24 dev ens192"
        print(cmd)


