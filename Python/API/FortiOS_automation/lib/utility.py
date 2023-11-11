import os
import sys
import time
import shutil
import datetime
import platform
import subprocess
import logging
import termcolor
import yaml

from smb.SMBConnection import SMBConnection
from cryptography.fernet import Fernet


def cs_log(text, type="INFO"):
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color_text = text
    if type == "INFO":
        logging.info(text.replace('\n', ''))
    elif type == "FLAG":
        logging.debug(text.replace('\n', ''))
        # color_text = termcolor.colored(text, "green")
    elif type == "DEBUG":
        logging.debug(text.replace('\n', ''))
        # color_text = termcolor.colored(text, "cyan")
    elif type == "WARN":
        logging.warning(text.replace('\n', ''))
        # color_text = termcolor.colored(text, "yellow")
    elif type == "CRIT":
        logging.critical(text.replace('\n', ''))
        # color_text = termcolor.colored(text, "magenta")
    elif type == "ERROR":
        logging.error(text.replace('\n', ''))
        # color_text = termcolor.colored(text, "red", attrs=['bold'])
    print(time_stamp, type.ljust(5), '', color_text, end='')


def load_yaml_config(path):
    f = open(path, 'r')
    config_yaml = yaml.safe_load(f)
    f.close()
    return config_yaml


def logging_setup():
    if not os.path.exists(os.getcwd() + os.sep + "log"): os.mkdir(os.getcwd() + os.sep + "log")
    if not os.path.exists(os.getcwd() + os.sep + "results"): os.mkdir(os.getcwd() + os.sep + "results")
    # logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    # logFormatter = logging.Formatter("%(asctime)s %(levelname)-6s %(message)s")
    # consoleHandler = logging.StreamHandler()
    # consoleHandler.setFormatter(logFormatter)
    # logging.getLogger().addHandler(consoleHandler)
    log_file_name = os.getcwd() + os.sep + "log" + os.sep + datetime.datetime.now().strftime("%y%m%d_%H%M%S") + '_automation.log'
    logging.basicConfig(filename=log_file_name, format='%(asctime)s [%(threadName)-12.12s]  %(levelname)-6s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')


def decode(pwd_path, key_path):
    encrypt_pwd = open(pwd_path, "r").read()
    fernet_code = Fernet(open(key_path, "rb").read())
    decoded_pwd = fernet_code.decrypt(encrypt_pwd.encode('utf-8')).decode()
    return decoded_pwd


def get_os(ssh):
    stdin, stdout, stderr = ssh.exec_command("systeminfo")
    for line in stdout.read().split(b'\n'):
        line = str(line.decode('utf-8'))
        if "OS Name:".lower() in line.lower():
            if any("Windows" in x for x in line.split(' ')):
                return "windows"
    stdin, stdout, stderr = ssh.exec_command("uname -mrs")
    for line in stdout.read().split(b'\n'):
        line = str(line.decode('utf-8'))
        if "Linux".lower() in line.lower():
            if any("Linux" in x for x in line.split(' ')):
                return "Linux"
    cs_log("ERROR GETTING OS...", "ERROR")
    sys.exit(-1)


def ping(host, os_version):
    param = '-n' if os_version == 'windows' else '-c'
    command = ['ping', param, '1', host]
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    if "(0% loss)" in str(output) or ", 0% packet loss" in str(output):
        return True
    else:
        return False


def check_connections(host, ip, jump_host=None, verbose=True):
    if jump_host == None:
        if verbose: cs_log("Pinging " + host + ": " + ip + "...\n")
        if ping(ip, platform.system().lower()) == True:
            if verbose: cs_log("Ping Successful!\n", "FLAG")
            return True
        else:
            if verbose: cs_log("Ping Failed!\n", "WARN")
    else:
        os_version = get_os(jump_host)
        if verbose: cs_log("Pinging " + host + ": " + ip + "...\n")
        command = ['ping', '-n' if os_version.lower() == 'windows' else '-c', '1', ip]
        stdin, stdout, stderr = jump_host.exec_command(' '.join(command))
        for line in stdout.read().split(b'\n'):
            line = str(line.decode('utf-8'))
            if "(0% loss)" in line or ", 0% packet loss" in line:
                if verbose: cs_log("Ping Successful!\n", "FLAG")
                return True
        if verbose: cs_log("Ping Failed!\n", "WARN")
    return False


def smb_connect(server_ip, username, password, client_machine_name, server_name):
    smb_connection = SMBConnection(username=username, password=password, my_name=client_machine_name, remote_name=server_name, domain=server_name)
    smb_connection.connect(ip=server_ip, port=139, timeout=300)
    return smb_connection


def select_build(device_type, device_model, target_version, target_branch, smb):
    version_list = []
    build_list = []
    selected_version = ""
    selected_build = ""
    image_file_name = ""
    image_build_path = r"/FortiOS/<VERSION>/images/"
    image_server_service_name = "Images"

    for folder in smb.listPath(image_server_service_name, '/FortiOS/'):
        if "v" in folder.filename.lower() and '.' in folder.filename.lower():
            version_list.append(folder.filename)

    if target_version != "":
        for version in version_list:
            if str(target_version).lower() in version:
                selected_version = version
                break
        if selected_version == "":
            version_list.sort()
            cs_log('Available versions:\n', "INFO")
            for item in version_list: cs_log(item + '\n', "INFO")
            cs_log("Target version " + str(target_version) + " not in database... EXITING\n", "ERROR")
            sys.exit(-1)
        cs_log("Selected Target version: " + selected_version + '\n')
    else:
        cs_log("Incorrect version input... EXITING\n", "ERROR")
        sys.exit(-1)

    for folder in smb.listPath(image_server_service_name, image_build_path.replace("<VERSION>", selected_version)):
        if 'build' in folder.filename:
            build_list.append(folder.filename)

    if target_branch != '':
        for build in build_list:
            if str(target_branch).lower() in build:
                selected_build = build
                break
        if selected_build == "":
            build_list.sort()
            cs_log('Available builds:\n', "INFO")
            for item in build_list: cs_log(item.replace('build', '') + '\n', "INFO")
            cs_log("Target build " + str(target_branch) + " not in database... EXITING\n", "ERROR")
            sys.exit(-1)
        cs_log("Selected Target build: " + selected_build + '\n')
    else:
        cs_log("Incorrect build input... EXITING\n", "ERROR")
        sys.exit(-1)

    if "fortiwifi" in device_type.lower():
        type = "FWF"
    else:
        type = "FGT"

    cs_log("Downloading image to local drive...\n")
    if not os.path.exists(os.getcwd() + os.sep + "tmp"): os.mkdir(os.getcwd() + os.sep + "tmp")
    for folder in smb.listPath(image_server_service_name, image_build_path.replace("<VERSION>", selected_version) + selected_build + '/'):
        if '_' + device_model + '-' in folder.filename and type in folder.filename and '.out' in folder.filename:
            if folder.filename.split('.')[-1] == 'out':
                image_file_name = os.getcwd() + os.sep + "tmp" + os.sep + folder.filename
                f = open(image_file_name, 'wb')
                smb.retrieveFile(image_server_service_name,
                                 image_build_path.replace("<VERSION>", selected_version) + selected_build + '/' + folder.filename, f)

    if image_file_name == "":
        cs_log(type + " Image for version " + selected_version + " build " + selected_build + " does not exist... EXITING\n", "ERROR")
        sys.exit(-1)

    return image_file_name
