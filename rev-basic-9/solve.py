# rotate left
def rol(char, n):
    return ((char << n) & 0xff) + (char >> (8 - n))

key = b'I_am_KEY'
correct_result = b'~}\x9a\x8b%-\xd5=\x03+8\x98\'\x9fO\xbc*y\x00}\xc4*OX' # IDAPython> get_bytes(0x140004000, 0x18)
chars = b'c|w{\xf2ko\xc50\x01g+\xfe\xd7\xabv\xca\x82\xc9}\xfaYG\xf0\xad\xd4\xa2\xaf\x9c\xa4r\xc0\xb7\xfd\x93&6?\xf7\xcc4\xa5\xe5\xf1q\xd81\x15\x04\xc7#\xc3\x18\x96\x05\x9a\x07\x12\x80\xe2\xeb\'\xb2u\t\x83,\x1a\x1bnZ\xa0R;\xd6\xb3)\xe3/\x84S\xd1\x00\xed \xfc\xb1[j\xcb\xbe9JLX\xcf\xd0\xef\xaa\xfbCM3\x85E\xf9\x02\x7fP<\x9f\xa8Q\xa3@\x8f\x92\x9d8\xf5\xbc\xb6\xda!\x10\xff\xf3\xd2\xcd\x0c\x13\xec_\x97D\x17\xc4\xa7~=d]\x19s`\x81O\xdc"*\x90\x88F\xee\xb8\x14\xde^\x0b\xdb\xe02:\nI\x06$\\\xc2\xd3\xacb\x91\x95\xe4y\xe7\xc87m\x8d\xd5N\xa9lV\xf4\xeaez\xae\x08\xbax%.\x1c\xa6\xb4\xc6\xe8\xddt\x1fK\xbd\x8b\x8ap>\xb5fH\x03\xf6\x0ea5W\xb9\x86\xc1\x1d\x9e\xe1\xf8\x98\x11i\xd9\x8e\x94\x9b\x1e\x87\xe9\xceU(\xdf\x8c\xa1\x89\r\xbf\xe6BhA\x99-\x0f\xb0T\xbb\x16' # IDAPython> get_bytes(0x140004020, 0x100)

input_arr = [correct_result[idx] for idx in range(len(correct_result))]

# inverse operation
for idx in reversed(range(3)):
    for i in range(16):
        for j in reversed(range(8)):
            input_arr[idx * 8 + ((j + 1) & 7)] = (rol(input_arr[idx * 8 + ((j + 1) & 7)], 5) - chars[key[j] ^ input_arr[idx * 8 + (j & 7)]]) & 0xff

# get flag
flag = ''
for idx in range(len(input_arr)):
    flag += chr(input_arr[idx])
print('DH{' + flag + '}')