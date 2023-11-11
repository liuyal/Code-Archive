import os
import re

api_monitor_class_template = '''
class <CN>(Template):
    """Monitor <P>/"""

    def __init__(self, logger, fgt):
        """
        Parameters
        ----------
        logger : object
            Logger object for saving kinds of log level to mongodb and print to terminal.
        fgt : dict
            fgt is a dict with fgt detail info, eg: management ip, admin https port, api token...
        """
        self.logger = logger
        self.fgt = fgt
        self.path = '<P>/'
'''

post_template = '''    def <F>(self, params=None, data=None, verbose=True):
        path = self.path + '<P>/'
        return self.create(path=path, params=params, data=data, verbose=verbose)
'''

get_template = '''    def <F>(self, params=None, verbose=True):
        path = self.path + '<P>/'
        return self.get(path=path, params=params, verbose=verbose)
'''

post_template_t3 = '''    def <F>(self, params=None, data=None, verbose=True):
        return self.create(params=params, data=data, verbose=verbose)
'''

get_template_t3 = '''    def <F>(self, params=None, verbose=True):
        return self.get(params=params, verbose=verbose)
'''

download_get_template = '''    def download(self, path=None, params=None, file_name=None, s3=False, verbose=True):
        p = self.path + 'download/'
        return super().download(path=p, params=params, file_name=file_name, s3=s3, verbose=verbose)
'''

deauth_all = '''    def deauth_all(self):
        response = self.get()
        if response:
            users = []
            for user in response:
                users.append({"id": user['uid'], "ip": user['ipaddr'], "user_type": "proxy" if user['type'] == 'wad' else user['type']})
            self.deauth(data={"users": users})
'''


def create_py_file(output_folder, file):
    if not os.path.exists(output_folder + os.sep + file + '.py'):
        f = open(output_folder + os.sep + file + '.py', 'a+')
        f.truncate(0)
        f.write('from ..template import Template\n\n')
        f.flush()
    else:
        f = open(output_folder + os.sep + file + '.py', 'a+')
    return f


def create_CN(path_elements, element_index):
    CN = path_elements[element_index][0].upper() + path_elements[element_index][1:]
    letters = [char for char in CN]
    indexes = [m.start() for m in re.finditer('-', CN)]
    for i in indexes: letters[i + 1] = CN[i + 1].upper()
    CN = ''.join(letters)
    CN = CN.replace('-', '').replace('+', '')
    if CN[0].isdigit(): CN = "_" + CN
    return CN


def api_gen_monitor(api_group, output_path):
    method, path = api_group['data'][0]
    path_elements = list(filter(None, path.split('/')))
    output_folder = output_path + os.sep + path_elements[0].replace('-', '_')

    if not os.path.exists(output_folder): os.mkdir(output_folder)
    f = open(output_folder + os.sep + '__init__.py', 'w+')
    f.close()

    if api_group['type'] == 1:
        file = path_elements[1].replace('-', '_').replace('.', '_').replace('+', '_')
        f = create_py_file(output_folder, file)
        CN = create_CN(path_elements, 1)
        x = api_monitor_class_template.replace('<CN>', CN).replace('<P>', path)
        f.write(x + '\n')
        f.flush()
        for item in api_group['data'][1:]:
            method, path = item
            path_elements = list(filter(None, path.split('/')))
            F = path_elements[-1].replace('-', '_').replace('import', 'Import')
            if method == "POST":
                x = post_template.replace('<F>', F).replace('<P>', path_elements[-1])
            else:
                x = get_template.replace('<F>', F).replace('<P>', path_elements[-1])
            if 'create' in path_elements[-1]:
                x = x.replace('self.create', 'super().create')
            if 'download' == path_elements[-1] and method == 'GET':
                x = download_get_template
            if 'file' == path_elements[-1] and method == 'GET' and 'config-revision' in path_elements[-2]:
                x = download_get_template.replace('def download(', 'def file(').replace("'download/'", "'file/'")
            f.write(x + '\n')
            f.flush()

        if '/user/firewall' in api_group['data'][0]:
            f.write(deauth_all + '\n')
            f.flush()

        f.close()

    elif api_group['type'] == 2:
        file = path_elements[0].replace('-', '_').replace('.', '_').replace('+', '_')
        f = create_py_file(output_folder, file)
        CN = create_CN(path_elements, 1)
        x = api_monitor_class_template.replace('<CN>', CN).replace('<P>', path)
        f.write(x + '\n')
        f.flush()
        f.close()

    elif api_group['type'] == 3:
        file = path_elements[1].replace('-', '_').replace('.', '_').replace('+', '_')
        f = create_py_file(output_folder, file)
        CN = create_CN(path_elements, 1)
        x = api_monitor_class_template.replace('<CN>', CN).replace('<P>', path)
        f.write(x + '\n')
        f.flush()
        F = path_elements[-1].replace('-', '_').replace('import', "Import")
        if method == "POST":
            x = post_template_t3.replace('<F>', F)
        else:
            x = get_template_t3.replace('<F>', F)
        if 'create' in path_elements[-1]:
            x = x.replace('self.create', 'super().create')
        if 'download' == path_elements[-1] and method == 'GET':
            x = download_get_template.splitlines()
            x.pop(1)
            x = '\n'.join(x)
            x = x.replace('path=p', 'path=path')
        f.write(x + '\n')
        f.flush()
        f.close()

    elif api_group['type'] == 4:
        file = path_elements[1].replace('-', '_').replace('.', '_').replace('+', '_')
        f = create_py_file(output_folder, file)
        CN = create_CN(path_elements, 1)
        BP = '/' + '/'.join(path_elements[0:2])
        x = api_monitor_class_template.replace('<CN>', CN).replace('<P>', BP)
        f.write(x + '\n')
        f.flush()
        for item in api_group['data']:
            method, path = item
            path_elements = list(filter(None, path.split('/')))
            F = path_elements[-1].replace('-', '_').replace('import', "Import")
            if method == "POST":
                x = post_template.replace('<F>', F).replace('<P>', path_elements[-1])
            else:
                x = get_template.replace('<F>', F).replace('<P>', path_elements[-1])
            if 'create' in path_elements[-1]:
                x = x.replace('self.create', 'super().create')
            if 'download' == path_elements[-1] and method == 'GET':
                x = download_get_template
            f.write(x + '\n')
            f.flush()
        f.close()


def runner(input_file, output_path):
    f = open(input_file, 'r+')
    api_list = f.read()
    f.close()

    raw_list = list(filter(None, api_list.split('\n')))
    api_list = []

    for i in range(0, len(raw_list)):
        type = raw_list[i].split('|')[0].upper()
        path = raw_list[i].split('|')[1]
        api_list.append((type, path))

    api_list = list(set([i for i in api_list]))
    api_list.sort(key=lambda x: x[1])

    api_group = {}
    for i in range(0, len(api_list)):
        type, path = api_list[i]
        path2 = '/' + '/'.join(list(filter(None, path.split('/')))[0:2])
        if path2 not in api_group.keys():
            api_group[path2] = {}
            api_group[path2]['type'] = 0
            api_group[path2]['data'] = []
            api_group[path2]['data'].append(api_list[i])
        else:
            api_group[path2]['data'].append(api_list[i])

    for key in api_group:
        group = api_group[key]
        if len(group['data']) == 1:
            if group['data'][0][1].count('/') == 2:
                api_group[key]['type'] = 2
            elif group['data'][0][1].count('/') == 3:
                api_group[key]['type'] = 3
        else:
            if group['data'][0][1].count('/') == 2 and group['data'][1][1].count('/') == 3:
                api_group[key]['type'] = 1
            elif group['data'][0][1].count('/') == 3 and group['data'][1][1].count('/') == 3:
                api_group[key]['type'] = 4

    for item in api_group:
        api_gen_monitor(api_group[item], output_path)
