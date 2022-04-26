from datetime import datetime
import requests

tm_mon = datetime.today().month # month of today
tm_mday = datetime.today().day # day of today
v2 = tm_mday * tm_mon

str1 = b'oh! handsome guy!'
str2 = b'Air fares to NY don\'t come cheap.'

dword_10003388 = b''

for idx in range(len(str1)):
    v3 = v2 + str1[idx]
    v4 = 126 * ((((0x7DF7DF7D * v3) >> 32) - v3) >> 6) + (((((0x7DF7DF7D * v3) >> 32) - v3) >> 31)) + v3
    if v4 < 33:
        v4 += tm_mon + 33
    v2 += tm_mon
    dword_10003388 += bytes([v4 & 0xff])

print(dword_10003388)

v8 = tm_mday * tm_mon

for idx in range(len(str2)):
    v9 = v8 + str2[idx]
    v10 = 126 * (((((0x7DF7DF7D * v9) >> 32) - v9) >> 6) + ((((0x7DF7DF7D * v9) >> 32) - v9) >> 31)) + v9
    if v10 < 33:
        v10 += tm_mday + 33
    v8 += tm_mday
    print(chr(v10 % 0x100))

