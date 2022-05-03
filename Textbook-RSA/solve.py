from pwn import *
from Crypto.Util.number import long_to_bytes
import binascii

r = remote('host1.dreamhack.games', 19484)

sla = r.sendlineafter

def encrypt(pt):
    sla(b'[3] Get info\n', b'1')
    sla(b'Input plaintext (hex): ', binascii.hexlify(long_to_bytes(pt)))
    return int(r.recvline()[:-1])

def decrypt(ct):
    sla(b'[3] Get info\n', b'2')
    sla(b'Input ciphertext (hex): ', binascii.hexlify(long_to_bytes(ct)))
    return int(r.recvline()[:-1])

def get_info():
    sla(b'[3] Get info\n', b'3')
    
    r.recvuntil(b'N: ')
    n = int(r.recvline()[:-1])

    r.recvuntil(b'e: ')
    e = int(r.recvline()[:-1])

    r.recvuntil(b'FLAG: ')
    flag_enc = int(r.recvline()[:-1])

    return n, e, flag_enc

n, e, flag_enc = get_info()
c = encrypt(2) # ciphertext of 0x02
flag_int = decrypt(flag_enc * c % n) >> 1
flag = long_to_bytes(flag_int)
print(flag)

r.interactive()