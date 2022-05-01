import string
from pwn import *
import hashlib

result = [0 for i in range(18)]
result[0] = 0xFE5D3A093968D02B
result[1] = 0xBA0AA367C2862EAE
result[2] = 0x8BEA2ADA9E26604F
result[3] = 0x2E6F41C96DCF5224
result[4] = 0x7FD91BD2949B75F3
result[5] = 0x5B1ED8E6072F3A6
result[6] = 0xC94045C6D4887611
result[7] = 0x9D43DF6DF6B94D95
result[8] = 0xB9A8A83C8AC08D80
result[9] = 0x6D78E80376518464
result[10] = 0xE81A20F2023C2D0
result[11] = 0x2E41EAE69D89F186
result[12] = 0x425C831DD2A3E5FD
result[13] = 0x82788DBBDC4100EC
result[14] = 0x6D0FEE8D3901DD20
result[15] = 0xEBE82A0A41E5D783
result[16] = 0x2AFA26414B72E506
result[17] = 0xD1848E9C21D114D

chars = string.printable.encode()
flag = b'DH{'

for i in range(1, 9):
    hash_result = p64(result[i * 2]) + p64(result[i * 2 + 1])

    for char1 in chars:
        for char2 in chars:
            for char3 in chars:
                found = False

                tmp = bytes([char1]) + bytes([char2]) + bytes([char3])
                if hashlib.md5(tmp).digest() == hash_result:
                    flag += tmp
                    found = True
                    break

            if found == True:
                break
            
        if found == True:
            break

    print(flag)