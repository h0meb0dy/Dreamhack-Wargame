result = b'\xad\xd8\xcb\xcb\x9d\x97\xcb\xc4\x92\xa1\xd2\xd7\xd2\xd6\xa8\xa5\xdc\xc7\xad\xa3\xa1\x98L\x00' # IDAPython> get_bytes(0x140003000, 0x18)
input_arr = [0 for i in range(len(result))]

for i in reversed(range(len(result) - 1)):
    input_arr[i] = result[i] - input_arr[i + 1]

flag = b''

for i in range(len(input_arr)):
    flag += bytes([input_arr[i]])

print(flag)