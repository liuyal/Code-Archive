import os
import re

api_config_template = '''
class <CN>(Template):
    """Configure <P>/"""

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
        self.path = '/<P>/'
'''

hard_wait = '''
    def create(self, params=None, data=None, sleep=<TIME>, verbose=True):
        return super().create(params=params, data=data, sleep=sleep, verbose=verbose)

    def update(self, mkey=None, params=None, data=None, sleep=<TIME>, verbose=True):
        return super().update(mkey=mkey, params=params, data=data, sleep=sleep, verbose=verbose)

    def delete(self, mkey, params=None, sleep=<TIME>, verbose=True):
        return super().delete(mkey=mkey, params=params, sleep=sleep, verbose=verbose)
'''

wait_list = ["policy", "proxy-policy", "interface"]


def api_gen_config(path, type, function, subtypes='', output_path='', mkey_tag=''):
    fixed_type = type.split('.')[0].replace('-', '_').replace('.', '_').replace('+', '_')

    output_folder = output_path + os.sep + fixed_type

    if subtypes != '':
        file = subtypes.replace('-', '_').replace('.', '_').replace('+', '_')
    else:
        file = type.replace('-', '_').replace('.', '_').replace('+', '_')

    if file[0].isdigit(): file = "_" + file

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    f = open(output_folder + os.sep + '__init__.py', 'w+')
    f.close()

    if not os.path.exists(output_folder + os.sep + file + '.py'):
        f = open(output_folder + os.sep + file + '.py', 'a+')
        f.truncate(0)
        f.write('from ..template import Template\n\n')
        f.flush()
    else:
        f = open(output_folder + os.sep + file + '.py', 'a+')

    func_str = function[0].upper() + function[1:]
    letters = [char for char in func_str]
    indexes = [m.start() for m in re.finditer('-', func_str)]
    for i in indexes: letters[i + 1] = func_str[i + 1].upper()
    func_str = ''.join(letters)
    CN = func_str.replace('-', '').replace('+', '')
    if CN[0].isdigit(): CN = "_" + CN

    if mkey_tag != '':
        tag = "        self.mkey_label = '" + mkey_tag + "'\n"
        x = api_config_template.replace('<P>', path).replace('<CN>', CN) + tag
    else:
        x = api_config_template.replace('<P>', path).replace('<CN>', CN)

    if function in wait_list and type == 'firewall': x = x + hard_wait.replace('<TIME>', '2')
    if function in wait_list and type == 'system': x = x + hard_wait.replace('<TIME>', '1')

    f.write(x + '\n')
    f.flush()
    f.close()


def runner(input_file, output_path):
    f = open(input_file, 'r+')
    api_list = f.read()
    f.close()

    api_list = list(filter(None, api_list.split('\n')))

    for line in api_list:

        item = line.split('|')[1][1:]

        type = item.split('/')[0].split('.', 1)[0]

        if '.' in item:
            subtype = item.split('/')[0].split('.', 1)[1]
        else:
            subtype = ''

        function = item.split('/')[-1]

        mkey_tag = line.split('|')[-1]

        api_gen_config(item, type, function, subtype, output_path, mkey_tag)
