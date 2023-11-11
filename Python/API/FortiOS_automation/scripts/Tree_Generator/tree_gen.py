import os
import sys
import time
import json

if __name__ == "__main__":

    f = open(r'C:\Users\ljerry\OneDrive-Fortinet\3_Code\Python\FGT_Automation\scripts\FOS_API_Generator\api_json720\FortiOS 7.2 FortiOS 7.2.0 Configuration API firewall.json', 'r')
    data = json.load(f)
    f.close()

    mandatory_list = ['name', 'schedule', 'service', 'action', 'srcintf', 'dstintf', 'srcaddr', 'dstaddr']

    policy = data['paths']['/firewall/policy']['post']['parameters'][0]['schema']['properties']

    for key in policy:

        item = policy[key]

        key = key.replace('-', '_')

        if item['type'] == 'integer':
            type = 'int'
            array_key =''

        elif item['type'] == 'array':
            type = 'list'
            array_key =  ' #--*' + str(list(item['items']['properties'].keys())[0])
        else:
            type = 'str'
            array_key = ''

        # if key not in mandatory_list:
        #     print(key + ": " + type + '= None,')
        # else:
        #     print(key + ": " + type + ',' )

        if key not in mandatory_list:
            print('with suppress(KeyError): self.' + key + " = kargs['" + key + "'] "+ array_key)
        # else:
        #     print('self.' + key + ' = ' + key + array_key)

