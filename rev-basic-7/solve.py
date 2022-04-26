# rotate right
def ror(value, n):
    return (value >> n) + ((value << (8 - n)) & 0xff)

result = b'R\xdf\xb3`\xf1\x8b\x1c\xb5W\xd1\x9f8K)\xd9&\x7f\xc9\xa3\xe9S\x18O\xb8j\xcb\x87X[9\x1e\x00' # IDAPython> get_bytes(0x140003000, 0x20)
input_bytes = b''

for idx in range(0x1f):
    input_bytes += bytes([ror(result[idx] ^ idx, idx & 7)])

print(input_bytes)