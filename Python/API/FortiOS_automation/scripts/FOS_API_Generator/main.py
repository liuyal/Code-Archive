import os
import sys
import git
import stat
import shutil
import argparse

from cryptography.fernet import Fernet

import json_parser
import fndn_parser
import fos_api_generator_config
import fos_api_generator_monitor
import fos_api_generator_log


def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


def decode(pwd_path, key_path):
    encrypt_pwd = open(pwd_path, "r").read()
    fernet_code = Fernet(open(key_path, "rb").read())
    decoded_pwd = fernet_code.decrypt(encrypt_pwd.encode('utf-8')).decode()
    return decoded_pwd


def generate_init_file(output_path):
    f = open(output_path + os.sep + '__init__.py', 'a+')
    f.truncate(0)
    for folder in os.listdir(output_path):
        if '.py' not in folder:
            for file in os.listdir(output_path + os.sep + folder):
                if '.py' in file and '__init__' not in file:
                    f.write('from .' + folder.replace('-', '_') + ' import ' + file.replace('.py', '') + '\n')
                    f.flush()
    f.close()


def create_output_path(output_path):
    if os.path.exists(output_path): shutil.rmtree(output_path, onerror=on_rm_error)
    os.mkdir(output_path)


def repo_update(output_path, version):

    branch = 'fos_rest_api_' + version.replace('.', '').split()[-1]

    output_path_c = output_path + 'configuration'
    output_path_l = output_path + 'log'
    output_path_m = output_path + 'monitor'

    create_output_path(os.getcwd() + os.sep + 'testscript')

    git_url = 'https://gl.devqalab.fortilab.net/root/testscript.git'
    repo = git.Repo.clone_from(git_url, 'testscript')

    testscript_api_path_c = os.getcwd() + os.sep + 'testscript' + os.sep + 'libs' + os.sep + 'fgtapi' + os.sep + 'configuration'
    testscript_api_path_l = os.getcwd() + os.sep + 'testscript' + os.sep + 'libs' + os.sep + 'fgtapi' + os.sep + 'log'
    testscript_api_path_m = os.getcwd() + os.sep + 'testscript' + os.sep + 'libs' + os.sep + 'fgtapi' + os.sep + 'monitor'

    template_path_c = testscript_api_path_c + os.sep + 'template.py'
    template_path_l = testscript_api_path_l + os.sep + 'template.py'
    template_path_m = testscript_api_path_l + os.sep + 'template.py'

    shutil.copyfile(template_path_c, output_path_c + os.sep + 'template.py')
    shutil.copyfile(template_path_l, output_path_l + os.sep + 'template.py')
    shutil.copyfile(template_path_m, output_path_m + os.sep + 'template.py')

    repo.git.checkout(b=branch)

    shutil.rmtree(testscript_api_path_c)
    shutil.rmtree(testscript_api_path_l)
    shutil.rmtree(testscript_api_path_m)

    shutil.copytree(output_path_c, testscript_api_path_c)
    shutil.copytree(output_path_l, testscript_api_path_l)
    shutil.copytree(output_path_m, testscript_api_path_m)

    repo.git.add(all=True)
    repo.index.commit("Update REST API to " + version)
    repo.git.push('--set-upstream', 'origin', branch)

    shutil.rmtree(os.getcwd() + os.sep + 'testscript', onerror=on_rm_error)


if __name__ == '__main__':
    encrpt_pwd = r'C:\Users\ljerry\OneDrive-Fortinet\3_Code\Python\FGT_Automation\scripts\Crypto_Generator\encrypt_pwd.key'
    key = r'C:\Users\ljerry\OneDrive-Fortinet\3_Code\Python\FGT_Automation\scripts\Crypto_Generator\key.txt'

    parser = argparse.ArgumentParser(description='', formatter_class=argparse.RawTextHelpFormatter)
    requiredNamed = parser.add_argument_group('Required Arguments')
    requiredNamed.add_argument("-v", "--version", action='store', type=str, dest="version", help='FGT REST API Version', required=True)
    requiredNamed.add_argument("-u", "--user", action='store', type=str, dest="user", help='LDAP User Email', required=True)
    requiredNamed.add_argument("-p", "--password", action='store', type=str, dest="password", help='LDAP Password', required=True)
    input_arg = parser.parse_args()

    usr = input_arg.user if input_arg.user else 'ljerry@fortinet.com'
    pwd = input_arg.password if input_arg.password else decode(encrpt_pwd, key)

    version = 'FortiOS ' + input_arg.version if input_arg.version else '7.2.0'
    download_path = os.getcwd() + os.sep + 'api_json' + version.split(' ')[-1].replace('.', '')
    file_header = 'fos' + version.split(' ')[-1].replace('.', '')

    print("Generating FNDN REST API LIB: " + version)
    fndn_parser.runner(version, usr, pwd, download_path)

    print("Parsing JSON files")
    json_parser.runner(download_path, file_header)

    output_path_c = os.getcwd() + os.sep + 'configuration'
    output_path_l = os.getcwd() + os.sep + 'log'
    output_path_m = os.getcwd() + os.sep + 'monitor'

    create_output_path(output_path_c)
    create_output_path(output_path_l)
    create_output_path(output_path_m)

    fos_api_generator_config.runner(file_header + '_configuration.txt', output_path_c)
    fos_api_generator_log.runner(file_header + '_log.txt', output_path_l)
    fos_api_generator_monitor.runner(file_header + '_monitor.txt', output_path_m)

    generate_init_file(output_path_c)
    generate_init_file(output_path_l)
    generate_init_file(output_path_m)

    repo_update(os.getcwd() + os.sep, version)

    print("COMPLETE!")
