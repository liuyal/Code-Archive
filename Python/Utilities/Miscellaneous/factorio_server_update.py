import os
import sys
import time
import scp
import paramiko
import argparse


def update_save(ssh, scp):
    print("Updating Server Save File...")
    print("Stopping factorio.service...")
    ssh.exec_command('systemctl stop factorio.service')

    time.sleep(3)

    print("Updating save zip file via SCP...")
    scp.put(local_save_path, server_save_path)

    print("Restarting factorio.service...")
    ssh.exec_command('systemctl restart factorio.service')

    time.sleep(3)

    stdin, stdout, stderr = ssh.exec_command('systemctl status factorio.service --no-pager')
    print("".join(stdout.readlines()))

    stdin, stdout, stderr = ssh.exec_command('cd /opt/factorio/saves/; ls -al')
    print("".join(stdout.readlines()))

    print("Update Complete!")


def restart(ssh):
    print("Restarting factorio.service...")
    ssh.exec_command('systemctl restart factorio.service')

    time.sleep(5)

    stdin, stdout, stderr = ssh.exec_command('systemctl status factorio.service --no-pager')
    print("".join(stdout.readlines()))

    print("Restart Complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-u", "--update", action='store_true', help='Update Server Save File')
    parser.add_argument("-s", "--start", action='store_true', help='Start Server Factorio.service')

    inputs = parser.parse_args()

    local_save_path = r"F:\Game\Factorio\saves\wonderland.zip"
    # local_save_path = os.getcwd() + os.sep + "saves" + os.sep + "wonderland.zip"
    server_save_path = r"/opt/factorio/saves/wonderland.zip"
    server_ip = "192.168.1.120"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=server_ip, username='root', password='1234', port=22)
    scp = scp.SCPClient(ssh.get_transport())

    if inputs.update:
        update_save(ssh, scp)
    elif inputs.start:
        restart(ssh)
    elif not inputs.update and not inputs.start:
        input_value = input("Update(u) or Restart (s): ")

        if input_value.lower() == "s":
            restart(ssh)
        elif input_value.lower() == "u":
            update_save(ssh, scp)

    time.sleep(3)
