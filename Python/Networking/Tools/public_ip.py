import os
import sys
import time
import requests

if __name__ == "__main__":
    ip = requests.get('https://api.ipify.org').text
    print('Public IP: {}'.format(ip))
