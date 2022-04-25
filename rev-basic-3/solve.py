result = b'I`gtcgBf\x80xii{\x99m\x88h\x94\x9f\x8dM\xa5\x9dE\x00\x00\x00\x00\x00\x00\x00\x00' # IDAPython> get_bytes(0x140003000, 0x20)
flag = b''

for i in range(0x18):
    flag += bytes([(result[i] - 2 * i) ^ i])

print(flag)