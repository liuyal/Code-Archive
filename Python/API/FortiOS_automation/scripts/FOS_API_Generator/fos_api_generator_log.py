import os
import re

api_log_template = '''
class <CN>(Template):
    """LOG API <P> """

    def __init__(self, logger, fgt, <ST>):
        """
        Parameters
        ----------
        logger : object
            Logger object for saving kinds of log level to mongodb and print to terminal.
        fgt : dict
            fgt is a dict with fgt detail info, eg: management ip, admin https port, api token...
        <ST> : str
            type of log that can be retrieved. <SP>
        """
        self.logger = logger
        self.fgt = fgt
        assert type(<ST>) == str, '<ST> should be string'
        self.<ST> = <ST>
        self.path = '<BP>/' + self.<ST>
'''

function_template = '''    
    def <F>(self, params=None):
        path = <P>
        self.get(path=path, params=params)
'''

download_get_template = '''
    def <F>(self, path=None, params=None, file_name=None, s3=False):
        p = self.path + '/<FP>/'
        return super().download(path=p, params=params, file_name=file_name, s3=s3)
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


def api_gen_log(api_group, output_path):
    method, path, enum = api_group['data'][0]
    path_elements = list(filter(None, path.split('/')))
    output_folder = output_path + os.sep + path_elements[0].replace('-', '_')

    if not os.path.exists(output_folder): os.mkdir(output_folder)
    f = open(output_folder + os.sep + '__init__.py', 'w+')
    f.close()

    type_label = ''
    for item in api_group['data']:
        if "{" in item[1]:
            type_label = item[1][item[1].find('{') + 1:item[1].find('}')]
            if type_label == 'type':
                type_label = 'types'
            break

    if api_group['type'] == 1:
        file = path_elements[1].replace('-', '_').replace('.', '_').replace('+', '_')
        f = create_py_file(output_folder, file)
        if type_label == '':
            CN = create_CN(path_elements, 1)
            x = api_log_template.replace('<CN>', CN).replace(', <ST>', '').replace('<P>', path).replace(' + self.<ST>', '')
            x = x.replace('<BP>', path).split('\n')
            del x[17:19], x[12:14]
            x = '\n'.join(x)
            f.write(x)
            f.flush()
        elif type_label == 'session_id':
            CN = create_CN(path_elements, 0)
            P = path[0:path.find('{')]
            x = api_log_template.replace('<CN>', CN).replace('<ST>', type_label).replace('<P>', P).replace('<BP>', P)
            x = x.replace('<SP>', '').replace('str,', 'int,').replace('string', 'integer')
            x = 'str(self.session_id)'.join(x.rsplit('self.session_id', 1)).replace('//', '/').replace('\t','    ')
            f.write(x)
            f.flush()
        f.close()

    elif api_group['type'] == 2:
        file = path_elements[0].replace('-', '_').replace('.', '_').replace('+', '_')
        f = create_py_file(output_folder, file)
        CN = create_CN(path_elements, 0)
        x = api_log_template.replace('<CN>', CN).replace('<ST>', type_label)
        x = x.replace('<SP>', '\n\t\t\tAvailable type of enums: [' + enum.replace(',', ', ') + ']')
        x = x.replace('<BP>', '/' + path_elements[0]).replace('<P>', path).replace('\t','    ')
        f.write(x)
        f.flush()
        for item in api_group['data'][1:]:
            method, path, enum = item
            path_elements = list(filter(None, path.split('/')))
            F = path_elements[-1].replace('-', '_')
            if type_label not in path: path = path.replace('type', type_label)
            P = path.replace('{' + type_label + '}', "' + " + 'self.' + type_label + " + '")
            x = function_template.replace('<F>', F).replace('<P>', "'" + P + "/'")
            if 'download' in path_elements[-1]:
                x = download_get_template.replace('<F>', F).replace('<FP>', path_elements[-1])
            if 'raw' in path_elements[-1]:
                x = x.replace('self.get(', 'return self.get(')
            f.write(x)
            f.flush()
        f.close()

    elif api_group['type'] == 3:
        file = path_elements[1].replace('-', '_').replace('.', '_').replace('+', '_')
        f = create_py_file(output_folder, file)
        CN = create_CN(path_elements, 1)
        P = '/' + '/'.join(path_elements[0:2])
        x = api_log_template.replace('<CN>', CN).replace('<ST>', type_label)
        x = x.replace('<SP>', '\n\t\t\tAvailable type of enums: [' + enum.replace(',', ', ') + ']')
        x = x.replace('<BP>', P).replace('<P>', path).replace('\t','    ')
        f.write(x)
        f.flush()
        for item in api_group['data'][1:]:
            method, path, enum = item
            path_elements = list(filter(None, path.split('/')))
            F = path_elements[-1].replace('-', '_')
            if type_label not in path: path = path.replace('type', type_label)
            P = path.replace('{' + type_label + '}', "' + " + 'self.' + type_label + " + '")
            x = function_template.replace('<F>', F).replace('<P>', "'" + P + "/'")
            if 'raw' in path_elements[-1]:
                x = x.replace('self.get(', 'return self.get(')
            f.write(x)
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
        enum = raw_list[i].split('|')[2]
        api_list.append((type, path, enum))

    api_list = list(set([i for i in api_list]))
    api_list.sort(key=lambda x: x[1])

    api_group = {}
    for i in range(0, len(api_list)):
        type, path, enum = api_list[i]
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
            api_group[key]['type'] = 1
        else:
            max_count = -1
            for type, api_path, enum in group['data']:
                if api_path.count('/') > max_count:
                    max_count = api_path.count('/')

            if max_count == 3:
                api_group[key]['type'] = 2
            elif max_count == 4:
                api_group[key]['type'] = 3

    for item in api_group:
        api_gen_log(api_group[item], output_path)
