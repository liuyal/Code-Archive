import yaml

with open("server_info.yaml", 'r') as stream:
    try: mysql_cred = yaml.safe_load(stream); print(mysql_cred)
    except yaml.YAMLError as exc: print(exc)