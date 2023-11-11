import os
import sys
import time
import datetime
import argparse
import shutil
from pathlib import Path

sys.path.append(os.getcwd() + os.sep + "lib")
from lib import fgt
from lib import fsw
from lib import ssh
from lib import tftp
from lib import utility
from lib import phab


def check_jump_connection(hostname, ip, config_yaml):
    jump_host_ip = config_yaml['GLOBAL']['SSH_JUMP_HOST'][0]['IP']
    jump_host_user = config_yaml['GLOBAL']['SSH_JUMP_HOST'][0]['USR']
    if not os.path.exists(os.getcwd() + os.sep + "keys"):
        jump_host_key = "/home/ljerry/keys/id_rsa"
    else:
        jump_host_key = str(Path.home()) + os.sep + ".ssh" + os.sep + "id_rsa"
    utility.cs_log("Checking Connection to " + hostname + "...\n")
    connection = utility.check_connections(hostname, ip, verbose=False)
    if connection != False:
        utility.cs_log(hostname + " Pinged!\n")
        jump_client = None
    else:
        utility.cs_log("Unable to Reach " + hostname + " directly, Creating Jump Host at " + jump_host_ip + "\n")
        jump_client = ssh.SSH(host_ip=jump_host_ip, usr=jump_host_user, key=jump_host_key)
        jump_client = jump_client.ssh_client
    return jump_client


def create_fsw_connection(config_yaml):
    fsw_ip = config_yaml['GLOBAL']['FSW_448D']['IP']
    fsw_user = config_yaml['GLOBAL']['FSW_448D']['USR']
    fsw_pwd = config_yaml['GLOBAL']['FSW_448D']['PWD']
    jump_host = check_jump_connection("FortiSwitch", fsw_ip, config_yaml)
    return fsw.FSW(fsw_ip, fsw_user, fsw_pwd, jump_host)


def create_fgt_connection(fgt_info, config_yaml):
    fgt_ip = fgt_info[0]

    if len(fgt_info) >= 2:
        fgt_usr = fgt_info[1]
    else:
        fgt_usr = "admin"
        for item in list(config_yaml["FGT"]):
            if fgt_ip == config_yaml["FGT"][item]["IP"]:
                fgt_usr = config_yaml["FGT"][item]["USR"]
                break
    if len(fgt_info) >= 3:
        fgt_pwd = fgt_info[2]
    else:
        fgt_pwd = ""
        for item in list(config_yaml["FGT"]):
            if fgt_ip == config_yaml["FGT"][item]["IP"]:
                fgt_pwd = config_yaml["FGT"][item]["PWD"]
                break
    jump_host = check_jump_connection("Fortigate", fgt_ip, config_yaml)
    return fgt.FGT(ip=fgt_ip, usr=fgt_usr, pwd=fgt_pwd, jump_client=jump_host)


def create_tftp_connection(config_yaml, tftp_info):
    if tftp_info:
        tftp_ip = tftp_info[0]
        tftp_usr = tftp_info[1]
        tftp_pwd = tftp_info[2]
    else:
        tftp_ip = config_yaml['GLOBAL']['TFTP_SERVER'][0]['IP']
        tftp_usr = config_yaml['GLOBAL']['TFTP_SERVER'][0]['USR']
        tftp_pwd = config_yaml['GLOBAL']['TFTP_SERVER'][0]['PWD']
    tftp_path = "/home/" + tftp_usr + "/Documents/tftp/"
    jump_host = check_jump_connection("TFTP Server", tftp_ip, config_yaml)
    return tftp.TFTP(tftp_ip, tftp_usr, tftp_pwd, tftp_path, jump_host)


def fgt_auto_upgrade(upgrade_info, config_yaml, fgt, tftp_info=None):
    fgt_target_version, fgt_target_build = upgrade_info

    key_path = os.getcwd() + os.sep + "scripts" + os.sep + "Crypto_Generator" + os.sep + "key.txt"
    pwd_path = os.getcwd() + os.sep + "scripts" + os.sep + "Crypto_Generator" + os.sep + "encrypt_pwd.key"

    if not os.path.exists(os.getcwd() + os.sep + "keys"):
        pwd_path = "/home/ljerry/keys/encrypt_pwd.key"
        key_path = "/home/ljerry/keys/key.txt"

    image_server_ip = config_yaml['GLOBAL']['IMAGE_SERVER']['IP']
    tftp = create_tftp_connection(config_yaml, tftp_info)

    ljerry_pwd = utility.decode(pwd_path, key_path)
    smb = utility.smb_connect(image_server_ip, 'ljerry', ljerry_pwd, 'VAN-915138-LT0', 'FORTINET-US')

    local_image_file_path = utility.select_build(fgt.device_type, fgt.device_model, fgt_target_version, fgt_target_build, smb)
    tftp.tftp_upload(local_image_file_path, tftp.tftp_path)
    fgt.exec_upgrade(fgt_target_version, fgt_target_build, local_image_file_path.split(os.sep)[-1], tftp.tftp_ip)
    tftp.tftp_clear_site(tftp.tftp_path, ".out")


def fgt_upload_config(config_file_name, config_yaml, fgt, tftp_info=None):
    local_config_path = os.getcwd() + os.sep + config_file_name
    tftp = create_tftp_connection(config_yaml, tftp_info)
    tftp.tftp_upload(local_config_path, tftp.tftp_path)
    fgt.exec_upload_config(tftp.tftp_ip, config_file_name)
    tftp.tftp_clear_site(tftp.tftp_path, ".conf")


def create_task_folder(path, id, ssh, remote=False):
    if not remote:
        if not os.path.exists(path + os.sep + id):
            os.mkdir(path + os.sep + id)
        if not os.path.exists(path + os.sep + id + os.sep + "Reference"):
            os.mkdir(path + os.sep + id + os.sep + "Reference")
        if not os.path.exists(path + os.sep + id + os.sep + "Reference" + os.sep + "image"):
            os.mkdir(path + os.sep + id + os.sep + "Reference" + os.sep + "image")

        check_list_exist = False
        for item in os.listdir(path + os.sep + id):
            if "check" in item.lower():
                check_list_exist = True
        if check_list_exist == False:
            shutil.copyfile(path + os.sep + "Checklist_T.txt", path + os.sep + id + os.sep + "Checklist_" + id + ".txt")
        return path + os.sep + id + os.sep + "Reference" + os.sep + "image"
    else:
        win_sep = r"\A".replace('A', '')
        ssh.exec_cmd("mkdir " + '"' + path + win_sep + id + '"')
        ssh.exec_cmd("mkdir " + '"' + path + win_sep + id + win_sep + "Reference" + '"')
        image_path = '"' + path + win_sep + id + win_sep + "Reference" + win_sep + "Image" + '"'
        ssh.exec_cmd("mkdir <PATH>".replace('<PATH>', image_path))
        return path + win_sep + id + win_sep + "Reference" + win_sep + "image"


def phab_runner(task_id):
    task_id = task_id.strip()
    task_folder_path = r"C:\Users\ljerry\OneDrive-Fortinet\1_Tasks"
    phab_url = r"https://phab.corp.fortinet.com/"

    key_path = os.getcwd() + os.sep + "scripts" + os.sep + "Crypto_Generator" + os.sep + "key.txt"
    pwd_path = os.getcwd() + os.sep + "scripts" + os.sep + "Crypto_Generator" + os.sep + "encrypt_pwd.key"
    host_key = str(Path.home()) + os.sep + ".ssh" + os.sep + "id_rsa"

    if sys.platform != 'win32' and not os.path.exists(os.getcwd() + os.sep + "keys"):
        pwd_path = "/home/ljerry/keys/encrypt_pwd.key"
        key_path = "/home/ljerry/keys/key.txt"
        host_key = "/home/ljerry/keys/id_rsa"

    pc = ssh.SSH(host_ip="172.17.216.160", usr="ljerry", key=host_key)
    image_path = create_task_folder(task_folder_path, task_id, pc, os.name != 'nt')
    phab_id = phab.PHAB(task_id, pc)
    phab_id.open_site(phab_url + task_id)
    phab_id.login("ljerry", utility.decode(pwd_path, key_path))
    phab_id.create_url_shortcut(task_folder_path + os.sep + task_id)
    phab_id.update_checklist(task_folder_path + os.sep + task_id + os.sep + "Checklist_" + task_id + ".txt", task_folder_path)
    phab_id.get_diff_id()
    phab_id.get_build_folder(image_path)
    phab_id.close_driver()


# TODO: add upload firmware file directly
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-fgt", "--fortigate", action='store', nargs='+', type=str, dest="fgt_info", help='FGT Mode -fgt <IP> <USR> <PWD>')
    parser.add_argument("-fsw", "--fortiswitch", action='store', nargs='+', type=str, dest="fsw_info", help='FSW Mode -fsw <IP> <USR> <PWD>')
    parser.add_argument("-u", "--upgrade", action='store', nargs='+', type=str, dest="upgrade_info", help='Upgrade target -u <VERSION> <BUILD>')
    # parser.add_argument("-f", "--upload_firmware", action='store', nargs='+', type=str, dest="upload_info", help='Upload Firmware -f <FIRMWARE_FILE>')
    parser.add_argument("-c", "--config", action='store', type=str, dest="config_info", help='Restore Configuration -c <CONFIG_NAME>')
    parser.add_argument("-tftp", "--TFTP", action='store', nargs='+', type=str, dest="tftp_info", help='TFTP info -tftp <IP> <USR> <PWD>')
    parser.add_argument("-ph", "--phab", action='store', type=str, dest="phab_info", help='Run Phab Task Setup -ph <PHAB_TASK_ID>')
    input_arg = parser.parse_args()

    config_yaml = utility.load_yaml_config(os.getcwd() + os.sep + "config" + os.sep + "config.yaml")
    utility.logging_setup()

    if input_arg.phab_info != None:
        phab_info = input_arg.phab_info
        phab_runner(phab_info)

    if input_arg.tftp_info != None:
        tftp_info = input_arg.tftp_info
    else:
        tftp_info = None

    if input_arg.fgt_info != None:
        fgt = create_fgt_connection(input_arg.fgt_info, config_yaml)

        if input_arg.upgrade_info != None:
            fgt_auto_upgrade(input_arg.upgrade_info, config_yaml, fgt, tftp_info)

        if input_arg.config_info != None:
            fgt_upload_config(input_arg.config_info, config_yaml, fgt, tftp_info)
