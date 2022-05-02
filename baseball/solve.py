'''
# find table

text_in_file = open('text_in.txt', 'rb')
text_in = text_in_file.read()
text_in_file.close()

text_out_file = open('text_out.txt', 'rb')
text_out = text_out_file.read()
text_out_file.close()

table_arr = [0 for i in range(64)]

for i in range(int(len(text_in) / 3)):
    table_arr[text_in[i * 3] >> 2] = text_out[i * 4]
    table_arr[(text_in[i * 3 + 1] >> 4) | (text_in[i * 3] * 16) & 0x30] = text_out[i * 4 + 1]
    table_arr[(text_in[i * 3 + 2] >> 6) | (text_in[i * 3 + 1] * 4) & 0x3c] = text_out[i * 4 + 2]
    table_arr[text_in[i * 3 + 2] & 0x3f] = text_out[i * 4 + 3]

i += 1

table_arr[text_in[i * 3] >> 2] = text_out[i * 4]

if len(text_in) % 3 == 1:
    table_arr[(text_in[i * 3] * 16) & 0x30] = text_out[i * 4 + 1]
elif len(text_in) % 3 == 2:
    table_arr[(text_in[i * 3 + 1] >> 4) | (text_in[i * 3] * 16) & 0x30] = text_out[i * 4 + 1]
    table_arr[(text_in[i * 3 + 1] * 4) & 0x3c]

table = b''
for t in table_arr:
    table += bytes([t])

table_file = open('table.txt', 'wb')
table_file.write(table)
table_file.close()
'''


# find flag

table_file = open('table.txt', 'rb')
table = table_file.read()
table_file.close()

flag_out_file = open('flag_out.txt', 'rb')
flag_out = flag_out_file.read()
flag_out_file.close()

flag = b''

for i in range(int(len(flag_out) / 4) - 1):
    flag_arr = [0, 0, 0] # flag[i * 3] ~ flag[i * 3 + 2]

    flag_arr[0] += table.index(flag_out[i * 4]) << 2
    flag_arr[0] += (table.index(flag_out[i * 4 + 1]) & 0x30) >> 4
    flag_arr[1] += (table.index(flag_out[i * 4 + 1]) & 0xf) << 4
    flag_arr[1] += (table.index(flag_out[i * 4 + 2]) & 0x3c) >> 2
    flag_arr[2] += (table.index(flag_out[i * 4 + 2]) & 0x3) << 6
    flag_arr[2] += table.index(flag_out[i * 4 + 3])

    flag += bytes([flag_arr[0]])
    flag += bytes([flag_arr[1]])
    flag += bytes([flag_arr[2]])

i += 1

flag_arr = [0, 0, 0] # flag[-3] ~ flag[-1]

flag_arr[0] += table.index(flag_out[i * 4]) << 2

if flag_out[i * 4 + 3] != ord(b'='): # len(flag) % 3 == 0
    flag_arr[0] += (table.index(flag_out[i * 4 + 1]) & 0x30) >> 4
    flag_arr[1] += (table.index(flag_out[i * 4 + 1]) & 0xf) << 4
    flag_arr[1] += (table.index(flag_out[i * 4 + 2]) & 0x3c) >> 2
    flag_arr[2] += (table.index(flag_out[i * 4 + 2]) & 0x3) << 6
    flag_arr[2] += table.index(flag_out[i * 4 + 3])
elif flag_out[i * 4 + 2] != ord(b'='): # len(flag) % 3 == 2
    flag_arr[0] += (table.index(flag_out[i * 4 + 1]) & 0x30) >> 4
    flag_arr[1] += (table.index(flag_out[i * 4 + 1]) & 0xf) << 4
    flag_arr[1] += table.index(flag_out[i * 4 + 2]) >> 2
else: # len(flag) % 3 == 1
    flag_arr[0] += table.index(flag_out[i * 4 + 1]) >> 4

flag += bytes([flag_arr[0]])
flag += bytes([flag_arr[1]])
flag += bytes([flag_arr[2]])

print(flag)