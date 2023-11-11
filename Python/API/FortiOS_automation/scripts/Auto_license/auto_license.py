import os
import sys
import re
import time
import shutil
import PyPDF2
import paramiko
import tftpy
import socket

from scp import SCPClient
from cryptography.fernet import Fernet

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def decode(pwd_path, key_path):
    encrypt_pwd = open(pwd_path, "r").read()
    fernet_code = Fernet(open(key_path, "rb").read())
    decoded_pwd = fernet_code.decrypt(encrypt_pwd.encode('utf-8')).decode()
    return decoded_pwd


def get_login(key_path):
    pwd_path = key_path + os.sep + "keys" + os.sep + "encrypt_pwd.key"
    key_path = key_path + os.sep + "keys" + os.sep + "key.txt"
    ljerry_pwd = decode(pwd_path, key_path)
    return 'ljerry@fortinet.com', ljerry_pwd


def get_key(folder):
    licenses = []
    for file_name in os.listdir(folder):
        if os.path.isfile(folder + os.sep + file_name) and '.pdf' in file_name:
            file = open(folder + os.sep + file_name, 'rb')
            fileReader = PyPDF2.PdfFileReader(file)
            for i in range(fileReader.numPages):
                current_page = fileReader.getPage(i)
                text = current_page.extractText()
                start = text.find("FORTINET INCRegistration Code   :")
                end = text.find("Evaluation license term", start)
                li = text[start + len("FORTINET INCRegistration Code   :"):end].strip()
                licenses.append((file_name.split('.')[0], li))
    for file, li in licenses: print(file, li)
    return licenses


def create_driver():
    if os.path.exists(os.getcwd() + os.sep + 'licenses'):
        shutil.rmtree(os.getcwd() + os.sep + 'licenses')
    os.mkdir(os.getcwd() + os.sep + 'licenses')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1900x950')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_service = Service(ChromeDriverManager().install())
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.getcwd() + os.sep + 'licenses',
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.set_window_size(1900, 950)
    return driver


def register_key(url, usr, pwd, licenses, fgt_id):
    if len(licenses) < 1: return
    driver = create_driver()
    driver.get(url)

    driver.find_element(By.CLASS_NAME, "bt-blue").click()
    driver.find_element(By.ID, 'id_username').send_keys(usr)
    driver.find_element(By.ID, 'id_password').send_keys(pwd)
    driver.find_element(By.CLASS_NAME, "submit").click()

    while True:
        try:
            service = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/div')
            service.click()
            time.sleep(5)
            break
        except:
            time.sleep(5)

    assest = driver.find_element(By.XPATH, '/html/body/div[4]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr/td/table/div/div[1]/div[1]/span[1]/div')
    assest.click()

    while True:
        try:
            register_now = driver.find_element(By.XPATH, '/html/body/app-root/div[1]/div[1]/div/as-split/as-split-area[2]/app-dashboard-container/div/div/div[1]/div[2]/app-region-overlay-loading/app-dashboard-register-now/div/button/span')
            register_now.click()
            time.sleep(5)
            break
        except:
            time.sleep(5)

    for file, key in licenses:
        try:
            print('Register:', fgt_id, file, key)
            driver.find_element(By.ID, 'RegNumber').send_keys(key)
            driver.find_element(By.ID, 'nogvmtUsr').click()
            driver.find_element(By.ID, 'btn').click()
            time.sleep(2)

            if len(driver.find_elements(By.ID, 'RegNumber')) > 0:
                print(file, key, 'USED')
                driver.refresh()
                fgt_id = fgt_id + 1
                continue

            driver.find_element(By.XPATH, '//*[@id="RegProduct"]/app-regproduct/div/div[1]/div/app-fmgvmregcontrol/div[2]/div/input').send_keys('FGT_VM_' + str(fgt_id))
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, 'select2-selection__arrow').click()
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, 'select2-search__field').send_keys('Unknown')
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, 'select2-search__field').send_keys(Keys.RETURN)
            time.sleep(1)
            driver.find_element(By.ID, 'assetTreerDropdownInput').click()
            time.sleep(1)
            driver.find_element(By.XPATH, ' //*[@id="effective-asset-permissions-menu"]/tree-root/tree-viewport/div/div/tree-node-collection/div/tree-node/div/tree-node-children/div/tree-node-collection/div/tree-node[1]/div/div/div[2]/tree-node-content/span').click()
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, 'btn-rect').click()
            time.sleep(5)

            driver.find_element(By.CLASS_NAME, 'accept-terms').click()
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, 'btn-rect').click()
            time.sleep(1)

            while True:
                try:
                    driver.find_element(By.XPATH, '//*[@id="Complete"]/app-complete/div/div[2]/div[2]/button[1]').click()
                    time.sleep(5)
                    break
                except:
                    time.sleep(5)

            fgt_id = fgt_id + 1

        except:
            time.sleep(5)

    driver.close()


def download_license(url, usr, pwd, id_list):
    driver = create_driver()
    driver.get(url)

    driver.find_element(By.CLASS_NAME, "bt-blue").click()
    driver.find_element(By.ID, 'id_username').send_keys(usr)
    driver.find_element(By.ID, 'id_password').send_keys(pwd)
    driver.find_element(By.CLASS_NAME, "submit").click()

    while True:
        try:
            service = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/div')
            service.click()
            time.sleep(5)
            break
        except:
            time.sleep(5)

    asset = driver.find_element(By.XPATH, '/html/body/div[4]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr/td/table/div/div[1]/div[1]/span[1]/div')
    asset.click()
    time.sleep(3)

    driver.find_element(By.XPATH, '/html/body/app-root/div[1]/div[1]/div/as-split/as-split-area[2]/app-dashboard-container/div/div/div[1]/div[1]/app-region-overlay-loading/app-dashboard-product-overview/div[2]/div[1]').click()
    time.sleep(2)

    for i in id_list:
        fgt_id = 'FGT_VM_' + str(i)

        while True:
            try:
                print('Download lic:' + fgt_id)
                search = driver.find_element(By.XPATH, '//*[@id="main-wrapper"]/div/as-split/as-split-area[2]/app-prod-view-container/div/div[2]/div[1]/app-prod-bar/div/div[1]/div[1]/div/div[1]/input')
                search.send_keys(fgt_id)
                time.sleep(2)
                break
            except:
                time.sleep(2)
                pass

        while True:
            try:
                serial_number_link = driver.find_element(By.CLASS_NAME, 'serial-number-link')
                serial_number = serial_number_link.text
                serial_number_link.click()
                time.sleep(2)
                break
            except:
                time.sleep(2)
                pass

        while True:
            try:
                driver.find_element(By.XPATH, '/html/body/app-root/div[1]/div[1]/div/as-split/as-split-area[2]/app-product-detail/div/div[2]/div/div[1]/app-product-general/div/div[2]/div/div/div[7]/app-product-general-field/div/div[2]/div/span/a').click()
                time.sleep(2)
                break
            except:
                time.sleep(2)
                pass

        while True:
            try:
                src = os.getcwd() + os.sep + 'licenses' + os.sep + serial_number + '.lic'
                dst = os.getcwd() + os.sep + 'licenses' + os.sep + serial_number + '_' + fgt_id + '.lic'
                os.rename(src, dst)
                break
            except:
                time.sleep(2)
                pass

        driver.execute_script("window.history.go(-1)")
        time.sleep(3)

        while True:
            try:
                search = driver.find_element(By.XPATH, '//*[@id="main-wrapper"]/div/as-split/as-split-area[2]/app-prod-view-container/div/div[2]/div[1]/app-prod-bar/div/div[1]/div[1]/div/div[1]/input')
                search.clear()
                time.sleep(2)
                break
            except:
                time.sleep(2)
                pass

    driver.close()


def upload_tftp_server():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='172.18.10.100', port=22, username='test', password='123456')
    scp = SCPClient(ssh_client.get_transport())

    for file in os.listdir(os.getcwd() + os.sep + 'licenses'):
        ip = '172.18.10.' + file.split('_')[-1].split('.')[0]
        print(ip, file)
        local_path = os.getcwd() + os.sep + 'licenses' + os.sep + file
        scp.put(local_path, '/home/test/tftp/' + local_path.split(os.sep)[-1])

    ssh_client.close()


def run_license_cmd():
    for file in os.listdir(os.getcwd() + os.sep + 'licenses'):
        ip = '172.18.10.' + file.split('_')[-1].split('.')[0]
        cmd = "exec restore vmlicense tftp " + file + " 172.18.10.100\n"
        print(ip, file, cmd)

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip, port=22, username='admin', password='')

        channel = ssh_client.invoke_shell()
        channel.send(cmd.encode())
        while not channel.recv_ready(): time.sleep(5)
        start_time = time.time()
        while True:
            stdout = channel.recv(9999).decode("ascii")
            print(stdout)
            if '##' in stdout: time.sleep(5)
            if "(y/n)" in stdout: channel.send(b'y')
            if "succeeded" in stdout and "Rebooting" in stdout: break
            if time.time() - start_time > 60: break

        ssh_client.close()


if __name__ == "__main__":
    id_list = list(range(200, 240))
    licenses = get_key(r"C:\Users\ljerry\OneDrive-Fortinet\3_Code\ADVPN5k\FGT_VM")
    get_key(r'C:\Users\ljerry\OneDrive-Fortinet\2_Lab\OS\FGT\FG-VM04_49704762')
    usr, pwd = get_login(r'C:\Users\ljerry\OneDrive-Fortinet\3_Code\Python\FGT_Automation')
    register_key('https://login.forticloud.com/', usr, pwd, licenses, id_list[0])
    download_license('https://login.forticloud.com/', usr, pwd, id_list)
    upload_tftp_server()
    run_license_cmd()

    print('EOT')