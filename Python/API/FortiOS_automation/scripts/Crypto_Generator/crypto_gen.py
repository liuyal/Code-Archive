from smb.SMBConnection import SMBConnection
from cryptography.fernet import Fernet


def generate_key(file_path):
    key = Fernet.generate_key()
    key_file = open(file_path, "wb")
    key_file.write(key)
    key_file.flush()
    key_file.close()
    return key


if __name__ == "__main__":

    k = generate_key("key.txt")
    f = Fernet(k)
    token = f.encrypt(b"")
    f = open("encrypt_pwd.key", "w")
    f.truncate(0)
    f.write(token.decode('utf-8'))
    f.flush()
    f.close()

    encrypt_pwd = open("encrypt_pwd.key", "r").read()
    fernet_code = Fernet(open("key.txt", "rb").read())
    decoded_pwd = fernet_code.decrypt(encrypt_pwd.encode('utf-8')).decode()

    conn = SMBConnection(username='ljerry', password=decoded_pwd, my_name='VAN-915138-LT0', remote_name='FORTINET-US', domain='FORTINET-US')
    conn.connect('172.16.100.80')
    results = conn.listPath('images', '/')
    for x in results: print(x.filename)
