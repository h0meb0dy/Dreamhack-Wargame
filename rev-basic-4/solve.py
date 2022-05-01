result = b"$'\x13\xc6\xc6\x13\x16\xe6G\xf5&\x96G\xf5F'\x13&&\xc6V\xf5\xc3\xc3\xf5\xe3\xe3\x00" # IDAPython> get_bytes(0x140003000, 0x1c)
flag = b''

for char in result:
    flag += bytes([(char >> 4) + ((char << 4) & 0xff)])

print(flag)