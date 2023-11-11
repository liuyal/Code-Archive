import os
import sys
import time
import re
import utility
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class PHAB():

    def __init__(self, id, ssh_client):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280x1024')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.ssh_client = ssh_client
        self.phab_url = r"https://phab.corp.fortinet.com/"
        self.task_id = id
        self.task_title = ""
        self.task_url = ""
        self.diff_id = ""
        self.diff_url = ""
        self.diff_folder = ""

    def phab_cs_log(self, text, type="INFO"):
        utility.cs_log(text, type)

    def open_site(self, url):
        self.phab_cs_log("Opening Task URL: " + url + '\n')
        self.task_url = url
        self.driver.get(url)

    def close_driver(self):
        self.driver.quit()

    def login(self, user, password):
        self.driver.find_element(By.ID, 'UQ0_0').send_keys(user)
        self.driver.find_element(By.ID, 'UQ0_1').send_keys(password)
        self.driver.find_element(By.NAME, "__submit__").click()

    def create_url_shortcut(self, task_folder_path):
        title_element = self.driver.find_elements(By.CLASS_NAME, "phui-header-header")
        title = title_element[0].text
        title = re.sub('[^0-9a-zA-Z]+', ' ', title).lstrip()
        self.task_title = title
        self.phab_cs_log("Creating Task Shortcut for: " + self.task_id + " " + title + ".url\n")
        elements = self.driver.find_elements(By.CLASS_NAME, "phui-property-list-properties")[0]
        labels = elements.text.split('\n')
        for i in range(0, len(labels)):
            if "Mantis" in labels[i]:
                self.mantis_id = labels[i + 1]

        if os.name != 'nt':
            win_sep = r"\A".replace('A', '')
            link_path = task_folder_path + win_sep + self.task_id + " " + title + ".url"
            cmd1 = "echo " + "[InternetShortcut]>" + '"' + link_path + '"'
            cmd2 = "echo URL=" + self.task_url + ">>" + '"' + link_path + '"'
            cmd3 = "echo F|xcopy " + '"' + link_path + '" "' + link_path.replace('.url', '_.url') + '"'
            cmd4 = "del /q " + '"' + link_path + '"'
            self.ssh_client.exec_cmd(cmd1)
            self.ssh_client.exec_cmd(cmd2)
            self.ssh_client.exec_cmd(cmd3)
            self.ssh_client.exec_cmd(cmd4)
        else:
            f = open(task_folder_path + os.sep + self.task_id + " " + title + ".url", "w+")
            f.truncate(0)
            f.write("[InternetShortcut]\nURL=" + self.task_url)
            f.flush()
            f.close()

    def update_checklist(self, check_list_temp_path, task_folder_path):
        if os.name != 'nt':
            win_sep = r"\A".replace('A', '')
            check_list_path = task_folder_path + win_sep + self.task_id + win_sep + "Checklist_" + self.task_id + ".txt"
            result = self.ssh_client.exec_cmd("if exist " + '"' + check_list_path + '"' + " (echo YES) else (echo NO)")
            if "NO" in result:
                f = open(os.getcwd() + os.sep + "templates" + os.sep + "Checklist_T.txt", "r+")
                txt = f.read()
                f.close()
                start_index = txt.find('Mantis ID:')
                end_index = txt.find('\n', start_index)
                txt = txt.replace(txt[start_index:end_index], 'Mantis ID: ' + self.mantis_id)
                start_index = txt.find('Bug Description:')
                end_index = txt.find('\n', start_index)
                txt = txt.replace(txt[start_index:end_index], 'Bug Description: ' + self.task_title)
                for line in txt.split('\n'):
                    line = line.replace('\n', '')
                    if len(line) < 1:
                        cmd = "echo.>>" + '"' + task_folder_path + win_sep + self.task_id + win_sep + "Checklist_" + self.task_id + ".txt" + '"' + '\n'
                    else:
                        cmd = "echo " + line.replace('<', '^<') + ">>" + '"' + task_folder_path + win_sep + self.task_id + win_sep + "Checklist_" + self.task_id + ".txt" + '"' + '\n'
                    self.ssh_client.exec_cmd(cmd)
        else:
            f = open(check_list_temp_path, 'r+')
            txt = f.read()
            f.close()
            start_index = txt.find('Mantis ID:')
            end_index = txt.find('\n', start_index)
            txt = txt.replace(txt[start_index:end_index], 'Mantis ID: ' + self.mantis_id)
            start_index = txt.find('Bug Description:')
            end_index = txt.find('\n', start_index)
            txt = txt.replace(txt[start_index:end_index], 'Bug Description: ' + self.task_title)
            f = open(check_list_temp_path, 'w+')
            f.truncate(0)
            f.write(txt)
            f.flush()
            f.close()

    def get_diff_id(self):
        self.phab_cs_log("Getting DIFF...\n")
        diff_xpath = '//*[@id="phabricator-standard-page-body"]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/dl/dd[1]/span/a'
        diff_element = self.driver.find_elements(By.XPATH, diff_xpath)
        if len(diff_element) == 0:
            self.phab_cs_log("DIFF not created...EXIT\n")
            self.close_driver()
            sys.exit(0)
        self.diff_id = diff_element[0].text.split(":")[0]
        self.diff_url = self.phab_url + self.diff_id
        self.phab_cs_log("DIFF: " + self.diff_id + ' ' + self.diff_url + '\n')
        self.driver.get(self.diff_url)

    def get_build_folder(self, image_path):
        elements = self.driver.find_elements(By.XPATH, "//*[contains(text(),'Build')]")
        build_folder_path = ""
        for item in reversed(elements):
            if "smb" in item.text:
                build_folder_path = item.text.split('\n')[-1].split(':')[-1]
                break
        if build_folder_path == "":
            self.phab_cs_log("Build Not Available\n")
            self.close_driver()
            sys.exit(0)

        if 'trunk' in build_folder_path:
            index = build_folder_path.find("trunk") + len("trunk")
            build_folder_path = build_folder_path[0:index + 1]

        diff = list(filter(None, build_folder_path.split('/')))[4]
        build_folder_path = '/'.join(build_folder_path.split('/')[0:7])
        self.phab_cs_log("Build: " + build_folder_path.replace('/', os.sep) + '\n')

        if os.name != 'nt':
            cmd1 = "echo " + "[InternetShortcut]>" + '"' + image_path + '\\' + "trunk_" + diff + ".url" + '"'
            cmd2 = "echo URL=file:" + build_folder_path + ">>" + '"' + image_path + '\\' + "trunk_" + diff + ".url" + '"'
            self.ssh_client.exec_cmd(cmd1)
            self.ssh_client.exec_cmd(cmd2)
        else:
            from win32com.client import Dispatch
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(image_path + os.sep + "trunk_" + diff + ".lnk")
            shortcut.Targetpath = build_folder_path.replace('/', os.sep)
            shortcut.save()

    def rename_folder(self, src):
        os.rename(src, src + ' - ' + self.task_title)
