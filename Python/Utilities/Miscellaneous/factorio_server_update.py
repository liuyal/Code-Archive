import os
import sys
import time
import scp
import paramiko
import argparse


# TODO: add download save, add sync save (timestamp based)


def upload_save(ssh, scp, local_path, server_path):
    print("Uploading Server Save File...")

    print("Stopping factorio.service...")
    ssh.exec_command('systemctl stop factorio.service')
    time.sleep(3)

    print("Uploading save zip file via SCP...")
    scp.put(local_path, server_path)

    print("Restarting factorio.service...")
    ssh.exec_command('systemctl restart factorio.service')
    time.sleep(3)

    stdin, stdout, stderr = ssh.exec_command('systemctl status factorio.service --no-pager')
    print("".join(stdout.readlines()))

    stdin, stdout, stderr = ssh.exec_command('cd /opt/factorio/saves/; ls -al')
    print("".join(stdout.readlines()) + "\nUploading Complete!")


def download_save(ssh, scp, local_path, server_path):
    print("Downloading Server Save File...")

    print("Stopping factorio.service...")
    ssh.exec_command('systemctl stop factorio.service')
    time.sleep(3)

    print("Downloading save zip file via SCP...")
    scp.get(server_path, local_path)
    time.sleep(3)

    stdin, stdout, stderr = ssh.exec_command('systemctl status factorio.service --no-pager')
    print("".join(stdout.readlines()) + "\nDownload Complete!")


def restart(ssh):
    print("Restarting factorio.service...")
    ssh.exec_command('systemctl restart factorio.service')
    time.sleep(5)

    stdin, stdout, stderr = ssh.exec_command('systemctl status factorio.service --no-pager')
    print("".join(stdout.readlines()) + "\nRestart Complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-u", "--upload", action='store_true', help='Upload Server Save File')
    parser.add_argument("-d", "--download", action='store_true', help='Download Server Save File')
    parser.add_argument("-s", "--start", action='store_true', help='Start Server Factorio.service')
    inputs = parser.parse_args()

    # local_save_path = os.getcwd() + os.sep + "saves" + os.sep + "wonderland.zip"
    local_save_path = r"F:\Game\Factorio\saves\wonderland.zip"
    server_save_path = r"/opt/factorio/saves/wonderland.zip"
    server_ip = "192.168.1.120"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=server_ip, username='root', password='1234', port=22)
    scp = scp.SCPClient(ssh.get_transport())

    if inputs.upload:
        upload_save(ssh, scp, local_save_path, server_save_path)
    elif inputs.download:
        download_save(ssh, scp, local_save_path, server_save_path)
    elif inputs.start:
        restart(ssh)
    elif not inputs.upload and not inputs.download and not inputs.start:
        msg = "Select Function Index:\n[1] Upload Save\n[2] Download Save\n[3] Start Server\n"
        input_value = input(msg)
        if input_value == "1":
            upload_save(ssh, scp, local_save_path, server_save_path)
        elif input_value == "2":
            download_save(ssh, scp, local_save_path, server_save_path)
        elif input_value == "3":
            restart(ssh)
        else:
            sys.exit("ERROR: Invalid Input")

    scp.close()
    time.sleep(3)
