import os
import sys
import time
import shutil

if __name__ == "__main__":

    folder = r'C:\Users\ljerry\OneDrive - Fortinet\1_Tasks\Ice_Bucket'
    name = ''

    for item in os.listdir(folder):
        for file in os.listdir(folder + os.sep + item):
            if '.url' in file:
                name = file.replace('.url', '')
                name = name.split(' ')
                if len(name[0]) == 1: name.pop(0)
                if '-' !=  name[1]: name.insert(1, ' - ')
                name = ' '.join(name)
                name = name.replace('  ',' ')
                print(name)
        os.rename(folder + os.sep + item, folder + os.sep + name)

    for item in os.listdir(folder):
        os.rename(folder + os.sep + item, folder + os.sep + item.split(' ')[0])