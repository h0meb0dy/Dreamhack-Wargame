result = b'\xac\xf3\x0c%\xa3\x10\xb7%\x16\xc6\xb7\xbc\x07%\x02\xd5\xc6\x11\x07\xc5\x00' # IDAPython> get_bytes(0x140003000, 0x15)
flag = b''

for idx in range(0x15):
    for i in range(0x100):
        if (-5 * i) % 0x100 == result[idx]:
            flag += bytes([i])

print(flag)