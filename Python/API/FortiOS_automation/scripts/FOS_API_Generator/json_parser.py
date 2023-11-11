import os
import sys
import time
import shutil
import json


def runner(json_files_path, file_name):
    api_paths = []
    for file in os.listdir(json_files_path):
        type = file.split()[-3]
        f = open(json_files_path + os.sep + file, 'r')
        txt = f.read()
        f.close()

        data = json.loads(txt)
        for path in data['paths']:
            methods = list(data['paths'][path].keys())
            enum = ''

            if "log" in type.lower():
                for method in methods:
                    for index in data['paths'][path][method]['parameters']:
                        if 'enum' in index:
                            enum = index['enum']

            elif "config" in type.lower():
                if '{' in path:
                    enum = path.split('{')[-1].replace('}', '')
                    path = path.split('{')[0][:-1]

            api_paths.append((type, methods, path, enum))

    for i in range(0, len(api_paths)):
        type, method, path, enum = api_paths[i]
        if "config" in type.lower():
            for j in range(i + 1, len(api_paths)):
                type2, method2, path2, enum2 = api_paths[j]
                if path2 == path:
                    api_paths[i] = type, list(dict.fromkeys(method + method2)), path, enum
                    api_paths[j] = ('', '', '', '')
                else:
                    break

    api_paths = [item for item in api_paths if item[0] != '']

    try:
        os.remove(file_name + '_configuration.txt')
        os.remove(file_name + '_log.txt')
        os.remove(file_name + '_monitor.txt')
    except:
        pass

    for type, method, path, enum in api_paths:
        api_methods = ','.join(method)
        api_enum = enum
        if "log" in type.lower():
            api_enum = ','.join(enum)
        f = open(file_name + '_' + type.lower() + '.txt', 'a+')
        f.write(api_methods + '|' + path + '|' + api_enum + '\n')
        f.flush()
        f.close()
