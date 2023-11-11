import re
import os
import sys
import time
import shutil
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def create_data():
    data = {}
    data['cmdb'] = {}
    data['cmdb']['id'] = '0'
    data['cmdb']['types'] = []
    data['cmdb']['type_url'] = []
    data['log'] = {}
    data['log']['id'] = '0'
    data['log']['types'] = []
    data['log']['type_url'] = []
    data['monitor'] = {}
    data['monitor']['id'] = '0'
    data['monitor']['types'] = []
    data['monitor']['type_url'] = []
    return data


def create_driver(download_path):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1024')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def runner(version, usr, pwd, download_path):
    API_type_list = ["configuration api", "log api", "monitor api"]
    url = r"https://fndn.fortinet.net/index.php?/fortiapi/1-fortios/"

    if os.path.exists(download_path): shutil.rmtree(download_path)
    os.mkdir(download_path)

    data = create_data()
    driver = create_driver(download_path)
    driver.get(url)
    driver.maximize_window()
    driver.find_element(By.NAME, 'auth').send_keys(usr)
    driver.find_element(By.NAME, 'password').send_keys(pwd)
    driver.find_element(By.NAME, "_processLogin").click()

    menu_list = driver.find_elements(By.CLASS_NAME, 'fortiApi_sideMenu_listHeader')
    fos_list = [item.text.strip() for item in menu_list if len(item.text.strip()) > 0]
    if version not in fos_list: raise Exception("Incorrect version input")
    [item.click() for item in menu_list if version in item.text.strip()]
    menu_list = driver.find_elements(By.CLASS_NAME, 'fortiApi_sideMenu_listHeader')

    print('Populating URL...')
    for item in menu_list:
        if item.text.lower().strip() in API_type_list:
            driver.execute_script("arguments[0].scrollIntoView();", item)
            time.sleep(3)
            print("Searching " + item.text.strip() + "...")
            item.click()
            time.sleep(3)

            api_list = driver.find_elements(By.CLASS_NAME, 'fortiAPI_sideMenu_classList')

            for element in api_list:
                if element.text.count('\n') >= 4 and "your" not in element.text:
                    api_list = element.text.split('\n')
                    break

            if 'config' in item.text.lower():
                data['cmdb']['types'] = api_list
                data['cmdb']['id'] = item.get_attribute('data-expand')

            if 'log' in item.text.lower():
                data['log']['types'] = api_list
                data['log']['id'] = item.get_attribute('data-expand')

            if 'monitor' in item.text.lower():
                data['monitor']['types'] = api_list
                data['monitor']['id'] = item.get_attribute('data-expand')

            time.sleep(3)
            item.click()

    data['cmdb']['types'] = [item for item in data['cmdb']['types'] if not item[0].isspace()]
    data['log']['types'] = [item for item in data['log']['types'] if not item[0].isspace()]
    data['monitor']['types'] = [item for item in data['monitor']['types'] if not item[0].isspace()]

    for key in data:
        id = data[key]['id']
        for type in data[key]['types']:
            target_url = url + "<id>/1/<type>/".replace('<id>', id).replace('<type>', type)
            data[key]['type_url'].append((type, target_url))

    for key in data:
        for type, url in data[key]['type_url']:
            print("Accessing: " + url)
            driver.get(url)
            time.sleep(2)
            btn = driver.find_element(By.ID, 'cmpDownloadApiButton')
            btn.click()
            time.sleep(2)

    driver.quit()
